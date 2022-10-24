#!/bin/bash


export PATH="/home/poker/miniconda3/bin:$PATH"
#export time=`date -u "+%Y%m%d%H%M" -d "6 min ago"`

cd /home/poker/goes16/conus


#  /weather/data/goes16/"+prod_id+"/"+band+"/latest.nc
cp /weather/data/goes16/TIRE/02/latest.nc /dev/shm/latest_TIRE_02.nc
cmp /weather/data/goes16/TIRE/02/latest.nc /dev/shm/latest_TIRE_02.nc > /dev/null
CONDITION=$?
#echo $CONDITION

while :; do

  until [ $CONDITION -eq 1 ] ; do
#     echo same
     sleep 5
     cmp /weather/data/goes16/TIRE/02/latest.nc /dev/shm/latest_TIRE_02.nc > /dev/null
     CONDITION=$?
  done

#  echo different
  cp /weather/data/goes16/TIRE/02/latest.nc /dev/shm/latest_TIRE_02.nc
  sleep 70
# goes16_conus_visible_sqrt_fixeddisk.py  goes16_conus_visible_fixeddisk.py
  /home/poker/miniconda3/envs/goes16_201710/bin/python goes16_conus_visible_sqrt_fixeddisk_latest.py /dev/shm/latest_TIRE_02.nc
  /home/poker/miniconda3/envs/goes16_201710/bin/python goes16_conus_visible_fixeddisk_latest.py /dev/shm/latest_TIRE_02.nc
  cmp /weather/data/goes16/TIRE/02/latest.nc /dev/shm/latest_TIRE_02.nc > /dev/null
  CONDITION=$?
#  echo repeat

done
