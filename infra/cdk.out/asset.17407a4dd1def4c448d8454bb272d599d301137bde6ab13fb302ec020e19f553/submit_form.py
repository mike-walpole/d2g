import json
import boto3
import uuid
import os
from datetime import datetime
from typing import Dict, Any

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name='us-east-1')  # SES not available in ap-east-1
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
        
        # Send email notification to user via SES
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
                print(f"Failed to send user email: {email_error}")
                # Don't fail the entire request if email fails
        
        # Send admin notification email with dynamic subject and JSON attachment
        try:
            # Get cargo type name for subject line
            cargo_type_name = "Unknown"
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
                                    cargo_type_name = cargo['name'].get('en', cargo['name'].get('zh', 'Unknown'))
                                else:
                                    cargo_type_name = cargo['name']
                                break
                except Exception as e:
                    print(f"Warning: Could not get cargo type name: {str(e)}")
            
            # Format current date and time
            current_time = datetime.utcnow()
            date_str = current_time.strftime('%Y-%m-%d')
            time_str = current_time.strftime('%H:%M')
            
            # Create dynamic subject line
            subject = f"Nowe zapytanie {cargo_type_name} {date_str} {time_str}"
            
            # Create email body with form data
            email_body = f"""
Nowe zapytanie otrzymane:

ID Zgłoszenia: {submission_id}
Email użytkownika: {user_email}
Data i czas: {date_str} {time_str}
Wersja schematu: {schema_version}

Dane formularza:
"""
            
            # Add form fields to email body
            for field_id, value in form_data.items():
                if value:  # Only show non-empty fields
                    email_body += f"{field_id}: {value}\n"
            
            # Create JSON attachment data
            json_data = {
                'submission_id': submission_id,
                'timestamp': timestamp,
                'user_email': user_email,
                'form_id': form_id,
                'schema_version': schema_version,
                'form_data': form_data,
                'cargo_type_name': cargo_type_name
            }
            
            # Send email with attachment using SES Raw Email
            import email
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.application import MIMEApplication
            
            # Send to each recipient separately to avoid verification issues
            recipients = ['walpole.mike@gmail.com', 'Oliwia.Walter@portgdansk.pl']
            
            for recipient in recipients:
                try:
                    # Create message for each recipient
                    msg = MIMEMultipart()
                    msg['Subject'] = subject
                    msg['From'] = 'Dock2Gdansk <michal@dagodigital.com>'
                    msg['To'] = recipient
                    
                    # Add text body
                    msg.attach(MIMEText(email_body, 'plain', 'utf-8'))
                    
                    # Add JSON attachment
                    json_attachment = MIMEApplication(json.dumps(json_data, indent=2, ensure_ascii=False), _subtype='json')
                    json_attachment.add_header('Content-Disposition', 'attachment', filename=f'submission_{submission_id}_{date_str}_{time_str}.json')
                    msg.attach(json_attachment)
                    
                    # Send raw email
                    ses.send_raw_email(
                        Source='michal@dagodigital.com',
                        Destinations=[recipient],
                        RawMessage={'Data': msg.as_string()}
                    )
                    
                    print(f"Admin notification email sent successfully to {recipient}")
                    
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
