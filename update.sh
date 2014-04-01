#!/bin/bash

repo=$(dirname $0)
cd $repo
git fetch origin
output=$(git log HEAD..origin/master --oneline)
if [ -n "$output" ]; then
  echo "Merging";
  git merge origin/master;
  buildbot checkconfig master.cfg
  # checkconfig exits 1 if everything is ok.
  if [ $? -eq 1]; then
    buildbot reconfig
  else
    echo "Buildbot config is bad";
  fi;
fi
