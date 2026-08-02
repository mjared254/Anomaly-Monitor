#!/usr/bin/env bash
#usage : sudo ./capture.sh <label> <seconds>
#Bash Script -> Captures the dataset

#runs the collector for <seconds> and saves output to data folder.

set -euo pipefail

PROJECT="/home/jared/anomaly-monitor"

LABEL="${1:?need a label}" #if there is no label print error and stop
SECS="${2:-300}" #if no secs given set default to 300
OUT="$PROJECT/data/raw/${LABEL}_$(date +%Y%m%d_%H%M%S).jsonl"

echo "capturing '$LABEL' for ${SECS}s -> $OUT"
timeout "$SECS" "$PROJECT/collector/collector" > "$OUT" || true
echo "done: $(wc -l < "$OUT" ) events"