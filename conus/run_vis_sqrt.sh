#!/bin/bash

sleep 57
export PATH="/home/poker/miniconda3/envs/goes16_201710/bin:$PATH"
#export time=`date -u "+%Y%m%d%H%M" -d "6 min ago"`
export time=`ls -1 /weather/data/goes16/TIRE/02/*PAO.nc | awk '{$1 = substr($1,30,12)} 1' | sort -u | tail -2 | head -1`

echo $time

sleep 70

cd /home/poker/goes16/conus

python goes16_conus_visible_sqrt_fixeddisk.py $time


