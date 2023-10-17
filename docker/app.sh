#!/bin/bash

alembic upgrade head

gunicorn executor:fastapi_application --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
