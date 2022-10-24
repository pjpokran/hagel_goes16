#!/bin/bash

export PATH="/home/poker/miniconda3/bin:$PATH"
#export time=`date -u "+%Y%m%d%H%M" -d "6 min ago"`
export time=`ls -1t /weather/data/goes16/TIRC/09/*PAA.nc | awk '{$1 = substr($1,30,12)} 1' | sort -u | tail -2 | head -1`

echo $time

sleep 127

cd /home/poker/goes16/conusc

python goes16_conusc_wv.py $time


