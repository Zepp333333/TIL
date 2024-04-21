import asyncio

from fastapi import FastAPI
from starlette.types import ASGIApp, Send, Scope, Receive

app = FastAPI()


class ASGIMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        await asyncio.sleep(0.1)
        await self.app(scope, receive, send)


for _ in range(5):
    app.add_middleware(ASGIMiddleware)


@app.get("/")
def read_root():
    return {"Hello": "World"}
