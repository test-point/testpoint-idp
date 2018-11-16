#!/bin/bash
export PYTHONPATH="/code:${PYTHONPATH}"
cd /code/src
gunicorn idp_core.wsgi:application --workers=4 -b 0.0.0.0:8080
