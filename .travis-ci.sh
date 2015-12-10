#!/bin/bash

# This script is triggered from the script section of .travis.yml
# It runs the appropriate commands depending on the task requested.

if [[ $TASK = 'flake8' ]]; then
  flake8 --max-line-length 80 --exclude *_pb2.py,.git,__pycache --ignore E111,E121 build.config config_helper.py master.cfg pass_toucher.py
else
  # Otherwise run checkconfig as normal
  mkdir buildbot && cd buildbot && buildbot create-master master && \
  rm -f master/master.cfg.sample && \
  cp ../build.config ../config_helper.py ../master.cfg master/. && \
  cp ../pass_toucher.py master/. && \
  cd master && ./pass_toucher.py && buildbot checkconfig master.cfg
fi
