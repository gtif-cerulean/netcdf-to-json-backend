import logging

from fastapi import FastAPI, Request
from starlette_exporter import PrometheusMiddleware, handle_metrics

logging.basicConfig(level=logging.INFO)


app = FastAPI()

# app.add_middleware(RequestIdLoggingMiddleware)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)


@app.get("/")
async def landing_page(request: Request):
    return {}


@app.get("/healthz")
def healthz():
    return {"message": "All is OK!"}
