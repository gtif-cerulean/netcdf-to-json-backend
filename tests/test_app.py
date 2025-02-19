from pathlib import Path

import pytest
import respx

from netcdf_to_json_backend.app import DATA_SOURCE


@pytest.fixture()
def mock_service_backend(respx_mock: respx.MockRouter) -> None:
    content = (Path(__file__).parent / "example.nc").read_bytes()
    respx_mock.get(DATA_SOURCE).respond(content=content)


def test_landing_page_loads(client):
    response = client.get("/")
    assert response.json() == {}


def test_data_returns_data(client, mock_service_backend):
    response = client.get("/data")
    assert response.json()["data"][2] == {
        "type": "a",
        "time": 17531,
        "siextentn_min": 5.113038063049316,
        "siextentn_max": 12.644613265991211,
    }
