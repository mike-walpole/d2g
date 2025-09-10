from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_cognito as cognito,
    aws_ses as ses,
    aws_apigatewayv2 as apigatewayv2,
    aws_apigatewayv2_integrations as apigatewayv2_integrations,
    aws_lambda as lambda_,
    aws_iam as iam,
    Duration,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct

class D2GStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table for form submissions
        self.form_submissions_table = dynamodb.Table(
            self, "FormSubmissionsTable",
            table_name="d2g-form-submissions",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,  # For development - change to RETAIN for production
            point_in_time_recovery=True
        )

        # DynamoDB Table for form schemas with versioning
        self.form_schemas_table = dynamodb.Table(
            self, "FormSchemasTable",
            table_name="d2g-form-schemas",
            partition_key=dynamodb.Attribute(
                name="formId",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="version",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,  # For development - change to RETAIN for production
            point_in_time_recovery=True
        )

        # Cognito User Pool
        self.user_pool = cognito.UserPool(
            self, "D2GUserPool",
            user_pool_name="d2g-user-pool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(
                email=True
            ),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(
                    required=True,
                    mutable=True
                )
            ),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=True
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            removal_policy=RemovalPolicy.DESTROY
        )

        # Cognito User Pool Client
        self.user_pool_client = cognito.UserPoolClient(
            self, "D2GUserPoolClient",
            user_pool=self.user_pool,
            user_pool_client_name="d2g-client",
            generate_secret=False,
            auth_flows=cognito.AuthFlow(
                user_password=True,
                user_srp=True,
                admin_user_password=True
            ),
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    implicit_code_grant=True
                ),
                scopes=[cognito.OAuthScope.OPENID, cognito.OAuthScope.EMAIL]
            )
        )

        # Cognito Admin Group
        self.admin_group = cognito.CfnUserPoolGroup(
            self, "AdminGroup",
            user_pool_id=self.user_pool.user_pool_id,
            group_name="admin",
            description="Administrators with access to kapitanat dashboard"
        )

        # SES Configuration (for email notifications)
        # Note: SES in Hong Kong region may have limited features
        # For now, we'll skip SES setup and configure it manually in the console
        # Alternatively, we can use a different region for SES
        # self.ses_identity = ses.EmailIdentity(
        #     self, "D2GSESIdentity",
        #     identity=ses.Identity.email("noreply@dock2gdansk.com")
        # )
        self.ses_email = "michal@dagodigital.com"  # Will need manual verification

        # Lambda function to handle form submissions
        self.submit_form_lambda = lambda_.Function(
            self, "SubmitFormLambda",
            function_name="d2g-submit-form",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="submit_form.handler",
            code=lambda_.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            memory_size=256,
            environment={
                "DYNAMODB_TABLE": self.form_submissions_table.table_name,
                "SCHEMAS_TABLE": self.form_schemas_table.table_name,
                "USER_POOL_ID": self.user_pool.user_pool_id,
                "USER_POOL_CLIENT_ID": self.user_pool_client.user_pool_client_id
            }
        )

        # Lambda function to get form schema
        self.get_schema_lambda = lambda_.Function(
            self, "GetSchemaLambda",
            function_name="d2g-get-schema",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="get_schema.handler",
            code=lambda_.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            memory_size=256,
            environment={
                "DYNAMODB_TABLE": self.form_submissions_table.table_name,
                "SCHEMAS_TABLE": self.form_schemas_table.table_name
            }
        )

        # Lambda function to get config (translations, cargo types)
        self.get_config_lambda = lambda_.Function(
            self, "GetConfigLambda",
            function_name="d2g-get-config",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="get_config.handler",
            code=lambda_.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            memory_size=256,
            environment={
                "SCHEMAS_TABLE": self.form_schemas_table.table_name
            }
        )

        # Lambda function to manage form schemas (CRUD operations)
        self.manage_schema_lambda = lambda_.Function(
            self, "ManageSchemaLambda",
            function_name="d2g-manage-schema",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="manage_schema.handler",
            code=lambda_.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            memory_size=256,
            environment={
                "SCHEMAS_TABLE": self.form_schemas_table.table_name
            }
        )

        # Lambda function for admin kapitanat dashboard
        self.admin_kapitanat_lambda = lambda_.Function(
            self, "AdminKapitanatLambda",
            function_name="d2g-admin-kapitanat",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="admin_kapitanat.handler",
            code=lambda_.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            memory_size=512,  # More memory for admin operations
            environment={
                "DYNAMODB_TABLE": self.form_submissions_table.table_name,
                "SCHEMAS_TABLE": self.form_schemas_table.table_name,
                "USER_POOL_ID": self.user_pool.user_pool_id,
                "USER_POOL_CLIENT_ID": self.user_pool_client.user_pool_client_id
            }
        )

        # Grant permissions to Lambda functions
        self.form_submissions_table.grant_write_data(self.submit_form_lambda)
        self.form_schemas_table.grant_read_data(self.submit_form_lambda)  # For schema version lookup
        self.form_submissions_table.grant_read_data(self.get_schema_lambda)
        self.form_schemas_table.grant_read_data(self.get_schema_lambda)
        self.form_schemas_table.grant_read_data(self.get_config_lambda)  # For config data
        self.form_schemas_table.grant_full_access(self.manage_schema_lambda)
        
        # Admin Lambda permissions
        self.form_submissions_table.grant_full_access(self.admin_kapitanat_lambda)
        self.form_schemas_table.grant_full_access(self.admin_kapitanat_lambda)

        # Note: Removed SES permissions since we're now using Resend for email

        # Grant Cognito permissions to admin lambda
        self.admin_kapitanat_lambda.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "cognito-idp:GetUser",
                    "cognito-idp:ListUsers",
                    "cognito-idp:AdminListGroupsForUser",
                    "cognito-idp:AdminCreateUser",
                    "cognito-idp:AdminDeleteUser",
                    "cognito-idp:AdminAddUserToGroup",
                    "cognito-idp:AdminRemoveUserFromGroup"
                ],
                resources=[self.user_pool.user_pool_arn]
            )
        )
        
# Note: Submit form lambda no longer needs Cognito permissions - it uses Analysis Email Recipients from DynamoDB

        # HTTP API Gateway
        self.api = apigatewayv2.HttpApi(
            self, "D2GHttpApi",
            api_name="d2g-api",
            cors_preflight=apigatewayv2.CorsPreflightOptions(
                allow_headers=["Content-Type", "Authorization"],
                allow_methods=[apigatewayv2.CorsHttpMethod.ANY],
                allow_origins=["*"],  # Configure appropriately for production
                max_age=Duration.days(1)
            )
        )

        # API Gateway integrations
        submit_form_integration = apigatewayv2_integrations.HttpLambdaIntegration(
            "SubmitFormIntegration",
            self.submit_form_lambda
        )

        get_schema_integration = apigatewayv2_integrations.HttpLambdaIntegration(
            "GetSchemaIntegration",
            self.get_schema_lambda
        )

        get_config_integration = apigatewayv2_integrations.HttpLambdaIntegration(
            "GetConfigIntegration",
            self.get_config_lambda
        )

        manage_schema_integration = apigatewayv2_integrations.HttpLambdaIntegration(
            "ManageSchemaIntegration",
            self.manage_schema_lambda
        )

        admin_kapitanat_integration = apigatewayv2_integrations.HttpLambdaIntegration(
            "AdminKapitanatIntegration",
            self.admin_kapitanat_lambda
        )

        # API Gateway routes
        self.api.add_routes(
            path="/submit-form",
            methods=[apigatewayv2.HttpMethod.POST],
            integration=submit_form_integration
        )

        self.api.add_routes(
            path="/schema",
            methods=[apigatewayv2.HttpMethod.GET],
            integration=get_schema_integration
        )

        self.api.add_routes(
            path="/config",
            methods=[apigatewayv2.HttpMethod.GET],
            integration=get_config_integration
        )

        self.api.add_routes(
            path="/manage-schema",
            methods=[
                apigatewayv2.HttpMethod.GET,
                apigatewayv2.HttpMethod.POST,
                apigatewayv2.HttpMethod.PUT,
                apigatewayv2.HttpMethod.DELETE
            ],
            integration=manage_schema_integration
        )

        # Admin kapitanat routes (protected)
        self.api.add_routes(
            path="/kapitanat/{proxy+}",
            methods=[
                apigatewayv2.HttpMethod.GET,
                apigatewayv2.HttpMethod.POST,
                apigatewayv2.HttpMethod.PUT,
                apigatewayv2.HttpMethod.DELETE
            ],
            integration=admin_kapitanat_integration
        )

        # Outputs
        CfnOutput(
            self, "ApiEndpoint",
            value=self.api.api_endpoint,
            description="API Gateway endpoint"
        )

        CfnOutput(
            self, "UserPoolId",
            value=self.user_pool.user_pool_id,
            description="Cognito User Pool ID"
        )

        CfnOutput(
            self, "UserPoolClientId",
            value=self.user_pool_client.user_pool_client_id,
            description="Cognito User Pool Client ID"
        )

        CfnOutput(
            self, "DynamoDBTableName",
            value=self.form_submissions_table.table_name,
            description="DynamoDB table name"
        )

        CfnOutput(
            self, "SchemasTableName",
            value=self.form_schemas_table.table_name,
            description="DynamoDB schemas table name"
        )
