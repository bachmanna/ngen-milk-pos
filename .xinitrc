#!/bin/sh
xset -dpms
xset s off
xset s noblank
fbset -depth $( cat /sys/module/*fb*/parameters/fbdepth );
/home/pi/mpos/web/runprod.sh
sed -i 's/"exited_cleanly": false/"exited_cleanly": true/' ~/.config/chromium/Default/Preferences
chromium --noerrdialogs --kiosk http://localhost --incognito