#!/bin/sh

sudo pkill uwsgi&
sudo uwsgi --ini /home/pi/ngen-milk-pos/web/uwsgi.ini