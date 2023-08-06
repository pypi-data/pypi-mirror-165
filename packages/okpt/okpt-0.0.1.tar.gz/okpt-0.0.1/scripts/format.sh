#!/bin/bash
SOURCES="okpt tests"

echo "Running isort..."
isort $SOURCES
echo "-----"

echo "Running black..."
black --skip-string-normalization $SOURCES
