#!/usr/bin/env bash

export PYTHONPATH=`pwd`:$PYTHONPATH

source venv/bin/activate

python3 auth_server/app.py