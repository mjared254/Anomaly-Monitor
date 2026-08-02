#!/usr/bin/env bash

for i in $(seq 1 500); do /bin/true; /bin/echo "$i" >/dev/null; done

#runs 500 tiny commands in a row to stimulate a session where the process-creation rate
#spikes far above normal, mirroring rapidly spawning process.