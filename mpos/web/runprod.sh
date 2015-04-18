#!/bin/sh

sudo pkill uwsgi& 2>&1
sudo uwsgi --ini /home/pi/mpos/web/uwsgi.ini