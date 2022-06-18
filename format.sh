#!/bin/sh

DIR="$(realpath "$(dirname "$0")")"

autopep8 --in-place $(find "$DIR" -name '*.py')
