#!/usr/bin/env bash

python -m unittest discover -s . || exit 1

coverage run --omit */.local/* -m unittest discover -s yo_fluq__tests

coverage html -d test_coverage/yo_fluq

coverage report > test_coverage/yo_fluq_report.txt

coverage run --omit */.local/* -m unittest discover -s .

coverage html -d test_coverage/all



python check_coverage.py