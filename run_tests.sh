#!/bin/bash

echo "Running tests"

# Prepare database
echo "Preparing DB..."
poetry run python src/db_helper.py
echo "DB setup done"

# Run pytest under coverage
echo "Running unit tests (pytest) under coverage..."
poetry run coverage run --parallel-mode --branch -m pytest
PYTEST_STATUS=$?
echo "pytest exit status: ${PYTEST_STATUS}"

if [[ ${PYTEST_STATUS} -ne 0 ]]; then
  echo "pytest failed"
  exit ${PYTEST_STATUS}
fi

# Start Flask app under coverage (in background)
echo "Starting Flask app under coverage..."
poetry run coverage run --parallel-mode --branch src/index.py &
SERVER_PID=$!
echo "Flask started (pid=${SERVER_PID})"

# Ensure server is stopped on exit
trap 'echo "Stopping server"; kill ${SERVER_PID} 2>/dev/null || true' EXIT

# wait for server to respond HTTP 200 (timeout after 60s)
echo "Waiting for server to be ready..."
MAX_WAIT=60
i=0
until [[ "$(curl -s -o /dev/null -w '%{http_code}' http://localhost:5001)" == "200" ]]; do
  sleep 1
  i=$((i+1))
  if [[ $i -ge $MAX_WAIT ]]; then
    echo "Server no ready within ${MAX_WAIT}s, stopping."
    kill ${SERVER_PID} 2>/dev/null || true
    exit 2
  fi
done
echo "Flask server is ready."

# Run robot tests
echo "Running Robot Framework tests..."
poetry run robot --variable HEADLESS:true src/story_tests
ROBOT_STATUS=$?
echo "robot exit status: ${ROBOT_STATUS}"

# Stop server
echo "Stopping Flask server..."
kill ${SERVER_PID} 2>/dev/null || true
wait ${SERVER_PID} 2>/dev/null || true

if [[ ${ROBOT_STATUS} -ne 0 ]]; then
  echo "Robot tests failed — exiting."
  exit ${ROBOT_STATUS}
fi

# Combine coverage data
echo "All tests passed."
echo "Combining coverage data..."
poetry run coverage combine || true

echo "Done."
exit 0
