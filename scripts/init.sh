#!/usr/bin/env bash

PYTHON=python3

if !(type $PYTHON); then
  echo "$PYTHON isn't installed! Please install it."
  exit 1
fi

if !(type "poetry" > /dev/null 2>&1); then
  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
    | $PYTHON /dev/stdin --yes --no-modify-path
fi

poetry install
