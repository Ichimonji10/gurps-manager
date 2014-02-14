#!/usr/bin/env bash
set -o errexit
set -o nounset
readonly script_name='virtualenv-setup.sh'
readonly usage="usage: ${script_name} <destdir>

Create a virtualenv environment for GURPS Manager in directory <destdir>.
Requires pip and virtualenv."

# Fetch argument <destdir> from user.
if [ -z "${1:-}" ]; then
    echo "$usage"
    exit 1
else
    readonly srcdir=$(readlink -e "$1")
fi

# Create the virtualenv environment.
echo -n "Creating virtualenv environment in directory ${srcdir}... "
cd "$srcdir"
virtualenv --python=python3.3 GURPS-ENV
# The script being sourced includes unbound variables.
set +o nounset
source GURPS-ENV/bin/activate
set -o nounset
pip install django
pip install django_extensions
pip install django_tables2
pip install factory_boy
pip install pylint
pip install pyyaml
set +o nounset
deactivate
set -o nounset
echo 'done.'
