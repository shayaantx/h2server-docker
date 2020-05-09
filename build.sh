#!/usr/bin/env bash

docker-compose rm -f -s || true
python build.py
docker-compose build --no-cache