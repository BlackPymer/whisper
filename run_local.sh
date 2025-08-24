#!/bin/bash

# Add local bin directory to PATH
export PATH="$(pwd)/bin:$PATH"

# Run the server using uv's virtual environment
uv run python3 run_server.py 