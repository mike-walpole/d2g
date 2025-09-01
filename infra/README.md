# Dock2Gdansk AWS Infrastructure

This directory contains the AWS CDK infrastructure for the Dock2Gdansk project, deployed in the Hong Kong region (ap-east-1).

## Architecture

The infrastructure includes:

- **DynamoDB**: 
  - `d2g-form-submissions`: Table for storing form submissions
  - `d2g-form-schemas`: Table for storing form schemas with versioning and cargo types
- **Cognito**: User authentication with admin group for kapitanat dashboard
- **SES**: Email service for notifications
- **API Gateway**: HTTP API for form submission, schema management, and admin dashboard
- **Lambda Functions**: 
  - `submit_form`: Handles form submissions and stores data in DynamoDB
  - `get_schema`: Returns form schema from DynamoDB
  - `manage_schema`: CRUD operations for form schemas with versioning
  - `admin_kapitanat`: Protected admin dashboard for managing forms, submissions, and users

## Prerequisites

1. **AWS CLI** installed and configured
2. **Python 3.8+** installed
3. **AWS CDK CLI** installed globally: `npm install -g aws-cdk`
4. **AWS Account** with appropriate permissions

## Setup

1. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS credentials** (if not already done):
   ```bash
   aws configure
   ```

4. **Set your AWS account ID** in the context:
   ```bash
   cdk context --set account YOUR_AWS_ACCOUNT_ID
   ```

## Deployment

1. **Bootstrap CDK** (first time only):
   ```bash
   cdk bootstrap
   ```

2. **Deploy the stack**:
   ```bash
   cdk deploy
   ```

3. **Initialize default schema** (after deployment):
   ```bash
   python init_schema.py
   ```

4. **To destroy the stack**:
   ```bash
   cdk destroy
   ```

## Configuration

### SES Email Identity

Before using SES, you need to verify your email domain or email address:

1. Go to AWS SES Console
2. Navigate to "Verified identities"
3. Add and verify your domain or email address
4. Update the email address in `d2g_stack.py` if needed

### CORS Configuration

The API Gateway is configured with CORS enabled for all origins (`*`). For production, update the `allow_origins` in `d2g_stack.py` to include only your specific domains.

## API Endpoints

After deployment, you'll get the following endpoints:

### Public Endpoints
- **POST** `/submit-form` - Submit form data
- **GET** `/schema` - Get form schema (default: dock2gdansk-main form)

### Schema Management (Public)
- **GET** `/manage-schema` - Get schema versions 
- **POST** `/manage-schema` - Create new schema version
- **PUT** `/manage-schema` - Update existing schema
- **DELETE** `/manage-schema` - Delete schema version

### Admin Endpoints (Protected - Requires Cognito Auth)
- **GET** `/kapitanat/dashboard` - Admin dashboard overview
- **GET** `/kapitanat/submissions` - View form submissions
- **DELETE** `/kapitanat/submissions` - Delete submissions
- **GET** `/kapitanat/team-members` - Manage team members
- **POST** `/kapitanat/team-members` - Add team members
- **DELETE** `/kapitanat/team-members` - Remove team members
- **GET** `/kapitanat/cargo-types` - Manage cargo types
- **POST** `/kapitanat/cargo-types` - Add cargo types
- **PUT** `/kapitanat/cargo-types` - Update cargo types
- **GET** `/kapitanat/schemas` - List all schema versions
- **GET** `/kapitanat/schemas?formId=X` - Get versions for specific form
- **POST** `/kapitanat/schemas` - Create new schema version
- **PUT** `/kapitanat/schemas` - Update existing schema version
- **DELETE** `/kapitanat/schemas?formId=X&version=Y` - Delete schema version

### Usage Examples

#### Form Submission with Schema Version Tracking
```javascript
const response = await fetch('YOUR_API_ENDPOINT/submit-form', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    formData: {
      company: 'ABC Logistics',
      email: 'contact@abc-logistics.com',
      phone_prefix: '+86',
      phone: '13712345678',
      cargo_type: '100', // Foodstuff
      inquiry_content: 'I need to ship containers from Shanghai to Gdansk...',
      privacy_consent: true,
      terms_consent: true,
      cross_border_consent: true
    },
    userEmail: 'contact@abc-logistics.com',
    formId: 'dock2gdansk-main',        // Optional - defaults to dock2gdansk-main
    schemaVersion: '1.2.0'             // Optional - auto-detected if not provided
  })
});

// Response includes submission with schema version tracking
const result = await response.json();
// {
//   "success": true,
//   "submissionId": "uuid",
//   "message": "Form submitted successfully",
//   "schemaVersion": "1.2.0",
//   "formId": "dock2gdansk-main"
// }
```

#### Get Form Schema
```javascript
// Get latest Dock2Gdansk form schema
const response = await fetch('YOUR_API_ENDPOINT/schema?formId=dock2gdansk-main');
const { schema, metadata } = await response.json();
```

#### Admin Dashboard (Requires Authentication)
```javascript
// Login first to get JWT token
const authResponse = await fetch('YOUR_API_ENDPOINT/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'admin@dock2gdansk.com', password: 'password' })
});
const { token } = await authResponse.json();

// Access admin dashboard
const dashboardResponse = await fetch('YOUR_API_ENDPOINT/kapitanat/dashboard', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const dashboard = await dashboardResponse.json();

// Manage cargo types
const newCargoType = await fetch('YOUR_API_ENDPOINT/kapitanat/cargo-types', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ name: 'New Cargo Type' })
});

// Admin Schema Management with Version Control
// List all schema versions
const schemasResponse = await fetch('YOUR_API_ENDPOINT/kapitanat/schemas', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const { schemas } = await schemasResponse.json();

// Get specific form versions
const formVersions = await fetch('YOUR_API_ENDPOINT/kapitanat/schemas?formId=dock2gdansk-main', {
  headers: { 'Authorization': `Bearer ${token}` }
});

// Create new schema version (auto-increments version)
const newSchemaVersion = await fetch('YOUR_API_ENDPOINT/kapitanat/schemas', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    formId: 'dock2gdansk-main',
    description: 'Added new field for delivery date',
    schema: {
      title: 'Updated Dock2Gdansk Form',
      fields: [
        // ... existing fields ...
        {
          id: 'delivery_date',
          type: 'date',
          label: 'Preferred Delivery Date',
          required: false
        }
      ]
    }
  })
});
// Creates version 1.1.0 automatically

// Update existing schema version
const updateSchema = await fetch('YOUR_API_ENDPOINT/kapitanat/schemas', {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    formId: 'dock2gdansk-main',
    version: '1.1.0',
    isActive: false,  // Deactivate this version
    description: 'Deprecated - use v1.2.0 instead'
  })
});
```

## Environment Variables

The Lambda functions use the following environment variables:

- `DYNAMODB_TABLE`: DynamoDB table name for form submissions
- `SCHEMAS_TABLE`: DynamoDB table name for form schemas
- `USER_POOL_ID`: Cognito User Pool ID
- `USER_POOL_CLIENT_ID`: Cognito User Pool Client ID
- `SES_IDENTITY`: SES email identity

## Security

- DynamoDB table has point-in-time recovery enabled
- Lambda functions have minimal required permissions
- API Gateway has CORS configured
- Cognito provides user authentication

## Monitoring

- CloudWatch logs are automatically created for Lambda functions
- DynamoDB metrics are available in CloudWatch
- API Gateway provides request/response metrics

## Cost Optimization

- DynamoDB uses on-demand billing (pay-per-request)
- Lambda functions have 30-second timeout and 256MB memory
- Consider using provisioned capacity for DynamoDB if you have predictable traffic

## Troubleshooting

### Common Issues

1. **SES not in production mode**: New SES accounts are in sandbox mode. Request production access if needed.

2. **CORS errors**: Ensure your frontend domain is included in the CORS configuration.

3. **Lambda timeout**: Increase the timeout in the stack if needed.

4. **Permission errors**: Ensure your AWS credentials have the necessary permissions.

### Useful Commands

```bash
# View stack outputs
cdk list

# View stack details
cdk diff

# View CloudFormation template
cdk synth

# View logs
aws logs tail /aws/lambda/d2g-submit-form --follow
aws logs tail /aws/lambda/d2g-get-schema --follow
```

## Development

To make changes to the infrastructure:

1. Modify the CDK code in `d2g_stack.py`
2. Update Lambda function code in the `lambda/` directory
3. Run `cdk diff` to see what will change
4. Run `cdk deploy` to apply changes

## Production Considerations

Before deploying to production:

1. Change `RemovalPolicy.DESTROY` to `RemovalPolicy.RETAIN` for critical resources
2. Configure proper CORS origins
3. Set up CloudWatch alarms
4. Configure SES for production use
5. Set up proper IAM roles and policies
6. Consider using AWS Secrets Manager for sensitive configuration
