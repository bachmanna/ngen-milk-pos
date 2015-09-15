import sys
import os
import re
from datetime import datetime
from glob import glob
import zipfile
from subprocess import call

USB_DRV_PATH = "/home/pi/usbdrv"
# USB_DRV_PATH = "/media/usb0"
USB_DRV_MOUNT_PATH = "/dev/sda1"
EXTRACT_PATH = "/home/pi/mpostest"
VERSION_FILE = "/home/pi/mpos/_version.py"

def is_usb_storage_connected():
  return os.path.exists(USB_DRV_MOUNT_PATH) and os.path.ismount(USB_DRV_PATH)

def do_upgrade(directory):
	files = glob(os.path.join(directory, "mpos*.zip"))
	if len(files) > 0:
		source_filename = files[0]
		print("Found upgrade file at %s" % source_filename)
		try:
			with zipfile.ZipFile(source_filename) as zf:
				current_version, upgrade_version = get_versions(zf)
				if can_upgrade_version(current_version, upgrade_version):
					zf.extractall(path=EXTRACT_PATH)
					restart_uwsgi()
					print('UPGRADE SUCCESS!!! (%s ---> %s)' % (current_version, upgrade_version))
				else:
					print("FIRMWARE is already upto date (%s == %s)!!!" % (current_version, upgrade_version))
		except Exception as e:
			print(e)
			print("UPGRADE FAILED!!!")
	else:
		print("No upgrade file found..")

def restart_uwsgi():
	# killall -9 uwsgi 2>/dev/null;
	# sudo uwsgi --ini /home/pi/mpos/web/uwsgi.ini;
	call(['/home/pi/mpos/web/runprod.sh'])

def get_versions(zf):
	current_version = read_version(VERSION_FILE)
	upgrade_version = None

	for member in zf.infolist():
		if not '_version.py' in member.filename:
			continue
		with zf.open(member) as f:
			upgrade_version = parse_version(f.read())
		break
	return current_version, upgrade_version

def can_upgrade_version(current_version, upgrade_version):
	return upgrade_version != None and current_version != None and upgrade_version != current_version

def read_version(filename):
	if not os.path.exists(filename):
		return None
	data = None
	with open(VERSION_FILE, 'r') as r:
		data = r.read()
	return parse_version(data)

def parse_version(text):
	s = re.search('__version__ = \'(?P<v>.*)\'', text)
	if not s:
		return None
	return s.group('v')

if __name__ == "__main__":
	print("MPOS --- Checking for update file in pendrive")

	if not is_usb_storage_connected():
		print("NO USB PENDRIVE FOUND")
		print("Exiting upgrade...")
	else:
		directory = os.path.join(USB_DRV_PATH, "mpos_firmware")
		if os.path.exists(directory):
			do_upgrade(directory)