#!/usr/bin/env bash

depth="${1:-1}"
["$depth" -ge 12] && exit 0
base "$0" $((depth + 1))

#scripts calls itself repeadtly, used to stimulate abnormal process depth.