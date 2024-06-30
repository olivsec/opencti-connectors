#!/bin/bash

# Wait until OpenCTI is fully up and running
while ! nc -z opencti 8080; do
  echo "Waiting for OpenCTI to be up..."
  sleep 3
done

python3 main.py
