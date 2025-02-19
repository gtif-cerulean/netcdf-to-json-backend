import pytest
from fastapi.testclient import TestClient

from netcdf_to_json_backend.app import app


@pytest.fixture()
def client():
    return TestClient(app)
