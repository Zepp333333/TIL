SUCCESS_RESPONSE_EXAMPLE = {"success": True}

RATE_LIMIT_EXCEEDED_RESPONSE_EXAMPLE = {
    "detail": [
        {
            "loc": ["rate_limiter"],
            "msg": "Retry in 15 minutes",
            "type": "rate_limit_exceeded",
        }
    ]
}


AUTH_HEADER_MISSING_RESPONSE_EXAMPLE = {
    "detail": [
        {
            "loc": ["header", "my-auth-header"],
            "msg": "Header is required",
            "type": "missing_header",
        }
    ]
}

AUTH_HEADER_INVALID_RESPONSE_EXAMPLE = {
    "detail": [
        {
            "loc": ["header", "my-auth-header"],
            "msg": "Header value is invalid",
            "type": "invalid_auth_header_value",
        }
    ]
}


RESPONSE_EXAMPLES = {
    202: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "success": {"value": SUCCESS_RESPONSE_EXAMPLE},
                }
            }
        },
    },
    403: {
        "description": "Failure",
        "content": {
            "application/json": {
                "examples": {
                    "auth_header_missing": {
                        "value": AUTH_HEADER_MISSING_RESPONSE_EXAMPLE
                    },
                    "auth_header_invalid": {
                        "value": AUTH_HEADER_INVALID_RESPONSE_EXAMPLE
                    },
                },
            }
        },
    },
    429: {
        "description": "Rate limit exceeded",
        "content": {
            "application/json": {
                "examples": {
                    "rate_limit_exceeded": {
                        "value": RATE_LIMIT_EXCEEDED_RESPONSE_EXAMPLE
                    }
                },
            }
        },
    },
}
