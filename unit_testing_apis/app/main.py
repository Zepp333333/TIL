from http.client import HTTPException
from typing import Literal

import fastapi
from fastapi import Body, HTTPException
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from unit_testing_apis.app.examples.input_bodies import (
    SLEEP_INPUT_EXAMPLE,
    WORKOUT_INPUT_EXAMPLE,
)
from unit_testing_apis.app.examples.responses import (
    AUTH_HEADER_INVALID_RESPONSE_EXAMPLE,
    AUTH_HEADER_MISSING_RESPONSE_EXAMPLE,
    RATE_LIMIT_EXCEEDED_RESPONSE_EXAMPLE,
    RESPONSE_EXAMPLES, SUCCESS_RESPONSE_EXAMPLE,
)
from unit_testing_apis.app.settings import get_settings

app = fastapi.FastAPI()


class SleepInputSchema(BaseModel):
    record_class: Literal["sleep"] = "sleep"
    record_id: int # for the sake of example
    content: dict

    model_config = {"json_schema_extra": {"examples": [SLEEP_INPUT_EXAMPLE]}}


class WorkoutInputSchema(BaseModel):
    record_class: Literal["workout"] = "workout"
    record_id: int # for the sake of example
    content: dict

    model_config = {"json_schema_extra": {"examples": [WORKOUT_INPUT_EXAMPLE]}}


class SuccessResponseSchema(BaseModel):
    success: bool = True
    model_config = {"json_schema_extra": {"examples": [SUCCESS_RESPONSE_EXAMPLE]}}

@app.post(
    "/record/",
    status_code=status.HTTP_202_ACCEPTED,
    responses=RESPONSE_EXAMPLES,
)
def post_record(
    request: Request,
    response: Response,
    payload: SleepInputSchema | WorkoutInputSchema = Body(...),
) -> SuccessResponseSchema:
    # Simulate a rate limit. Will raise 429 HTTPException
    raise_on_rate_limit_exceeded(request)

    # Simulate auth check
    # Will raise HTTPException with different body depending on whether the header is missing or or secret token is invalid
    raise_on_unauthorized(request)

    # Simulate some processing
    do_something_with_payload(payload)

    # Return a success response
    response.status_code = status.HTTP_202_ACCEPTED
    return SuccessResponseSchema()


def raise_on_unauthorized(request: Request):
    forbidden_reason: dict | None = None
    if request.headers.get("my-auth-header") is None:
        forbidden_reason = AUTH_HEADER_MISSING_RESPONSE_EXAMPLE
    elif request.headers.get("my-auth-header") != get_settings().SECRET_TOKEN:
        forbidden_reason = AUTH_HEADER_INVALID_RESPONSE_EXAMPLE

    if forbidden_reason:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=forbidden_reason["detail"]
        )


def do_something_with_payload(_payload) -> None:
    pass


def raise_on_rate_limit_exceeded(request: Request):
    if request.headers.get("X-RateLimit-Remaining") == "0":
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=RATE_LIMIT_EXCEEDED_RESPONSE_EXAMPLE["detail"],
        )
