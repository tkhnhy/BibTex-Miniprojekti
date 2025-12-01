#!/bin/bash

echo "Running tests"

# creating a database
poetry run python src/db_helper.py

echo "DB setup done"

# starting the Flask server in the background
poetry run python3 src/index.py &

echo "started Flask server"

# waiting until the server is ready to accept requests
while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' localhost:5001)" != "200" ]];
  do sleep 1;
done

echo "Flask server is ready"

# tests are done
poetry run robot --variable HEADLESS:true src/story_tests

status=$?

# stopping the Flask server on port 5001
kill $(lsof -t -i:5001)

exit $status
