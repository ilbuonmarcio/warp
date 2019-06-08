#!/bin/sh
set -e

export FLASK_DEBUG=1 
flask run --host 0.0.0.0 --port 33456
