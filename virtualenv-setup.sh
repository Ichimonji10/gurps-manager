#!/usr/bin/env bash
set -o errexit
set -o nounset
readonly script_name='virtualenv-setup.sh'
readonly usage="usage: ${script_name} <requirements_file> <destdir>

Create a virtualenv environment for GURPS Manager in directory <destdir>.
Requires pip and virtualenv."

# Fetch argument <requirements_file> from user.
if [ -z "${1:-}" ]; then
    echo "${usage}"
    exit 1
else
    readonly requirements_file=$(readlink -e "$1")
fi

# Fetch argument <destdir> from user.
if [ -z "${2:-}" ]; then
    echo "${usage}"
    exit 1
else
    readonly destdir=$(readlink -e "$2")
fi

# Create the virtualenv environment. The "set +o nounset" command is present
# because `activate` and `deactivate` include unbound variables, and because we
# want to exit the virtual environment even if pip fails.
cd "${destdir}"
virtualenv --python=python3.4 GURPS-ENV
set +o nounset
source GURPS-ENV/bin/activate
pip install -r "${requirements_file}"
deactivate
set -o nounset
