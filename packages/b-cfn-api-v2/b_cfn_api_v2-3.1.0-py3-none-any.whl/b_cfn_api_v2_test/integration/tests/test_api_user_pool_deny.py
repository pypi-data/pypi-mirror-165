import urllib3
from urllib3 import HTTPResponse

from b_cfn_api_v2_test.integration.infrastructure.main_stack import MainStack


def test_RESOURCE_api_WITH_no_access_token_EXPECT_request_denied() -> None:
    """
    Tests whether the API works as expected.
    Without access token request should get denied.

    :return: No return.
    """
    endpoint = MainStack.get_output(MainStack.USER_POOL_ENDPOINT_KEY)

    http = urllib3.PoolManager()

    response: HTTPResponse = http.request(
        method='GET',
        url=endpoint,
        headers={},
    )

    assert response.status == 401


def test_RESOURCE_api_WITH_invalid_access_token_EXPECT_request_denied() -> None:
    """
    Tests whether the API works as expected.
    Invalid access token should result in denied request.

    :return: No return.
    """
    endpoint = MainStack.get_output(MainStack.USER_POOL_ENDPOINT_KEY)

    http = urllib3.PoolManager()

    response: HTTPResponse = http.request(
        method='GET',
        url=endpoint,
        headers={
            'Authorization': 'aaa.bbb.ccc'
        },
    )

    assert response.status == 403
