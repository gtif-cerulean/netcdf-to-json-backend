# build is docker compose build
all:
	docker compose run --user `id -u` netcdf-to-json-backend bash -c "ruff format . && pytest && ruff check . && mypy ."

test:
	docker compose run --user `id -u` netcdf-to-json-backend python3 -m pytest -s

test-watch:
	docker compose run --user `id -u` netcdf-to-json-backend ptw

lint:
	docker compose run --user `id -u` netcdf-to-json-backend bash -c "ruff format . && ruff check . && mypy ."

lint-watch:
	docker compose run --user `id -u` netcdf-to-json-backend bash -c "watch -n1 bash -c \"'ruff format . && ruff check . && mypy .'\""

upgrade-packages:
	docker compose run --user 0 netcdf-to-json-backend bash -c "python3 -m pip install pip-upgrader setuptools && pip-upgrade --skip-package-installation"

bash:
	docker compose run --user `id -u` netcdf-to-json-backend bash

up:
	docker compose up

build:
	docker compose build
