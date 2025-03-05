#!/bin/bash

# Start the first process
python -i -m app.consumer.karma_coins_minted &
python -i -m app.consumer.student_funds_courses_updated &
python -i -m app.consumer.user_updated &

# Start the second process
gunicorn app.server:main_app --worker-class uvicorn.workers.UvicornWorker --config /gunicorn_conf.py &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
