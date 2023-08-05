from aws_cdk.aws_apigatewayv2 import CfnApi
from aws_cdk.core import Construct
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack
from b_cfn_custom_userpool_authorizer.config.user_pool_ssm_config import UserPoolSsmConfig

from b_cfn_api_v2.api import Api
from b_cfn_api_v2_test.integration.infrastructure.authorized_endpoint_api_key_stack import AuthorizedEndpointApiKeyStack
from b_cfn_api_v2_test.integration.infrastructure.authorized_endpoint_user_pool_stack import \
    AuthorizedEndpointUserPoolStack
from b_cfn_api_v2_test.integration.infrastructure.user_pool_stack import UserPoolStack


class MainStack(TestingStack):
    USER_POOL_ENDPOINT_KEY = 'UserPoolEndpoint'
    API_KEY_ENDPOINT_KEY = 'ApiKeyEndpoint'
    USER_POOL_ID_KEY = 'UserPoolId'
    USER_POOL_CLIENT_ID_KEY = 'UserPoolClientId'
    API_KEYS_GENERATOR_FUNCTION_KEY = 'ApiKeysGeneratorFunction'

    def __init__(self, scope: Construct) -> None:
        super().__init__(scope=scope)

        prefix = TestingStack.global_prefix()

        self.user_pool_stack = UserPoolStack(self)

        self.api = Api(
            scope=self,
            id='Api',
            name=f'{prefix}Api',
            description='Sample description.',
            protocol_type='HTTP',
            cors_configuration=CfnApi.CorsProperty(
                allow_methods=['GET', 'PUT', 'POST', 'OPTIONS', 'DELETE'],
                allow_origins=['*'],
                allow_headers=[
                    'Content-Type',
                    'Authorization'
                ],
                max_age=300
            )
        )

        self.api.enable_api_key_authorizer()
        self.api.enable_authorizer(UserPoolSsmConfig(
            user_pool_id_ssm_key=self.user_pool_stack.ssm_pool_id.parameter_name,
            user_pool_client_id_ssm_key=self.user_pool_stack.ssm_pool_client_id.parameter_name,
            user_pool_region_ssm_key=self.user_pool_stack.ssm_pool_region.parameter_name,
        ), cache_ttl=0)

        self.api.enable_default_stage('test', enable_logging=True)

        AuthorizedEndpointApiKeyStack(self, self.api)
        AuthorizedEndpointUserPoolStack(self, self.api)

        self.add_output(self.USER_POOL_ENDPOINT_KEY, value=f'{self.api.full_url}/dummy1')
        self.add_output(self.API_KEY_ENDPOINT_KEY, value=f'{self.api.full_url}/dummy2')
        self.add_output(self.USER_POOL_ID_KEY, value=self.user_pool_stack.pool.user_pool_id)
        self.add_output(self.USER_POOL_CLIENT_ID_KEY, value=self.user_pool_stack.client.user_pool_client_id)
        self.add_output(self.API_KEYS_GENERATOR_FUNCTION_KEY, value=self.api.api_key_authorizer.generator_function.function_name)
