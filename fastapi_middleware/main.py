import asyncio
import time
from pathlib import Path
from urllib.request import Request
from fastapi import FastAPI
from pyinstrument import Profiler
from pyinstrument.renderers import HTMLRenderer, SpeedscopeRenderer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Send, Scope, Receive, Message

app = FastAPI()

current_dir = Path(__file__).parent


def register_profiling_middleware(app: FastAPI):
    @app.middleware("http")
    async def profile_request(request: Request, call_next):
        """Profile the current request

        Taken from https://pyinstrument.readthedocs.io/en/latest/guide.html#profile-a-web-request-in-fastapi
        with slight improvements.

        """
        profile_type_to_ext = {"html": "html", "speedscope": "speedscope.json"}
        profile_type_to_renderer = {
            "html": HTMLRenderer,
            "speedscope": SpeedscopeRenderer,
        }
        if request.query_params.get("profile", False):
            profile_type = request.query_params.get("profile_format", "speedscope")
            with Profiler(interval=0.001, async_mode="enabled") as profiler:
                response = await call_next(request)
            extension = profile_type_to_ext[profile_type]
            renderer = profile_type_to_renderer[profile_type]()
            with open(current_dir / f"../profile.{extension}", "w") as out:
                out.write(profiler.output(renderer=renderer))
            return response
        return await call_next(request)


class HTTPMiddleware:
    async def __call__(self, request: Request, call_next):
        # await asyncio.sleep(0.1)
        # print("HTTPMiddleware")
        # return await call_next(request)

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        await asyncio.sleep(0.1)
        return response


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     return await call_next(request)


class ASGIMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        # await asyncio.sleep(0.1)
        # print("ASGIMiddleware")
        # await self.app(scope, receive, send)

        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = time.time()
        response_headers = []

        async def send_wrapper(message: Message):
            nonlocal response_headers
            if message["type"] == "http.response.start":
                process_time = time.time() - start_time
                headers = [(b"x-process-time", str(process_time).encode())]
                message["headers"] = headers + message.get("headers", [])
                response_headers = headers

            await send(message)

        await asyncio.sleep(0.1)
        await self.app(scope, receive, send_wrapper)


for _ in range(5):
    app.add_middleware(BaseHTTPMiddleware, dispatch=HTTPMiddleware())


# for _ in range(10):
#     app.add_middleware(ASGIMiddleware)

# register_profiling_middleware(app)


@app.get("/")
def read_root():
    return {"Hello": "World"}
