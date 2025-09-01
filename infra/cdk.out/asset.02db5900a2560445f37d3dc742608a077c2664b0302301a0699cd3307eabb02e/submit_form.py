import json
import boto3
import uuid
import os
from datetime import datetime
from typing import Dict, Any

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')
cognito = boto3.client('cognito-idp')

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function to handle form submissions
    """
    try:
        # Parse the request body
        body = json.loads(event.get('body', '{}'))
        
        # Extract form data
        form_data = body.get('formData', {})
        user_email = body.get('userEmail', '')
        form_id = body.get('formId', 'dock2gdansk-main')  # Allow frontend to specify formId
        schema_version = body.get('schemaVersion')  # Allow frontend to specify version used
        
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
        
        # Generate unique ID for the submission
        submission_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Prepare item for DynamoDB
        item = {
            'id': submission_id,
            'timestamp': timestamp,
            'userEmail': user_email,
            'formData': form_data,
            'formId': form_id,
            'schemaVersion': schema_version,
            'status': 'submitted',
            'submittedAt': timestamp
        }
        
        # Store in DynamoDB
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
        table.put_item(Item=item)
        
        # Send email notification via SES
        if user_email:
            try:
                email_body = f"""
                New form submission received:
                
                Submission ID: {submission_id}
                User Email: {user_email}
                Timestamp: {timestamp}
                
                Form Data:
                {json.dumps(form_data, indent=2)}
                """
                
                ses.send_email(
                    Source=os.environ['SES_IDENTITY'],
                    Destination={
                        'ToAddresses': [user_email]
                    },
                    Message={
                        'Subject': {
                            'Data': 'Form Submission Confirmation - Dock2Gdansk'
                        },
                        'Body': {
                            'Text': {
                                'Data': email_body
                            }
                        }
                    }
                )
            except Exception as email_error:
                print(f"Failed to send email: {email_error}")
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
                'submissionId': submission_id,
                'message': 'Form submitted successfully',
                'formId': form_id,
                'schemaVersion': schema_version,
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
