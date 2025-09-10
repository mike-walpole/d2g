import json
import boto3
import os
from typing import Dict, Any

# Initialize AWS client
dynamodb = boto3.resource('dynamodb')

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function to return configuration data (translations, cargo types)
    """
    try:
        # Parse query parameters
        query_params = event.get('queryStringParameters', {}) or {}
        config_type = query_params.get('type', 'all')  # all, translations, cargo-types
        language = query_params.get('lang', 'en')  # en, zh
        
        # Get config from DynamoDB
        schemas_table = dynamodb.Table(os.environ['SCHEMAS_TABLE'])
        
        result = {}
        
        if config_type in ['all', 'translations']:
            # Get translations
            response = schemas_table.get_item(
                Key={
                    'formId': 'config',
                    'version': 'translations'
                }
            )
            
            if 'Item' in response:
                translations = response['Item']['schema']['translations']
                if language in translations:
                    result['translations'] = translations[language]
                else:
                    result['translations'] = translations.get('en', {})
            else:
                result['translations'] = {}
        
        if config_type in ['all', 'cargo-types']:
            # Get cargo types with translations
            response = schemas_table.get_item(
                Key={
                    'formId': 'config',
                    'version': 'cargo-types'
                }
            )
            
            if 'Item' in response:
                cargo_types = response['Item']['schema']['cargoTypes']
                # Transform cargo types for frontend consumption
                transformed_cargo_types = []
                for cargo in cargo_types:
                    if cargo.get('active', True):
                        # Handle both old format (string name) and new format (object with translations)
                        if isinstance(cargo['name'], dict):
                            name = cargo['name'].get(language, cargo['name'].get('en', 'Unknown'))
                        else:
                            name = cargo['name']  # Fallback for old format
                        
                        transformed_cargo_types.append({
                            'id': cargo['id'],
                            'name': name,
                            'value': cargo['id']
                        })
                
                result['cargoTypes'] = transformed_cargo_types
            else:
                result['cargoTypes'] = []
        
        # Return the config
        return create_success_response(result)
        
    except Exception as e:
        print(f"Error retrieving config: {str(e)}")
        return create_error_response(500, 'Internal server error')

def create_success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Helper function to create success response"""
    return {
        'statusCode': 200,
        'headers': get_cors_headers(),
        'body': json.dumps({
            'success': True,
            **data
        })
    }

def create_error_response(status_code: int, error_message: str) -> Dict[str, Any]:
    """Helper function to create error response"""
    return {
        'statusCode': status_code,
        'headers': get_cors_headers(),
        'body': json.dumps({
            'success': False,
            'error': error_message
        })
    }

def get_cors_headers() -> Dict[str, str]:
    """Get standard CORS headers"""
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,OPTIONS'
    }
