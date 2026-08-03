
#!/usr/bin/env bash
depth="${1:-1}"
if [ "$depth" -ge 12 ]; then
    exit 0
fi
bash "$0" $((depth + 1))

#scripts calls itself repeadtly, used to stimulate abnormal process depth.