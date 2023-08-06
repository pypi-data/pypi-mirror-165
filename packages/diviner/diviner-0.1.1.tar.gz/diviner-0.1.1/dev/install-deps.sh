#!/usr/bin/env bash

set -ex

function retry-with-backoff() {
    for BACKOFF in 0 1 2 4 8 16 32 64; do
        sleep $BACKOFF
        if "$@"; then
            return 0
        fi
    done
    return 1
}

python --version
pip install --upgrade pip wheel
pip --version

DIVINER_HOME=$(pwd)
export DIVINER_HOME
# Add base requirements
required_files=" -r requirements/base-requirements.txt"

if [[ "$INSTALL_PROPHET_DEPS" == "true" ]]; then
  required_files+=" -r requirements/prophet-requirements.txt"
fi

if [[ "$INSTALL_PMDARIMA_DEPS" == "true" ]]; then
  required_files+=" -r requirements/pmdarima-requirements.txt"
fi

if [[ -n $required_files ]]; then
  retry-with-backoff pip install $required_files
fi

echo $DIVINER_HOME
set +ex
