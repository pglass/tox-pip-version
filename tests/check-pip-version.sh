#!/bin/bash -x

EXPECTED_PIP_VERSION="${1?Need expected pip version}"
PIP_VERSION_OUTPUT=`pip --version`

if [[ "$PIP_VERSION_OUTPUT" == *"$EXPECTED_PIP_VERSION"* ]]; then
    exit 0
fi

exit 1
