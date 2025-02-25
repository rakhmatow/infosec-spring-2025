#!/usr/bin/env bash

WORK_DAY_BEGIN="09:00"
WORK_DAY_END="18:00"

current_time=$(date +%s)
time_until_begin=$(( $(date -d $WORK_DAY_BEGIN +%s) - $current_time ))
time_until_end=$(( ($(date -d $WORK_DAY_END +%s) - $current_time + 59) / 60 * 60 ))

echo -n "Current time: $(date -d \@$current_time +%H:%M)."

if [ $time_until_begin -gt 0 ]; then
    echo " Work day has not begun."
elif [ $time_until_end -le 0 ]; then
    echo " Work day has ended."
else
    echo " Work day ends after $(date -u -d \@$time_until_end +'%-H hours and %-M minutes')."
fi
