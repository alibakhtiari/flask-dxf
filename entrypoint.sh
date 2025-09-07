#!/bin/sh

# Start the cron daemon in the background
cron

# Start the Python application in the foreground
# Using 'exec' ensures that the application becomes the main process (PID 1),
# which allows it to receive signals correctly, like from 'docker stop'.
exec python app.py