#!/usr/bin/env bash

for i in $(seq 1 500); do /bin/true; /bin/echo "$i" >/dev/null; done