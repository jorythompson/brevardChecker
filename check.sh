#!/bin/bash
if [ ! -d /venv ]
then
  venv/bin/python3 brevardChecker.py --config check.cfg
else
  python3 brevardChecker.py --config check.cfg
fi