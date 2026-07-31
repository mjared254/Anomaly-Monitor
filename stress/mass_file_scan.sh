#!/usr/bin/env bash

find "$HOME" -type f -exec head -c 1 {} \; >/dev/null 2>&1