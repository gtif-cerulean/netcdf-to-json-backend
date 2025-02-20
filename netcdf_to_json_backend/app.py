import logging
from itertools import zip_longest

import httpx
import netCDF4
from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics

from netcdf_to_json_backend import config

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)


@app.get("/")
async def landing_page():
    return {}


@app.get("/healthz")
def healthz():
    return {"message": "All is OK!"}


DATA_SOURCE = "https://thredds.met.no/thredds/fileServer/metusers/steingod/deside/climmodseaice-yearlymaxmin/siextentn/MIROC6_sea_ice/Daily/ssp460/siextentn_SIday_MIROC6_ssp460_r1i1p1f1_2015-2100.nc"


@app.get("/data/{path:path}")
async def le_data(path: str):
    # not sure if we need more validation, at least escaping from the domain
    # should (tm) not be possible
    url = f"{config.settings.base_url}/{path}"

    logger.info(f"Fetching netcdf from {url}")

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    response.raise_for_status()

    ds = netCDF4.Dataset("in-mem-file", mode="r", memory=response.content)

    # extract all data so we can zip it
    data_by_var = [variable[:].tolist() for variable in ds.variables.values()]
    data = [
        # zip items back together with variable names
        dict(zip(ds.variables.keys(), data_item, strict=True))
        for data_item in zip_longest(*data_by_var, fillvalue=None)
    ]
    return {"data": data}
