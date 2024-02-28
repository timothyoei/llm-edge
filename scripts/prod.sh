#!/bin/bash

gunicorn -w 4 -b 0.0.0.0:8000 --chdir src/server 'server:app' &

cd src/client && npm run dev &