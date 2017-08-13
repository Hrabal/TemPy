#!/bin/bash

set -e

CHANGED_FILES=`git diff --name-only master...${TRAVIS_COMMIT}`
ONLY_READMES=True
MD=".md"

for CHANGED_FILE in $CHANGED_FILES; do
  if ! [[ $CHANGED_FILE =~ $MD ]]; then
    ONLY_READMES=False
    break
  fi
done

if [[ $ONLY_READMES == True ]]; then
  echo "Only .md files found, exiting."
  travis_terminate 0
  exit 1
else
  echo "Non-.md files found, continuing with build."
fi
