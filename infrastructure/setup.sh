#!/bin/bash -x

PUBLIC_REQUIREMENTS=requirements.txt
PRIVATE_REQUIREMENTS=requirements_private.txt
NEXUS_URL=https://nexus.alemira.dev/repository/pypi/simple
WORKING_DIRECTORY=$(pwd)

if [[ "$WORKING_DIRECTORY" == *E2E ]]; then
  cd ./infrastructure || return
fi

pip3 install --upgrade pip
pip3 install -r $PUBLIC_REQUIREMENTS
pip3 install -r $PRIVATE_REQUIREMENTS -i $NEXUS_URL
