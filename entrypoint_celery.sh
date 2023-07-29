#!/bin/bash
. activate chat-analytics

# Get the number of workers from the first script argument
NUM_WORKERS=$1

# Verify that num_workers is a number
if ! [[ "$NUM_WORKERS" =~ ^[0-9]+$ ]]
then
    NUM_WORKERS=1
fi

# Start the specified number of workers
for ((i=1; i<=NUM_WORKERS; i++))
do
    echo "Starting worker $i..."
    celery -A chat_analytics.celery.tasks worker --loglevel=info &
done

# Wait for all background processes to finish
wait
