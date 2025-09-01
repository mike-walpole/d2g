#!/usr/bin/env python3
import aws_cdk as cdk
from d2g_stack import D2GStack

app = cdk.App()
D2GStack(app, "D2GStack",
    env=cdk.Environment(
        account=app.node.try_get_context('account'),
        region='ap-east-1'  # Hong Kong region
    ),
    description="Dock2Gdansk infrastructure with DynamoDB, Cognito, SES, API Gateway, and Lambdas"
)

app.synth()
