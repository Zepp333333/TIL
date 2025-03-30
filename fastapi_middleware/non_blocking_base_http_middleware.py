import asyncio
from pathlib import Path
from urllib.request import Request

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware


# to_thread.current_default_thread_limiter().total_tokens = 80
app = FastAPI()

current_dir = Path(__file__).parent


class HTTPMiddleware:
    async def __call__(self, request: Request, call_next):
        await asyncio.sleep(0.1)
        return await call_next(request)


for _ in range(5):
    app.add_middleware(BaseHTTPMiddleware, dispatch=HTTPMiddleware())


@app.get("/")
def read_root():
    return {"Hello": "World"}
