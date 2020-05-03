#!/usr/bin/env bash

docker-compose rm -f -s || true
docker-compose build --no-cache
python build.py