import json
import boto3
import os
from datetime import datetime
from typing import Dict, Any

# Initialize AWS client
dynamodb = boto3.resource('dynamodb')

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function to manage form schemas (CRUD operations with versioning)
    """
    try:
        # Parse the request
        http_method = event.get('httpMethod', 'GET')
        body = json.loads(event.get('body', '{}')) if event.get('body') else {}
        query_params = event.get('queryStringParameters', {}) or {}
        
        table = dynamodb.Table(os.environ['SCHEMAS_TABLE'])
        
        if http_method == 'GET':
            # Get schema - either latest version or specific version
            form_id = query_params.get('formId', 'default')
            version = query_params.get('version', 'latest')
            
            if version == 'latest':
                # Get the latest version
                response = table.query(
                    KeyConditionExpression='formId = :formId',
                    ScanIndexForward=False,  # Descending order
                    Limit=1
                )
                items = response.get('Items', [])
                if not items:
                    return create_response(404, {
                        'success': False,
                        'error': f'Schema not found for formId: {form_id}'
                    })
                schema = items[0]
            else:
                # Get specific version
                response = table.get_item(
                    Key={
                        'formId': form_id,
                        'version': version
                    }
                )
                schema = response.get('Item')
                if not schema:
                    return create_response(404, {
                        'success': False,
                        'error': f'Schema not found for formId: {form_id}, version: {version}'
                    })
            
            return create_response(200, {
                'success': True,
                'schema': schema
            })
            
        elif http_method == 'POST':
            # Create new schema version
            form_id = body.get('formId', 'default')
            schema_data = body.get('schema', {})
            version = body.get('version')  # Optional, will auto-generate if not provided
            
            if not version:
                # Auto-generate version based on timestamp
                version = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            
            # Check if version already exists
            existing = table.get_item(
                Key={
                    'formId': form_id,
                    'version': version
                }
            ).get('Item')
            
            if existing:
                return create_response(409, {
                    'success': False,
                    'error': f'Schema version {version} already exists for formId: {form_id}'
                })
            
            # Create new schema
            schema_item = {
                'formId': form_id,
                'version': version,
                'schema': schema_data,
                'createdAt': datetime.utcnow().isoformat(),
                'isActive': body.get('isActive', True)
            }
            
            table.put_item(Item=schema_item)
            
            return create_response(201, {
                'success': True,
                'message': 'Schema created successfully',
                'formId': form_id,
                'version': version
            })
            
        elif http_method == 'PUT':
            # Update existing schema
            form_id = body.get('formId')
            version = body.get('version')
            schema_data = body.get('schema', {})
            
            if not form_id or not version:
                return create_response(400, {
                    'success': False,
                    'error': 'formId and version are required for updates'
                })
            
            # Check if schema exists
            existing = table.get_item(
                Key={
                    'formId': form_id,
                    'version': version
                }
            ).get('Item')
            
            if not existing:
                return create_response(404, {
                    'success': False,
                    'error': f'Schema not found for formId: {form_id}, version: {version}'
                })
            
            # Update schema
            update_expression = "SET schema = :schema, updatedAt = :updatedAt"
            expression_values = {
                ':schema': schema_data,
                ':updatedAt': datetime.utcnow().isoformat()
            }
            
            # Add optional fields
            if 'isActive' in body:
                update_expression += ", isActive = :isActive"
                expression_values[':isActive'] = body['isActive']
            
            table.update_item(
                Key={
                    'formId': form_id,
                    'version': version
                },
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values
            )
            
            return create_response(200, {
                'success': True,
                'message': 'Schema updated successfully',
                'formId': form_id,
                'version': version
            })
            
        elif http_method == 'DELETE':
            # Delete schema version
            form_id = query_params.get('formId')
            version = query_params.get('version')
            
            if not form_id or not version:
                return create_response(400, {
                    'success': False,
                    'error': 'formId and version are required for deletion'
                })
            
            # Check if schema exists
            existing = table.get_item(
                Key={
                    'formId': form_id,
                    'version': version
                }
            ).get('Item')
            
            if not existing:
                return create_response(404, {
                    'success': False,
                    'error': f'Schema not found for formId: {form_id}, version: {version}'
                })
            
            # Delete schema
            table.delete_item(
                Key={
                    'formId': form_id,
                    'version': version
                }
            )
            
            return create_response(200, {
                'success': True,
                'message': 'Schema deleted successfully',
                'formId': form_id,
                'version': version
            })
            
        else:
            return create_response(405, {
                'success': False,
                'error': 'Method not allowed'
            })
            
    except Exception as e:
        print(f"Error managing schema: {str(e)}")
        return create_response(500, {
            'success': False,
            'error': 'Internal server error'
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
