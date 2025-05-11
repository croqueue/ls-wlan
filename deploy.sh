#!/usr/bin/env bash

# Deploy library code
mpremote fs cp -r src/lib :
# Deploy main
mpremote fs cp src/main.py :
