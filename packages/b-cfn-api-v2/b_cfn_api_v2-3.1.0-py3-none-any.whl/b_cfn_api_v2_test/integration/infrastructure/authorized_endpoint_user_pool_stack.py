from aws_cdk.aws_apigatewayv2 import CfnRoute
from aws_cdk.aws_lambda import Function, Code, Runtime, CfnPermission
from aws_cdk.core import Stack, Duration
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack
from b_cfn_lambda_integration.lambda_integration import LambdaIntegration

from b_cfn_api_v2.api import Api


class AuthorizedEndpointUserPoolStack(Stack):
    def __init__(self, scope: Stack, api: Api):
        super().__init__(
            scope=scope,
            id='UserPoolAuthorizedEndpointStack'
        )

        prefix = TestingStack.global_prefix()

        self.api_endpoint_function = Function(
            scope=self,
            id='ApiFunction1',
            function_name=f'{prefix}ApiFunction1',
            code=Code.from_inline(
                'def handler(event, context):\n'
                '    print(event)\n'
                '    return {\n'
                '        "statusCode": 200,\n'
                '        "headers": {},\n'
                '        "body": "Hello World!",\n'
                '        "isBase64Encoded": False'
                '    }'
            ),
            handler='index.handler',
            runtime=Runtime.PYTHON_3_7,
            memory_size=128,
            timeout=Duration.seconds(30),
        )

        CfnPermission(
            scope=self,
            id=f'{prefix}InvokePermission',
            action='lambda:InvokeFunction',
            function_name=self.api_endpoint_function.function_name,
            principal='apigateway.amazonaws.com',
        )

        self.integration = LambdaIntegration(
            scope=self,
            api=api,
            integration_name=f'{prefix}Integration1',
            lambda_function=self.api_endpoint_function
        )

        self.route = CfnRoute(
            scope=self,
            id='DummyRoute',
            api_id=api.ref,
            route_key=f'GET /dummy1',
            authorization_type='CUSTOM',
            target=f'integrations/{self.integration.ref}',
            authorizer_id=api.authorizer.ref
        )
