#!/bin/sh

sudo pkill uwsgi& 2>&1
sudo uwsgi --ini /home/pi/ngen-milk-pos/web/uwsgi.ini