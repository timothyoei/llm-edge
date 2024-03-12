#!/bin/bash

# Check if a port number is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <port-number>"
    exit 1
fi

PORT=$1

# Find the process using the specified port
PID=$(lsof -t -i:$PORT)

# Check if any process was found
if [ -z "$PID" ]; then
  echo "No process found running on port $PORT."
  exit 1
fi

# Kill the process
kill -9 $PID

if [ $? -eq 0 ]; then
  echo "Process on port $PORT has been terminated."
else
  echo "Failed to terminate process on port $PORT."
fi