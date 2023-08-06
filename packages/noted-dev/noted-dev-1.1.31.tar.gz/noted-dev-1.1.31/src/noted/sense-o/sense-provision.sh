#!/bin/sh

echo "------------------------------------------------------------------" >> noted/logs/sense.log
date >> noted/logs/sense.log
echo "Received provision request from NOTED for $2"  >> noted/logs/sense.log

STATUS=`sense_util.py -s -u $1`
echo "$2 current status:" ${STATUS} >> noted/logs/sense.log

if [ "$STATUS" = "CANCEL - READY" ]
then
  echo "$2 is down: OK to provision" >> noted/logs/sense.log
  sense_util.py -r -u $1 >> noted/logs/sense.log
  date >> noted/logs/sense.log
  echo "$2 done" >> noted/logs/sense.log
else
  echo "ERROR to provision" >> noted/logs/sense.log
fi

exit 0