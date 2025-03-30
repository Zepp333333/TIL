import os

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient


@pytest.fixture()
def test_client(test_app: FastAPI):
    with TestClient(test_app) as c:
        yield c


@pytest.fixture()
def test_app(set_default_environ):
    from ..main import app  # relative import for the sake the example

    yield app


@pytest.fixture(autouse=True, scope="session")
def set_default_environ():
    os.environ["SECRET_TOKEN"] = "secret_1"
