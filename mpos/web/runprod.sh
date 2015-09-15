#!/bin/sh
sudo kill -9 `cat /tmp/mpos-master.pid` && sudo uwsgi --ini /home/pi/mpos/web/uwsgi.ini