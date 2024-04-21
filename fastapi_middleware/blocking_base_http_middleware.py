from pathlib import Path
from urllib.request import Request
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

current_dir = Path(__file__).parent

class HTTPMiddleware:
    async def __call__(self, request: Request, call_next):
        with open('/tmp/middleware.log', 'a') as f:
            f.write('HTTPMiddleware\n' * 1000)
        return await call_next(request)


for _ in range(5):
    app.add_middleware(BaseHTTPMiddleware, dispatch=HTTPMiddleware())


@app.get("/")
def read_root():
    return {"Hello": "World"}
