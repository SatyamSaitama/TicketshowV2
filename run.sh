#!/bin/bash

# Start your web server (replace the command with the actual command to start your server)




# Start Celery worker
echo "Starting Celery worker..."
celery -A main beat --loglevel=info &

# Start Celery beat
echo "Starting Celery beat..."
celery -A tasks worker --loglevel=info&

