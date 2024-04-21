from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_middleware.main import app
from concurrent.futures import ThreadPoolExecutor

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_concurrent_requests():
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(test_read_root) for _ in range(1000)}
        for future in futures:
            # If the function call raised an exception, this will re-raise that exception
            future.result()
