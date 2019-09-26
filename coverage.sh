#!/usr/bin/env bash

python -m unittest discover -s .
coverage run --omit */.local/* -m unittest discover -s .
coverage html -i
