#!/usr/bin/env bash

set -e
set -x

mypy fastapi
flake8 fastapi tests
black fastapi tests --check
isort fastapi tests docs_src scripts --check-only
