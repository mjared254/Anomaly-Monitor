#!/usr/bin/env bash

find "$HOME" -type f -exec head -c 1 {} \; >/dev/null 2>&1

#stimulates crawling into a given folder and touches every file
#creates a abnormal session where one process is opening far
#more files than normal process would