from pathlib import Path
from urllib.request import Request
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

app = FastAPI()

current_dir = Path(__file__).parent


class HTTPMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        return await call_next(request)


# for _ in range(5):
app.add_middleware(HTTPMiddleware)




@app.get("/")
def read_root():
    return {"Hello": "World"}
