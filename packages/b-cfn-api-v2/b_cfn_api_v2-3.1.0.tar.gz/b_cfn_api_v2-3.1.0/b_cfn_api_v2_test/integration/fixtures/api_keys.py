import json
from typing import Tuple

from b_aws_testing_framework.credentials import Credentials
from pytest import fixture

from b_cfn_api_v2_test.integration.infrastructure.main_stack import MainStack


@fixture(scope='function')
def api_keys() -> Tuple[str, str]:
    api_keys_generator_function = MainStack.get_output(MainStack.API_KEYS_GENERATOR_FUNCTION_KEY)

    client = Credentials().boto_session.client('lambda')
    response = client.invoke(
        FunctionName=api_keys_generator_function,
        InvocationType='RequestResponse',
    )

    response = json.loads(response['Payload'].read())
    api_key = response['ApiKey']
    api_secret = response['ApiSecret']

    return api_key, api_secret
