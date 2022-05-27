#!/usr/bin/env bash9
docker build -t drug_search ..
docker tag drug_search:latest drug_search:1.2.0
