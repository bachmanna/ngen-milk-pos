#!/bin/sh
while true; do

	# Clean up previously running apps, gracefully at first then harshly
	killall -TERM chromium 2>/dev/null;
	killall -TERM midori 2>/dev/null;
	killall -TERM matchbox-window-manager 2>/dev/null;

	killall -TERM uwsgi 2>/dev/null;

	sleep 2;
	killall -9 chromium 2>/dev/null;
	killall -9 midori 2>/dev/null;
	killall -9 matchbox-window-manager 2>/dev/null;

	killall -9 uwsgi 2>/dev/null;

	if [ -f /home/pi/mpos/app_upgrade.pyc ]; then
		sudo python /home/pi/mpos/app_upgrade.pyc;
	fi

	sudo uwsgi --ini /home/pi/mpos/web/uwsgi.ini;

	sleep 2;

	# Clean out existing profile information
	rm -rf /home/pi/.cache;
	rm -rf /home/pi/.config;
	rm -rf /home/pi/.pki;

	# Generate the bare minimum to keep Chromium happy!
	mkdir -p /home/pi/.config/chromium/Default
	sqlite3 /home/pi/.config/chromium/Default/Web\ Data "CREATE TABLE meta(key LONGVARCHAR NOT NULL UNIQUE PRIMARY KEY, value LONGVARCHAR); INSERT INTO meta VALUES('version','46'); CREATE TABLE keywords (foo INTEGER);";

	# Disable DPMS / Screen blanking
	xset -dpms
	xset s off
	# xset s noblank

	# Reset the framebuffer's colour-depth
	fbset -depth $( cat /sys/module/*fb*/parameters/fbdepth );

	# Hide the cursor (move it to the bottom-right, comment out if you want mouse interaction)
	# xwit -root -warp $( cat /sys/module/*fb*/parameters/fbwidth ) $( cat /sys/module/*fb*/parameters/fbheight )

	# Start the window manager (remove "-use_cursor no" if you actually want mouse interaction)
	#matchbox-window-manager -use_titlebar no -use_cursor no &
	matchbox-window-manager -use_titlebar no &

	# Start the browser (See http://peter.sh/experiments/chromium-command-line-switches/)
	sed -i 's/"exited_cleanly": false/"exited_cleanly": true/' ~/.config/chromium/Default/Preferences
	# chromium  --incognito --noerrdialogs --kiosk http://localhost/
	midori -e Fullscreen -c /home/pi/.midori/ --app http://localhost/

done;
