#!/usr/bin/env bash
#usage : sudo ./capture.sh <label> <seconds>
#Bash Script -> Captures the dataset

set -euo pipefall

LABEL = "${1:?need a label}" #if there is no label print error and stop
SECS = "${2:-300}" #if no secs given set default to 300
OUT = "$HOME/anomaly-monitor/data/raw/${LABEL}_$(date +%Y%m%d_%H%M%S).json1"

echo "capturing '$LABEL' for ${SECS}s -> $OUT"
timeout "$SECS" "$HOME/anomaly-monitor/collector/collector" > "$OUT" || true
echo "done: $(wc -1 < "$OUT" ) events"