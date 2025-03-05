#!/bin/bash

echo "Starting now"

# You can put other setup logic here
alembic upgrade head

# Evaluating passed command:
exec "$@"
