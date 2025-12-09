import json
import boto3
import os
from decimal import Decimal
from typing import Dict, Any

# Initialize AWS client
dynamodb = boto3.resource('dynamodb')

def decimal_to_number(obj):
    """Convert Decimal objects to regular numbers for JSON serialization"""
    if isinstance(obj, Decimal):
        # Convert to int if it's a whole number, otherwise float
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    elif isinstance(obj, dict):
        return {key: decimal_to_number(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_number(item) for item in obj]
    else:
        return obj

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function to return form schema from DynamoDB
    """
    try:
        # Parse query parameters
        query_params = event.get('queryStringParameters', {}) or {}
        form_id = query_params.get('formId', 'dock2gdansk-main')
        version = query_params.get('version', 'latest')
        
        # Get schema from DynamoDB
        schemas_table = dynamodb.Table(os.environ['SCHEMAS_TABLE'])
        
        if version == 'latest':
            # Get the latest version
            response = schemas_table.query(
                KeyConditionExpression='formId = :formId',
                ExpressionAttributeValues={':formId': form_id},
                ScanIndexForward=False,  # Descending order
                Limit=1
            )
            items = response.get('Items', [])
            if not items:
                return create_error_response(404, f'No schema found for formId: {form_id}')
            schema_item = items[0]
        else:
            # Get specific version
            response = schemas_table.get_item(
                Key={
                    'formId': form_id,
                    'version': version
                }
            )
            schema_item = response.get('Item')
            if not schema_item:
                return create_error_response(404, f'Schema not found for formId: {form_id}, version: {version}')
        
        # Return the schema from DynamoDB (convert Decimal objects)
        response_data = {
            'schema': decimal_to_number(schema_item['schema']),
            'metadata': {
                'formId': schema_item['formId'],
                'version': schema_item['version'],
                'createdAt': schema_item.get('createdAt'),
                'isActive': schema_item.get('isActive', True)
            }
        }
        return create_success_response(response_data)
        
    except Exception as e:
        print(f"Error retrieving form schema: {str(e)}")
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
