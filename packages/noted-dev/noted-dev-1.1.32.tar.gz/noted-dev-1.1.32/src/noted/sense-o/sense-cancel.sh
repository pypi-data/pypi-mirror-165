#!/bin/sh

echo "------------------------------------------------------------------" >> noted/logs/sense.log
date >> noted/logs/sense.log
echo "Received cancel request from NOTED for $2" >> noted/logs/sense.log

STATUS=`sense_util.py -s -u $1`
echo "$2 current status:" ${STATUS} >> noted/logs/sense.log

if [ "$STATUS" = "REINSTATE - READY" ] || [ "$STATUS" = "REINSTATE - COMMITTED" ] || [ "$STATUS" = "CREATE - READY" ]
then
  echo "$2 is up: OK to cancel" >> noted/logs/sense.log
  sense_util.py -ca -u $1 >> noted/logs/sense.log
  date >> noted/logs/sense.log
  echo "$2 done" >> noted/logs/sense.log
else
  echo "ERROR to cancel" >> noted/logs/sense.log
fi

exit 0