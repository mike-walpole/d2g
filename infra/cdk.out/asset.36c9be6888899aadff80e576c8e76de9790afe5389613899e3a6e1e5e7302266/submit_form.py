import json
import boto3
import uuid
import os
import re
import requests
from datetime import datetime
from typing import Dict, Any, Tuple

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

def validate_form_data(form_data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, str]]:
    """
    Validate form data to prevent empty/invalid submissions.

    Returns:
        Tuple of (is_valid, error_message, field_errors)
    """
    field_errors = {}

    # Define required fields based on your form schema
    required_text_fields = {
        'company': 'Company name',
        'email': 'Email',
        'phone': 'Phone number',
        'contact_person': 'Contact person',
        'inquiry_content': 'Inquiry content'
    }

    required_select_fields = {
        'cargo_type': 'Cargo type',
        'referral_source': 'How did you hear about us'
    }

    required_consent_fields = {
        'privacy_consent': 'Privacy policy consent',
        'terms_consent': 'Terms of service consent',
        'cross_border_consent': 'Cross-border data transfer consent'
    }

    # 1. Check if form_data exists and is not empty
    if not form_data or not isinstance(form_data, dict):
        return False, "Form data is missing or invalid", {}

    # 2. Validate required text fields (must not be empty strings)
    for field, label in required_text_fields.items():
        value = form_data.get(field)
        if not value or not isinstance(value, str) or not value.strip():
            field_errors[field] = f"{label} is required"

    # 3. Validate required select fields (must have a value)
    for field, label in required_select_fields.items():
        value = form_data.get(field)
        if not value or not isinstance(value, str) or not value.strip():
            field_errors[field] = f"{label} is required"

    # 4. Validate required consent checkboxes (must be true)
    for field, label in required_consent_fields.items():
        value = form_data.get(field)
        if value is not True:  # Must be explicitly True, not just truthy
            field_errors[field] = f"{label} must be accepted"

    # 5. Validate email format
    if 'email' in form_data and form_data['email']:
        email = form_data['email'].strip()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            field_errors['email'] = "Invalid email format"

    # 6. Validate phone number (basic check - not empty and contains digits)
    if 'phone' in form_data and form_data['phone']:
        phone = str(form_data['phone']).strip()
        if not re.search(r'\d', phone):  # Must contain at least one digit
            field_errors['phone'] = "Invalid phone number format"

    # 7. Validate phone prefix exists
    phone_prefix = form_data.get('phone_prefix')
    if not phone_prefix or not isinstance(phone_prefix, str) or not phone_prefix.strip():
        field_errors['phone_prefix'] = "Phone prefix is required"

    # 8. If phone prefix is custom, validate custom_phone_prefix
    if phone_prefix == 'custom':
        custom_prefix = form_data.get('custom_phone_prefix')
        if not custom_prefix or not isinstance(custom_prefix, str) or not custom_prefix.strip():
            field_errors['custom_phone_prefix'] = "Custom phone prefix is required when 'custom' is selected"
        elif not re.match(r'^\+\d{1,4}$', custom_prefix.strip()):
            field_errors['custom_phone_prefix'] = "Custom phone prefix must be in format +XX (e.g., +33)"

    # Return validation result
    if field_errors:
        error_summary = f"Validation failed: {len(field_errors)} field(s) with errors"
        print(f"❌ Form validation failed: {field_errors}")
        return False, error_summary, field_errors

    print("✅ Form validation passed")
    return True, "", {}

def generate_submission_id() -> str:
    """
    Generate sequential submission ID in format 00000001, 00000002, etc.
    Uses DynamoDB counter for sequential numbering.
    """
    try:
        # Get the schemas table (same table, different key for counter)
        schemas_table = dynamodb.Table(os.environ['SCHEMAS_TABLE'])
        
        # Try to get current counter value
        counter_key = {'formId': 'counter', 'version': 'submission_id'}
        
        try:
            # Get current counter
            response = schemas_table.get_item(Key=counter_key)
            if 'Item' in response:
                current_counter = int(response['Item'].get('value', 0))
            else:
                # First submission - initialize counter
                current_counter = 0
                
        except Exception as e:
            print(f"Error reading counter, starting from 0: {e}")
            current_counter = 0
        
        # Increment counter for next submission
        next_counter = current_counter + 1
        
        # Update counter in database
        schemas_table.put_item(
            Item={
                'formId': 'counter',
                'version': 'submission_id', 
                'value': next_counter,
                'updatedAt': datetime.utcnow().isoformat()
            }
        )
        
        # Format as 8-digit string with leading zeros
        submission_id = f"{next_counter:08d}"
        
        print(f"Generated sequential submission ID: {submission_id} (counter: {next_counter})")
        return submission_id
        
    except Exception as e:
        print(f"Error generating sequential submission ID: {e}")
        # Fallback to timestamp-based ID
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

        # ===== SERVER-SIDE VALIDATION =====
        # Validate form data BEFORE processing
        is_valid, error_message, field_errors = validate_form_data(form_data)

        if not is_valid:
            print(f"🚫 Rejecting invalid submission: {error_message}")
            print(f"🚫 Field errors: {field_errors}")
            print(f"🚫 Received data: {json.dumps(form_data, indent=2)}")

            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                    'Access-Control-Allow-Methods': 'POST,OPTIONS'
                },
                'body': json.dumps({
                    'success': False,
                    'error': error_message,
                    'field_errors': field_errors
                })
            }
        # ===== END VALIDATION =====

        print(f"✅ Validation passed - processing submission")

        # Process form_data to handle custom phone prefix
        processed_form_data = form_data.copy()
        if form_data.get('phone_prefix') == 'custom' and form_data.get('custom_phone_prefix'):
            processed_form_data['phone_prefix'] = form_data.get('custom_phone_prefix')
            # Remove the custom_phone_prefix field since we've merged it into phone_prefix
            processed_form_data.pop('custom_phone_prefix', None)

        user_email = body.get('user_email', '')
        form_id = body.get('form_id', 'dock2gdansk-main')  # Allow frontend to specify form_id
        schema_version = body.get('schema_version')  # Allow frontend to specify version used
        
        # If schema version not provided, get the current latest version
        if not schema_version:
            try:
                schemas_table = dynamodb.Table(os.environ['SCHEMAS_TABLE'])
                # First try to get from legacy dock2gdansk-main record which has currentVersion
                legacy_response = schemas_table.get_item(
                    Key={'formId': 'dock2gdansk-main', 'version': '1.0.0'}
                )
                if 'Item' in legacy_response and 'currentVersion' in legacy_response['Item']:
                    schema_version = str(legacy_response['Item']['currentVersion'])
                    print(f"Got schema version from legacy record: {schema_version}")
                else:
                    # Fallback: look for latest versioned schema
                    schema_response = schemas_table.query(
                        KeyConditionExpression='formId = :formId',
                        ExpressionAttributeValues={':formId': 'homepage-form'},
                        ScanIndexForward=False,  # Get latest version first
                        Limit=1
                    )
                    if schema_response['Items']:
                        schema_version = schema_response['Items'][0]['version']
                        print(f"Got schema version from homepage-form: {schema_version}")
                    else:
                        schema_version = '1'  # Default to version 1
                        print("No schema version found, defaulting to version 1")
            except Exception as e:
                print(f"Warning: Could not retrieve schema version: {str(e)}")
                schema_version = '1'  # Default to version 1
        
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
            'userEmail': processed_form_data.get('email', user_email),  # Changed from 'user_email' to 'userEmail'
            'formData': processed_form_data,  # Use processed form data with custom phone prefix resolved
            'formId': form_id,  # Changed from 'form_id' to 'formId'
            'schemaVersion': schema_version,  # Changed from 'schema_version' to 'schemaVersion'
            'status': 'submitted',
            'submittedAt': timestamp,
            'companyName': processed_form_data.get('company', ''),  # Added companyName
            'cargoTypeName': cargo_type_name  # Changed from 'cargo_type_name' to 'cargoTypeName'
        }
        
        # Store in DynamoDB
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
        table.put_item(Item=item)
        
        # User confirmation email removed per request
        
        # Send admin notification email with dynamic subject and JSON attachment
        try:
            # Get company name from processed form data
            company_name = processed_form_data.get('company', 'Unknown Company')
            
            # Format current date in DD/MM/YYYY format
            current_time = datetime.utcnow()
            date_str = current_time.strftime('%d/%m/%Y')
            
            # Create subject line with format: "Dock2Gdansk:submission_id@wersja:1.0.0"
            subject = f"Dock2Gdansk:{submission_id}@wersja:{schema_version}"
            
            # Create full JSON data with exact schema structure
            json_data = {
                'submission_id': submission_id,
                'timestamp': timestamp,
                'user_email': processed_form_data.get('email', user_email),
                'form_id': form_id,
                'schema_version': schema_version,
                'form_data': processed_form_data,
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
                                'filename': f'dock2gdansk_{company_name.replace(" ", "_")}_{submission_id}.json',
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
