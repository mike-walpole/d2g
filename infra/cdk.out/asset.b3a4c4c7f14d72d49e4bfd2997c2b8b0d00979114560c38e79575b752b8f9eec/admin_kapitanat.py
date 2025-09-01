import json
import boto3
import os
from typing import Dict, Any
from datetime import datetime

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
cognito = boto3.client('cognito-idp')

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function for admin kapitanat dashboard operations
    Handles: view submissions, manage team members, update cargo types
    """
    try:
        # Parse the request
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '').split('/')[-1]  # Get last part of path
        body = json.loads(event.get('body', '{}')) if event.get('body') else {}
        query_params = event.get('queryStringParameters', {}) or {}
        
        # Verify admin authentication (check JWT token in Authorization header)
        auth_result = verify_admin_auth(event)
        if not auth_result['success']:
            return create_response(401, auth_result)
        
        # Route to appropriate handler
        if path == 'submissions':
            return handle_submissions(http_method, query_params, body)
        elif path == 'team-members':
            return handle_team_members(http_method, query_params, body)
        elif path == 'cargo-types':
            return handle_cargo_types(http_method, query_params, body)
        elif path == 'schemas':
            return handle_schemas(http_method, query_params, body)
        elif path == 'dashboard':
            return handle_dashboard(http_method, query_params)
        else:
            return create_response(404, {
                'success': False,
                'error': 'Endpoint not found'
            })
            
    except Exception as e:
        print(f"Error in admin kapitanat handler: {str(e)}")
        return create_response(500, {
            'success': False,
            'error': 'Internal server error'
        })

def verify_admin_auth(event: Dict[str, Any]) -> Dict[str, Any]:
    """Verify admin authentication via Cognito JWT token"""
    try:
        headers = event.get('headers', {})
        auth_header = headers.get('Authorization', '') or headers.get('authorization', '')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return {'success': False, 'error': 'Missing or invalid authorization header'}
        
        token = auth_header.replace('Bearer ', '')
        
        # Verify the token with Cognito
        response = cognito.get_user(AccessToken=token)
        user_attributes = {attr['Name']: attr['Value'] for attr in response['UserAttributes']}
        
        # Check if user has admin role (you can customize this logic)
        # For now, we'll check if user is in admin group
        user_groups = cognito.admin_list_groups_for_user(
            UserPoolId=os.environ['USER_POOL_ID'],
            Username=response['Username']
        )
        
        is_admin = any(group['GroupName'] == 'admin' for group in user_groups['Groups'])
        
        if not is_admin:
            return {'success': False, 'error': 'Insufficient privileges'}
        
        return {
            'success': True,
            'user': {
                'username': response['Username'],
                'email': user_attributes.get('email'),
                'groups': [group['GroupName'] for group in user_groups['Groups']]
            }
        }
        
    except Exception as e:
        print(f"Auth verification error: {str(e)}")
        return {'success': False, 'error': 'Authentication failed'}

def handle_submissions(http_method: str, query_params: Dict, body: Dict) -> Dict[str, Any]:
    """Handle form submissions management"""
    submissions_table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    if http_method == 'GET':
        # List submissions with pagination
        limit = int(query_params.get('limit', '50'))
        last_key = query_params.get('lastKey')
        
        scan_kwargs = {'Limit': limit}
        if last_key:
            scan_kwargs['ExclusiveStartKey'] = json.loads(last_key)
        
        response = submissions_table.scan(**scan_kwargs)
        
        return create_response(200, {
            'success': True,
            'submissions': response['Items'],
            'lastKey': response.get('LastEvaluatedKey'),
            'count': response['Count']
        })
    
    elif http_method == 'DELETE':
        # Delete submission
        submission_id = query_params.get('id')
        timestamp = query_params.get('timestamp')
        
        if not submission_id or not timestamp:
            return create_response(400, {
                'success': False,
                'error': 'Missing id or timestamp parameter'
            })
        
        submissions_table.delete_item(
            Key={'id': submission_id, 'timestamp': timestamp}
        )
        
        return create_response(200, {
            'success': True,
            'message': 'Submission deleted successfully'
        })
    
    else:
        return create_response(405, {'success': False, 'error': 'Method not allowed'})

def handle_team_members(http_method: str, query_params: Dict, body: Dict) -> Dict[str, Any]:
    """Handle team members management"""
    if http_method == 'GET':
        # List team members
        try:
            response = cognito.list_users(UserPoolId=os.environ['USER_POOL_ID'])
            users = []
            
            for user in response['Users']:
                user_groups = cognito.admin_list_groups_for_user(
                    UserPoolId=os.environ['USER_POOL_ID'],
                    Username=user['Username']
                )
                
                user_attributes = {attr['Name']: attr['Value'] for attr in user['Attributes']}
                
                users.append({
                    'username': user['Username'],
                    'email': user_attributes.get('email'),
                    'status': user['UserStatus'],
                    'enabled': user['Enabled'],
                    'groups': [group['GroupName'] for group in user_groups['Groups']],
                    'created': user['UserCreateDate'].isoformat(),
                    'lastModified': user['UserLastModifiedDate'].isoformat()
                })
            
            return create_response(200, {
                'success': True,
                'users': users
            })
            
        except Exception as e:
            return create_response(500, {
                'success': False,
                'error': f'Failed to list users: {str(e)}'
            })
    
    elif http_method == 'POST':
        # Add new team member
        email = body.get('email')
        temporary_password = body.get('temporaryPassword', 'TempPass123!')
        is_admin = body.get('isAdmin', False)
        
        if not email:
            return create_response(400, {
                'success': False,
                'error': 'Email is required'
            })
        
        try:
            # Create user
            response = cognito.admin_create_user(
                UserPoolId=os.environ['USER_POOL_ID'],
                Username=email,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'email_verified', 'Value': 'true'}
                ],
                TemporaryPassword=temporary_password,
                MessageAction='SUPPRESS'  # Don't send email automatically
            )
            
            # Add to admin group if specified
            if is_admin:
                cognito.admin_add_user_to_group(
                    UserPoolId=os.environ['USER_POOL_ID'],
                    Username=email,
                    GroupName='admin'
                )
            
            return create_response(201, {
                'success': True,
                'message': 'User created successfully',
                'username': email,
                'temporaryPassword': temporary_password
            })
            
        except Exception as e:
            return create_response(500, {
                'success': False,
                'error': f'Failed to create user: {str(e)}'
            })
    
    elif http_method == 'DELETE':
        # Remove team member
        username = query_params.get('username')
        
        if not username:
            return create_response(400, {
                'success': False,
                'error': 'Username is required'
            })
        
        try:
            cognito.admin_delete_user(
                UserPoolId=os.environ['USER_POOL_ID'],
                Username=username
            )
            
            return create_response(200, {
                'success': True,
                'message': 'User deleted successfully'
            })
            
        except Exception as e:
            return create_response(500, {
                'success': False,
                'error': f'Failed to delete user: {str(e)}'
            })
    
    else:
        return create_response(405, {'success': False, 'error': 'Method not allowed'})

def handle_cargo_types(http_method: str, query_params: Dict, body: Dict) -> Dict[str, Any]:
    """Handle cargo types management"""
    schemas_table = dynamodb.Table(os.environ['SCHEMAS_TABLE'])
    
    if http_method == 'GET':
        # Get current cargo types
        response = schemas_table.get_item(
            Key={'formId': 'config', 'version': 'cargo-types'}
        )
        
        if 'Item' not in response:
            return create_response(404, {
                'success': False,
                'error': 'Cargo types configuration not found'
            })
        
        return create_response(200, {
            'success': True,
            'cargoTypes': response['Item']['schema']['cargoTypes']
        })
    
    elif http_method == 'POST':
        # Add new cargo type
        name = body.get('name')
        
        if not name:
            return create_response(400, {
                'success': False,
                'error': 'Cargo type name is required'
            })
        
        # Get current config
        response = schemas_table.get_item(
            Key={'formId': 'config', 'version': 'cargo-types'}
        )
        
        if 'Item' not in response:
            return create_response(404, {
                'success': False,
                'error': 'Cargo types configuration not found'
            })
        
        config = response['Item']
        cargo_types = config['schema']['cargoTypes']
        next_id = config['schema']['nextId']
        
        # Add new cargo type
        new_cargo_type = {
            'id': str(next_id),
            'name': name,
            'active': True
        }
        cargo_types.append(new_cargo_type)
        
        # Update config
        config['schema']['cargoTypes'] = cargo_types
        config['schema']['nextId'] = next_id + 1
        config['schema']['lastUpdated'] = datetime.utcnow().isoformat()
        
        schemas_table.put_item(Item=config)
        
        return create_response(201, {
            'success': True,
            'message': 'Cargo type added successfully',
            'cargoType': new_cargo_type
        })
    
    elif http_method == 'PUT':
        # Update cargo type
        cargo_id = body.get('id')
        name = body.get('name')
        active = body.get('active')
        
        if not cargo_id:
            return create_response(400, {
                'success': False,
                'error': 'Cargo type ID is required'
            })
        
        # Get current config
        response = schemas_table.get_item(
            Key={'formId': 'config', 'version': 'cargo-types'}
        )
        
        if 'Item' not in response:
            return create_response(404, {
                'success': False,
                'error': 'Cargo types configuration not found'
            })
        
        config = response['Item']
        cargo_types = config['schema']['cargoTypes']
        
        # Find and update cargo type
        for cargo_type in cargo_types:
            if cargo_type['id'] == cargo_id:
                if name is not None:
                    cargo_type['name'] = name
                if active is not None:
                    cargo_type['active'] = active
                break
        else:
            return create_response(404, {
                'success': False,
                'error': 'Cargo type not found'
            })
        
        # Update config
        config['schema']['cargoTypes'] = cargo_types
        config['schema']['lastUpdated'] = datetime.utcnow().isoformat()
        
        schemas_table.put_item(Item=config)
        
        return create_response(200, {
            'success': True,
            'message': 'Cargo type updated successfully'
        })
    
    else:
        return create_response(405, {'success': False, 'error': 'Method not allowed'})

def handle_schemas(http_method: str, query_params: Dict, body: Dict) -> Dict[str, Any]:
    """Handle schema management with versioning"""
    schemas_table = dynamodb.Table(os.environ['SCHEMAS_TABLE'])
    
    if http_method == 'GET':
        # List all schemas or get specific schema versions
        form_id = query_params.get('formId')
        
        if form_id:
            # Get all versions of a specific form
            response = schemas_table.query(
                KeyConditionExpression='formId = :formId',
                ExpressionAttributeValues={':formId': form_id},
                ScanIndexForward=False  # Latest first
            )
            return create_response(200, {
                'success': True,
                'formId': form_id,
                'versions': response['Items']
            })
        else:
            # Get all schemas (exclude config items)
            response = schemas_table.scan(
                FilterExpression='formId <> :config',
                ExpressionAttributeValues={':config': 'config'}
            )
            
            # Group by formId
            schemas_by_form = {}
            for item in response['Items']:
                form_id = item['formId']
                if form_id not in schemas_by_form:
                    schemas_by_form[form_id] = []
                schemas_by_form[form_id].append({
                    'version': item['version'],
                    'createdAt': item.get('createdAt'),
                    'isActive': item.get('isActive', True),
                    'description': item.get('description', '')
                })
            
            # Sort versions for each form
            for form_id in schemas_by_form:
                schemas_by_form[form_id].sort(key=lambda x: x['createdAt'], reverse=True)
            
            return create_response(200, {
                'success': True,
                'schemas': schemas_by_form
            })
    
    elif http_method == 'POST':
        # Create new schema version
        form_id = body.get('formId')
        schema_data = body.get('schema')
        description = body.get('description', '')
        base_version = body.get('baseVersion')  # Version to copy from
        
        if not form_id or not schema_data:
            return create_response(400, {
                'success': False,
                'error': 'formId and schema are required'
            })
        
        try:
            # Generate new version number
            if base_version:
                # If copying from existing version, increment patch version
                version_parts = base_version.split('.')
                if len(version_parts) == 3:
                    major, minor, patch = version_parts
                    new_version = f"{major}.{minor}.{int(patch) + 1}"
                else:
                    new_version = f"{base_version}.1"
            else:
                # Get latest version for this form and increment
                response = schemas_table.query(
                    KeyConditionExpression='formId = :formId',
                    ExpressionAttributeValues={':formId': form_id},
                    ScanIndexForward=False,
                    Limit=1
                )
                
                if response['Items']:
                    latest_version = response['Items'][0]['version']
                    version_parts = latest_version.split('.')
                    if len(version_parts) == 3:
                        major, minor, patch = version_parts
                        new_version = f"{major}.{int(minor) + 1}.0"
                    else:
                        new_version = "1.1.0"
                else:
                    new_version = "1.0.0"
            
            # Create new schema version
            schema_item = {
                'formId': form_id,
                'version': new_version,
                'schema': schema_data,
                'createdAt': datetime.utcnow().isoformat(),
                'isActive': True,
                'description': description or f'Version {new_version} created by admin'
            }
            
            schemas_table.put_item(Item=schema_item)
            
            return create_response(201, {
                'success': True,
                'message': 'Schema version created successfully',
                'formId': form_id,
                'version': new_version,
                'schema': schema_item
            })
            
        except Exception as e:
            return create_response(500, {
                'success': False,
                'error': f'Failed to create schema version: {str(e)}'
            })
    
    elif http_method == 'PUT':
        # Update existing schema (creates new version)
        form_id = body.get('formId')
        version = body.get('version')
        schema_data = body.get('schema')
        description = body.get('description')
        is_active = body.get('isActive')
        
        if not form_id or not version:
            return create_response(400, {
                'success': False,
                'error': 'formId and version are required'
            })
        
        try:
            # Get existing schema
            response = schemas_table.get_item(
                Key={'formId': form_id, 'version': version}
            )
            
            if 'Item' not in response:
                return create_response(404, {
                    'success': False,
                    'error': 'Schema version not found'
                })
            
            existing_schema = response['Item']
            
            # Update fields
            update_expression = "SET updatedAt = :updatedAt"
            expression_values = {':updatedAt': datetime.utcnow().isoformat()}
            
            if schema_data is not None:
                update_expression += ", schema = :schema"
                expression_values[':schema'] = schema_data
            
            if description is not None:
                update_expression += ", description = :description"
                expression_values[':description'] = description
            
            if is_active is not None:
                update_expression += ", isActive = :isActive"
                expression_values[':isActive'] = is_active
            
            schemas_table.update_item(
                Key={'formId': form_id, 'version': version},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values
            )
            
            return create_response(200, {
                'success': True,
                'message': 'Schema updated successfully',
                'formId': form_id,
                'version': version
            })
            
        except Exception as e:
            return create_response(500, {
                'success': False,
                'error': f'Failed to update schema: {str(e)}'
            })
    
    elif http_method == 'DELETE':
        # Delete schema version (only if not the last active version)
        form_id = query_params.get('formId')
        version = query_params.get('version')
        
        if not form_id or not version:
            return create_response(400, {
                'success': False,
                'error': 'formId and version are required'
            })
        
        try:
            # Check if this is the last active version
            response = schemas_table.query(
                KeyConditionExpression='formId = :formId',
                FilterExpression='isActive = :active',
                ExpressionAttributeValues={':formId': form_id, ':active': True}
            )
            
            active_versions = response['Items']
            if len(active_versions) <= 1 and any(v['version'] == version for v in active_versions):
                return create_response(400, {
                    'success': False,
                    'error': 'Cannot delete the last active version of a schema'
                })
            
            # Delete the schema version
            schemas_table.delete_item(
                Key={'formId': form_id, 'version': version}
            )
            
            return create_response(200, {
                'success': True,
                'message': 'Schema version deleted successfully',
                'formId': form_id,
                'version': version
            })
            
        except Exception as e:
            return create_response(500, {
                'success': False,
                'error': f'Failed to delete schema version: {str(e)}'
            })
    
    else:
        return create_response(405, {'success': False, 'error': 'Method not allowed'})

def handle_dashboard(http_method: str, query_params: Dict) -> Dict[str, Any]:
    """Handle dashboard overview"""
    if http_method != 'GET':
        return create_response(405, {'success': False, 'error': 'Method not allowed'})
    
    try:
        # Get submissions count
        submissions_table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
        submissions_response = submissions_table.scan(Select='COUNT')
        submissions_count = submissions_response['Count']
        
        # Get recent submissions (last 10)
        recent_submissions = submissions_table.scan(Limit=10)['Items']
        recent_submissions.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Get schemas count
        schemas_table = dynamodb.Table(os.environ['SCHEMAS_TABLE'])
        schemas_response = schemas_table.scan(Select='COUNT')
        schemas_count = schemas_response['Count']
        
        # Get users count
        users_response = cognito.list_users(UserPoolId=os.environ['USER_POOL_ID'])
        users_count = len(users_response['Users'])
        
        return create_response(200, {
            'success': True,
            'dashboard': {
                'statistics': {
                    'totalSubmissions': submissions_count,
                    'totalSchemas': schemas_count,
                    'totalUsers': users_count
                },
                'recentSubmissions': recent_submissions[:5]  # Only return 5 most recent
            }
        })
        
    except Exception as e:
        return create_response(500, {
            'success': False,
            'error': f'Failed to load dashboard: {str(e)}'
        })

def create_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """Helper function to create consistent API responses"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
        },
        'body': json.dumps(body)
    }
