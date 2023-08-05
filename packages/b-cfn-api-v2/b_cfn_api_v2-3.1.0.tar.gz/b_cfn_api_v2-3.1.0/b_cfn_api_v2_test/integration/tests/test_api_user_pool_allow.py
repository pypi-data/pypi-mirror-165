import urllib3
from urllib3 import HTTPResponse

from b_cfn_api_v2_test.integration.infrastructure.main_stack import MainStack


def test_RESOURCE_api_WITH_valid_access_token_EXPECT_request_successful(access_token: str) -> None:
    """
    Tests whether the API works as expected.

    :param access_token: Access token to prove identity.

    :return: No return.
    """
    endpoint = MainStack.get_output(MainStack.USER_POOL_ENDPOINT_KEY)

    http = urllib3.PoolManager()

    response: HTTPResponse = http.request(
        method='GET',
        url=endpoint,
        headers={
            'Authorization': access_token
        },
    )

    assert response.status == 200

    data = response.data
    data = data.decode()
    # Response from a dummy lambda function defined in the infrastructure main stack.
    assert data == 'Hello World!'
