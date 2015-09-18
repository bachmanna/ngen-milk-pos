#!/bin/bash
PID='/tmp/mpos-master.pid'
UWSGI='/home/pi/mpos/web/uwsgi.ini'

if [ -f "$PID" ]; then
  pid=`cat $PID`
  (sudo kill -9 "$pid"; sudo uwsgi --ini "$UWSGI")
else
  sudo uwsgi --ini "$UWSGI"
fi