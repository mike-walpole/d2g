#!/usr/bin/env python3
"""
Script to initialize the DynamoDB schema table with schemas from JSON files
Run this after deploying the CDK stack
"""

import boto3
import json
import os
from datetime import datetime

def load_schema_from_file(filename: str) -> dict:
    """Load schema from JSON file"""
    schema_path = os.path.join(os.path.dirname(__file__), 'schemas', filename)
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Schema file not found: {schema_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in schema file {filename}: {e}")
        return None

def init_schema_from_file(filename: str):
    """Initialize the schema table with schema from JSON file"""
    
    # Get table name from environment or use default
    table_name = os.environ.get('SCHEMAS_TABLE', 'd2g-form-schemas')
    
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    # Load schema from file
    schema_data = load_schema_from_file(filename)
    if not schema_data:
        return None
    
    try:
        # Check if schema already exists
        existing = table.get_item(
            Key={
                'formId': schema_data['formId'],
                'version': schema_data['version']
            }
        ).get('Item')
        
        if existing:
            print(f"✅ Schema already exists for formId: {schema_data['formId']}, version: {schema_data['version']}")
            return existing
        
        # Insert the schema
        table.put_item(Item=schema_data)
        print(f"✅ Successfully created schema from {filename}:")
        print(f"   - Form ID: {schema_data['formId']}")
        print(f"   - Version: {schema_data['version']}")
        print(f"   - Description: {schema_data.get('description', 'N/A')}")
        
        return schema_data
        
    except Exception as e:
        print(f"❌ Error creating schema from {filename}: {str(e)}")
        return None

def init_cargo_types():
    """Initialize cargo types configuration in DynamoDB"""
    
    # Get table name from environment or use default
    table_name = os.environ.get('SCHEMAS_TABLE', 'd2g-form-schemas')
    
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    # Load cargo types from file
    cargo_data = load_schema_from_file('cargo_types.json')
    if not cargo_data:
        return None
    
    # Create cargo types configuration item
    cargo_config = {
        'formId': 'config',
        'version': 'cargo-types',
        'schema': cargo_data,
        'createdAt': datetime.utcnow().isoformat(),
        'isActive': True,
        'description': 'Cargo types configuration'
    }
    
    try:
        # Check if config already exists
        existing = table.get_item(
            Key={
                'formId': 'config',
                'version': 'cargo-types'
            }
        ).get('Item')
        
        if existing:
            print(f"✅ Cargo types config already exists")
            return existing
        
        # Insert the config
        table.put_item(Item=cargo_config)
        print(f"✅ Successfully created cargo types configuration:")
        print(f"   - {len(cargo_data['cargoTypes'])} cargo types loaded")
        
        return cargo_config
        
    except Exception as e:
        print(f"❌ Error creating cargo types config: {str(e)}")
        return None

def list_schemas():
    """List all schemas in the table"""
    table_name = os.environ.get('SCHEMAS_TABLE', 'd2g-form-schemas')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    try:
        response = table.scan()
        schemas = response.get('Items', [])
        
        if not schemas:
            print("📋 No schemas found in the table")
            return []
        
        print(f"📋 Found {len(schemas)} schema(s):")
        for schema in schemas:
            print(f"   - {schema['formId']} v{schema['version']} ({'Active' if schema.get('isActive') else 'Inactive'})")
            print(f"     Created: {schema.get('createdAt', 'Unknown')}")
        
        return schemas
        
    except Exception as e:
        print(f"❌ Error listing schemas: {str(e)}")
        return []

def init_translations():
    """Initialize translations configuration in DynamoDB"""
    
    # Get table name from environment or use default
    table_name = os.environ.get('SCHEMAS_TABLE', 'd2g-form-schemas')
    
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    # Load translations from file
    translations_data = load_schema_from_file('translations.json')
    if not translations_data:
        return None
    
    try:
        # Check if translations already exist
        existing = table.get_item(
            Key={
                'formId': 'config',
                'version': 'translations'
            }
        ).get('Item')
        
        if existing:
            print(f"✅ Translations config already exists")
            return existing
        
        # Insert the translations
        table.put_item(Item=translations_data)
        print(f"✅ Successfully created translations configuration:")
        print(f"   - Languages: en, zh")
        
        return translations_data
        
    except Exception as e:
        print(f"❌ Error creating translations config: {str(e)}")
        return None

if __name__ == "__main__":
    print("🚀 Initializing Dock2Gdansk Schema Table...")
    print("=" * 50)
    
    # Initialize schemas from JSON files
    schema = init_schema_from_file('dock2gdansk_schema.json')
    cargo_config = init_cargo_types()
    translations_config = init_translations()
    
    print("\n📋 Current schemas in table:")
    print("-" * 30)
    list_schemas()
    
    print("\n✅ Schema initialization complete!")
    print("\n📚 Next steps:")
    print("1. Test the schema API: GET /schema?formId=dock2gdansk-main")
    print("2. Get cargo types: GET /manage-schema (formId=config, version=cargo-types)")
    print("3. Get translations: GET /manage-schema (formId=config, version=translations)")
    print("4. Create new schemas: POST /manage-schema")
    print("5. Access admin panel: /kapitanat (requires Cognito auth)")
