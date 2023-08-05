import urllib3
from urllib3 import HTTPResponse

from b_cfn_api_v2_test.integration.infrastructure.main_stack import MainStack


def test_RESOURCE_api_WITH_valid_api_keys_EXPECT_request_successful(api_keys) -> None:
    """
    Tests whether the API works as expected.

    :param access_token: Access token to prove identity.

    :return: No return.
    """
    api_key, api_secret = api_keys

    endpoint = MainStack.get_output(MainStack.API_KEY_ENDPOINT_KEY)

    http = urllib3.PoolManager()

    response: HTTPResponse = http.request(
        method='GET',
        url=endpoint,
        headers={
            'ApiKey': api_key,
            'ApiSecret': api_secret
        },
    )

    assert response.status == 200

    data = response.data
    data = data.decode()
    # Response from a dummy lambda function defined in the infrastructure main stack.
    assert data == 'Hello World!'
