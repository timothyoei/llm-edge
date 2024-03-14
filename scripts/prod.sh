#!/bin/bash

# Start API
micromamba activate && micromamba activate venv && gunicorn -w 4 -b 0.0.0.0:8000 --chdir src/server 'server:app' &

# Start UI
cd src/client && npm run start &