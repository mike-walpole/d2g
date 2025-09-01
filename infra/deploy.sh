#!/bin/bash

# Dock2Gdansk AWS CDK Deployment Script

set -e

echo "🚀 Starting Dock2Gdansk AWS CDK Deployment..."

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS CLI not configured. Please run 'aws configure' first."
    exit 1
fi

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "🔐 Using AWS Account: $ACCOUNT_ID"

# Set account in CDK context
echo "⚙️  Setting CDK context..."
cdk context --set account $ACCOUNT_ID

# Check if CDK is bootstrapped
if ! cdk list &> /dev/null; then
    echo "🔧 Bootstrapping CDK for region ap-east-1..."
    cdk bootstrap aws://$ACCOUNT_ID/ap-east-1
fi

# Show what will be deployed
echo "📋 Previewing deployment..."
cdk diff

# Ask for confirmation
read -p "🤔 Do you want to proceed with deployment? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled."
    exit 1
fi

# Deploy the stack
echo "🚀 Deploying stack..."
cdk deploy --require-approval never

echo "✅ Deployment completed successfully!"
echo ""
echo "📊 Stack outputs:"
cdk list

# Get stack outputs
API_ENDPOINT=$(aws cloudformation describe-stacks --stack-name D2GStack --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' --output text)
USER_POOL_ID=$(aws cloudformation describe-stacks --stack-name D2GStack --query 'Stacks[0].Outputs[?OutputKey==`UserPoolId`].OutputValue' --output text)

echo ""
echo "🔧 Initializing schemas..."
export SCHEMAS_TABLE="d2g-form-schemas"
python init_schema.py

echo ""
echo "👥 Setting up admin user..."
read -p "🤔 Do you want to create the first admin user now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    export USER_POOL_ID=$USER_POOL_ID
    python create_admin.py
fi

echo ""
echo "🔗 Next steps:"
echo "1. Verify your SES email identity in the AWS Console"
echo "2. Update CORS origins in the stack for production"
echo "3. Test the API endpoints:"
echo "   - Main form: GET $API_ENDPOINT/schema?formId=dock2gdansk-main"
echo "   - Submit form: POST $API_ENDPOINT/submit-form"
echo "   - Admin dashboard: $API_ENDPOINT/kapitanat/dashboard (requires auth)"
echo ""
echo "📚 For more information, see README.md"
