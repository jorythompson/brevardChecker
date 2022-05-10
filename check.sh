#!/bin/bash
if [ ! -d /venv ]
then
  source venv/bin/activate.csh
fi
python3 brevardChecker.py --config check.cfg
