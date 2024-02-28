#!/bin/bash

python3 src/server/server.py run &

cd src/client && npm run dev &