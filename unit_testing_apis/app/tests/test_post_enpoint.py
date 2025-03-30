import pytest

from unit_testing_apis.app.examples.input_bodies import (
    WORKOUT_INPUT_EXAMPLE,
    SLEEP_INPUT_EXAMPLE,
)
from unit_testing_apis.app.examples.responses import (
    RATE_LIMIT_EXCEEDED_RESPONSE_EXAMPLE,
    AUTH_HEADER_MISSING_RESPONSE_EXAMPLE,
    AUTH_HEADER_INVALID_RESPONSE_EXAMPLE,
    SUCCESS_RESPONSE_EXAMPLE,
)


@pytest.mark.parametrize("input_payload", (SLEEP_INPUT_EXAMPLE, WORKOUT_INPUT_EXAMPLE))
def test_post_endpoint_success(input_payload, test_client):
    response = test_client.post(
        "/record/",
        json=input_payload,
        headers={"my-auth-header": "secret_1"},
    )
    assert response.status_code == 202
    assert response.json() == SUCCESS_RESPONSE_EXAMPLE


def test_post_endpoint_rate_limit_exceeded(test_client):
    response = test_client.post(
        "/record/",
        json=SLEEP_INPUT_EXAMPLE,
        headers={
            "my-auth-header": "secret_1",
            "X-RateLimit-Remaining": "0",
        },
    )
    assert response.status_code == 429
    assert response.json() == RATE_LIMIT_EXCEEDED_RESPONSE_EXAMPLE


@pytest.mark.parametrize(
    "headers, expected_response",
    [
        (
            {"my-auth-header": "wrong_value"},
            AUTH_HEADER_INVALID_RESPONSE_EXAMPLE,
        ),
        (
            {"invalid-header": "secret_1"},
            AUTH_HEADER_MISSING_RESPONSE_EXAMPLE,
        ),
    ],
)
def test_post_endpoint_forbidden(headers, expected_response, test_client):
    response = test_client.post(
        "/record/",
        json=SLEEP_INPUT_EXAMPLE,
        headers=headers,
    )
    assert response.status_code == 403
    assert response.json() == expected_response
