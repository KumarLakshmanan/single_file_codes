#!/bin/bash

url="https://support.aixiomatic.com/support/create_embedding"

# Infinite loop
while true
do
  # Make the request and store the response
  response=$(curl -s $url)

  if [ -z "$response" ] || [ "$response" == "null" ]; then
    pm2 delete crontab
    echo "Empty response, stopping the loop."
    break
  fi

  sleep 2
done
