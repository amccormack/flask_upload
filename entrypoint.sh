#!/bin/bash

python flask_upload.py "$@" --upload-folder /tmp/output --host 0.0.0.0 --port 5000
