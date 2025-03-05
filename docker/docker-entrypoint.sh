#!/bin/bash

# echo "Starting now"
# while :
# do
#     echo "IN loop"
#     nc -z localstack 4566;
#     result=$?
#     if [[ $result -eq 0 ]]; then
#         echo "localstack is available"
#         break
#     fi
#     echo "localstack is unavailable. Sleeping"
#     sleep 1
# done


# activate our virtual environment here
. /opt/pysetup/.venv/bin/activate

# You can put other setup logic here
alembic upgrade head
python app/shared/infra/setup_sns_sqs.py
python app/shared/infra/setup_s3.py

# Evaluating passed command:
exec "$@"
