from http import HTTPStatus
from pathlib import Path

import pytest
import respx

from netcdf_to_json_backend import config


@pytest.fixture()
def mock_data_source(respx_mock: respx.MockRouter) -> None:
    content = (Path(__file__).parent / "example.nc").read_bytes()
    respx_mock.get(f"{config.settings.base_url}/a/b.nc").respond(content=content)

    respx_mock.get(f"{config.settings.base_url}/a/not-found").respond(
        status_code=HTTPStatus.NOT_FOUND
    )


def test_landing_page_loads(client):
    response = client.get("/")
    assert response.json() == {}


def test_data_returns_data(client, mock_data_source):
    response = client.get("/data/a/b.nc")
    assert response.json()["data"][2] == {
        "type": "a",
        "time": 17531,
        "siextentn_min": 5.113038063049316,
        "siextentn_max": 12.644613265991211,
    }


def test_data_fills_missing_values_with_none(client, mock_data_source):
    response = client.get("/data/a/b.nc")

    assert response.json()["data"][9]["type"] is None


def test_data_forwards_not_found(client, mock_data_source):
    response = client.get("/data/a/not-found")
    assert response.status_code == HTTPStatus.NOT_FOUND
