#!/bin/sh

set -e

echo "Run tests"

# execute unittests
python -m unittest discover .

echo "Run applicattion"

# Run the application
python -m movie_list