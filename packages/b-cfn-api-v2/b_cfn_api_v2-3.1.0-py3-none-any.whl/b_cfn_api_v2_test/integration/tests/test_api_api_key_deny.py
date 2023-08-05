import urllib3
from urllib3 import HTTPResponse

from b_cfn_api_v2_test.integration.infrastructure.main_stack import MainStack


def test_RESOURCE_api_WITH_no_api_keys_EXPECT_request_denied() -> None:
    """
    Tests whether the API works as expected.
    Without api keys request should get denied.

    :return: No return.
    """
    endpoint = MainStack.get_output(MainStack.API_KEY_ENDPOINT_KEY)

    http = urllib3.PoolManager()

    response: HTTPResponse = http.request(
        method='GET',
        url=endpoint,
        headers={},
    )

    assert response.status == 401


def test_RESOURCE_api_WITH_invalid_api_keys_EXPECT_request_denied() -> None:
    """
    Tests whether the API works as expected.
    Invalid api keys should result in denied request.

    :return: No return.
    """
    endpoint = MainStack.get_output(MainStack.API_KEY_ENDPOINT_KEY)

    http = urllib3.PoolManager()

    response: HTTPResponse = http.request(
        method='GET',
        url=endpoint,
        headers={
            'ApiKey': 'aaa.bbb.ccc',
            'ApiSecret': 'aaa.bbb.ccc'
        },
    )

    assert response.status == 403
