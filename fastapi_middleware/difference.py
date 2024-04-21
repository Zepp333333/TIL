import asyncio

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

app = FastAPI()


class HTTPMiddleware:
    async def __call__(self, request: Request, call_next):
        await asyncio.sleep(0.1)
        return await call_next(request)


# BaseHTTPMiddleware with simulated delay
async def custom_basehttp_middleware(request: Request, call_next):
    # Simulated processing delay
    await asyncio.sleep(0.1)
    return await call_next(request)


# Example of an ASGIMiddleware
class CustomASGIMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Asynchronous processing (non-blocking)
        await asyncio.sleep(0.1)  # Non-blocking sleep
        await self.app(scope, receive, send)


for _ in range(10):
    app.add_middleware(BaseHTTPMiddleware, dispatch=HTTPMiddleware())
#
#
# for _ in range(10):
#     app.add_middleware(BaseHTTPMiddleware, dispatch=custom_basehttp_middleware)


# for _ in range(10):
#     app.add_middleware(CustomASGIMiddleware)


@app.get("/")
def read_root():
    return {"Hello": "World"}
