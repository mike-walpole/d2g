import json
import boto3
import uuid
import os
import requests
from datetime import datetime
from typing import Dict, Any

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
cognito = boto3.client('cognito-idp')

# Resend configuration
RESEND_API_KEY = 're_TbtKRqSo_CKVpSvn6vpTVu4UTHR2fAzqB'
RESEND_API_URL = 'https://api.resend.com/emails'

def get_admin_email_addresses():
    """
    Get email addresses from Analysis Email Recipients configuration
    """
    try:
        # Get email recipients from schemas table
        schemas_table = dynamodb.Table(os.environ['SCHEMAS_TABLE'])
        response = schemas_table.get_item(
            Key={'formId': 'config', 'version': 'analysis-emails'}
        )
        
        admin_emails = []
        
        if 'Item' in response and 'emails' in response['Item']:
            # Get active email recipients
            for email_config in response['Item']['emails']:
                if email_config.get('active', True):  # Default to active if not specified
                    admin_emails.append(email_config['email'])
        
        # Fallback to default recipients if no active emails found
        if not admin_emails:
            print("No active email recipients found in config, using fallback recipients")
            admin_emails = ['Marek.Machalski@portgdansk.pl', 'michal@dagodigital.com']
        
        print(f"Analysis email recipients: {admin_emails}")
        return admin_emails
        
    except Exception as e:
        print(f"Error getting analysis email recipients from config: {e}")
        print("Using fallback recipients")
        return ['Marek.Machalski@portgdansk.pl', 'michal@dagodigital.com']

def generate_submission_id() -> str:
    """
    Generate submission ID in format yyyymmdd_hhmmss[milliseconds]
    Example: 20250910_143052123
    """
    try:
        now = datetime.utcnow()
        # Format: yyyymmdd_hhmmss + milliseconds (3 digits)
        submission_id = now.strftime("%Y%m%d_%H%M%S") + f"{now.microsecond // 1000:03d}"
        
        print(f"Generated timestamp-based submission ID: {submission_id}")
        return submission_id
        
    except Exception as e:
        print(f"Error generating submission ID: {e}")
        # Fallback to simple timestamp
        fallback_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S000")
        print(f"Using fallback submission ID: {fallback_id}")
        return fallback_id

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function to handle form submissions
    """
    try:
        # Parse the request body
        body = json.loads(event.get('body', '{}'))
        
        # Extract form data
        form_data = body.get('form_data', {})
        user_email = body.get('user_email', '')
        form_id = body.get('form_id', 'dock2gdansk-main')  # Allow frontend to specify form_id
        schema_version = body.get('schema_version')  # Allow frontend to specify version used
        
        # If schema version not provided, get the current latest version
        if not schema_version:
            try:
                schemas_table = dynamodb.Table(os.environ['SCHEMAS_TABLE'])
                schema_response = schemas_table.query(
                    KeyConditionExpression='formId = :formId',
                    ExpressionAttributeValues={':formId': form_id},
                    ScanIndexForward=False,  # Descending order
                    Limit=1
                )
                if schema_response['Items']:
                    schema_version = schema_response['Items'][0]['version']
                else:
                    schema_version = 'unknown'
            except Exception as e:
                print(f"Warning: Could not retrieve schema version: {str(e)}")
                schema_version = 'unknown'
        
        # Generate timestamp-based ID for the submission
        submission_id = generate_submission_id()
        timestamp = datetime.utcnow().isoformat()
        
        # Get cargo type name for the record
        cargo_type_name = "Unknown Cargo"
        if 'cargo_type' in form_data and form_data['cargo_type']:
            try:
                # Get cargo types from config
                schemas_table = dynamodb.Table(os.environ['SCHEMAS_TABLE'])
                cargo_response = schemas_table.get_item(
                    Key={'formId': 'config', 'version': 'cargo-types'}
                )
                if 'Item' in cargo_response:
                    cargo_types = cargo_response['Item']['schema']['cargoTypes']
                    for cargo in cargo_types:
                        if cargo['id'] == form_data['cargo_type']:
                            if isinstance(cargo['name'], dict):
                                cargo_type_name = cargo['name'].get('en', cargo['name'].get('zh', 'Unknown Cargo'))
                            else:
                                cargo_type_name = cargo['name']
                            break
            except Exception as e:
                print(f"Warning: Could not get cargo type name: {str(e)}")
        
        # Prepare item for DynamoDB - exact schema structure as specified
        item = {
            'id': submission_id,  # Changed from 'submission_id' to 'id'
            'timestamp': timestamp,
            'userEmail': form_data.get('email', user_email),  # Changed from 'user_email' to 'userEmail'
            'formData': form_data,  # Changed from 'form_data' to 'formData'
            'formId': form_id,  # Changed from 'form_id' to 'formId'
            'schemaVersion': schema_version,  # Changed from 'schema_version' to 'schemaVersion'
            'status': 'submitted',
            'submittedAt': timestamp,
            'companyName': form_data.get('company', ''),  # Added companyName
            'cargoTypeName': cargo_type_name  # Changed from 'cargo_type_name' to 'cargoTypeName'
        }
        
        # Store in DynamoDB
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
        table.put_item(Item=item)
        
        # User confirmation email removed per request
        
        # Send admin notification email with dynamic subject and JSON attachment
        try:
            # Get company name from form data
            company_name = form_data.get('company', 'Unknown Company')
            
            # Format current date in DD/MM/YYYY format
            current_time = datetime.utcnow()
            date_str = current_time.strftime('%d/%m/%Y')
            
            # Create subject line with format: "Dock2Gdansk:submission_id@wersja:1.0.0"
            subject = f"Dock2Gdansk:{submission_id}@wersja:{schema_version}"
            
            # Create full JSON data with exact schema structure
            json_data = {
                'submission_id': submission_id,
                'timestamp': timestamp,
                'user_email': form_data.get('email', user_email),
                'form_id': form_id,
                'schema_version': schema_version,
                'form_data': form_data,
                'cargo_type_name': cargo_type_name
            }
            
            # Create email body with full JSON included
            email_body = f"""New Dock2Gdansk submission received:

Cargo Type: {cargo_type_name}
Company: {company_name}
Date: {date_str}
Submission ID: {submission_id}
User Email: {user_email}
Schema Version: {schema_version}

FULL SUBMISSION DATA (JSON):
{json.dumps(json_data, indent=2, ensure_ascii=False)}
"""
            
            # Convert JSON to base64 for attachment
            import base64
            json_content = json.dumps(json_data, indent=2, ensure_ascii=False)
            json_base64 = base64.b64encode(json_content.encode('utf-8')).decode('utf-8')
            
            # Get admin email addresses from Cognito User Pool
            recipients = get_admin_email_addresses()
            
            for recipient in recipients:
                try:
                    admin_email_data = {
                        'from': 'Dock2Gdansk <re-reply@comm.dagodigital.com>',
                        'to': [recipient],
                        'subject': subject,
                        'text': email_body,
                        'attachments': [
                            {
                                'filename': f'dock2gdansk_{company_name.replace(" ", "_")}_{date_str.replace("/", "-")}.json',
                                'content': json_base64
                            }
                        ]
                    }
                    
                    response = requests.post(
                        RESEND_API_URL,
                        headers={
                            'Authorization': f'Bearer {RESEND_API_KEY}',
                            'Content-Type': 'application/json'
                        },
                        json=admin_email_data
                    )
                    
                    if response.status_code == 200:
                        print(f"Admin notification email sent successfully to {recipient}")
                    else:
                        print(f"Failed to send admin email to {recipient}: {response.status_code} - {response.text}")
                        
                except Exception as recipient_error:
                    print(f"Failed to send email to {recipient}: {recipient_error}")
                    # Continue with other recipients even if one fails
            
        except Exception as admin_email_error:
            print(f"Failed to send admin email: {admin_email_error}")
            # Don't fail the entire request if email fails
        
        # Return success response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({
                'success': True,
                'submission_id': submission_id,
                'message': 'Form submitted successfully',
                'form_id': form_id,
                'schema_version': schema_version,
                'timestamp': timestamp
            })
        }
        
    except Exception as e:
        print(f"Error processing form submission: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({
                'success': False,
                'error': 'Internal server error'
            })
        }
