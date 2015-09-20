import sys
import os
import re
from datetime import datetime
from glob import glob
import zipfile
from subprocess import call

EXTRACT_PATH = "/home/pi"

USB_DRV_PATH = "/home/pi/usbdrv"
FIRMWARE_PATH = "/home/pi/usbdrv/mpos_firmware"
# USB_DRV_PATH = "/media/usb0"
USB_DRV_MOUNT_PATH = "/dev/sda1"

VERSION_FILE = EXTRACT_PATH + "/mpos/_version.py"
DB_FILE = EXTRACT_PATH + "/mpos/web/app.db"

MIDORI_CONFIG_PATH = "/home/pi/.midori/"
APP_CONFIG_PATH = EXTRACT_PATH + "/mpos/config/"
APP_EXECUTE_FILE = EXTRACT_PATH + "/mpos/web/runprod.sh"

SPLASHSCREEN_FILE = dict(source=FIRMWARE_PATH + '/splash.png', target='/etc/splash.png')
COW_IMAGE_FILE = dict(source=FIRMWARE_PATH+'/cow.png', target=EXTRACT_PATH + '/mpos/web/static/images/cow.png')
FOOTER_IMAGE_FILE = dict(source=FIRMWARE_PATH+'/footer.png', target=EXTRACT_PATH + '/mpos/web/static/images/footer.png')


def is_usb_storage_connected():
	return os.path.exists(USB_DRV_MOUNT_PATH) and os.path.ismount(USB_DRV_PATH)

def web_app_upgrade_task():
	files = glob(os.path.join(FIRMWARE_PATH, "mpos*.zip"))

	if len(files) > 0:
		source_filename = files[0]
		print("Found upgrade file at %s" % source_filename)
		try:
			with zipfile.ZipFile(source_filename) as zf:
				current_version, upgrade_version = get_versions(zf)
				if can_upgrade_version(current_version, upgrade_version):
					backup_db(current_version)
					zf.extractall(path=EXTRACT_PATH)
					link_config_files()
					restart_uwsgi()
					print('UPGRADE SUCCESS!!! (%s ---> %s)' % (current_version, upgrade_version))
				else:
					print("FIRMWARE is already upto date (%s == %s)!!!" % (current_version, upgrade_version))
		except Exception as e:
			print(e)
			print("UPGRADE FAILED!!!")
	else:
		print("No application upgrade file found..")

def mkdir(path):
	if not os.path.exists(path):
		os.makedirs(path)

def backup_db(version):
	if not os.path.exists(DB_FILE):
		return
	filename = "app_data_%s.db" % (version.replace('.', '_'))
	dest_file = os.path.join(FIRMWARE_PATH, 'data_backup', filename)

	mkdir(os.path.dirname(dest_file))

	call(['cp', DB_FILE, dest_file])
	print("Backup database complete, %s" % (dest_file))

def link_config_files():
	if not os.path.exists(APP_CONFIG_PATH):
		print("No config folder found!")
		return
	link_xinitrc()
	link_midori()

def link_xinitrc():
	xinitrc_file = os.path.join(APP_CONFIG_PATH,'.xinitrc')
	link_file(xinitrc_file, "/home/pi/.xinitrc")

def link_midori():
	config_file = os.path.join(APP_CONFIG_PATH,'midori_config')
	accels_file = os.path.join(APP_CONFIG_PATH,'midori_accels')
	mkdir(MIDORI_CONFIG_PATH)
	link_file(config_file, os.path.join(MIDORI_CONFIG_PATH,'config'))
	link_file(accels_file, os.path.join(MIDORI_CONFIG_PATH,'accels'))

def link_file(src, dest):
	if not os.path.exists(src):
		return
	try:
		os.remove(dest)
		os.symlink(src, dest)
		print("Linking config file %s -> %s" % (src, dest))
	except Exception as e:
		print(e)

def restart_uwsgi():
	# killall -9 uwsgi 2>/dev/null;
	# sudo uwsgi --ini /home/pi/mpos/web/uwsgi.ini;
	call([APP_EXECUTE_FILE])

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


def splash_screen_upgrade_task():
	update_image_file(SPLASHSCREEN_FILE['source'], SPLASHSCREEN_FILE['target'])

def web_app_image_upgrade_task():
	update_image_file(COW_IMAGE_FILE['source'], COW_IMAGE_FILE['target'])
	update_image_file(FOOTER_IMAGE_FILE['source'], FOOTER_IMAGE_FILE['target'])

def update_image_file(src, dest):
	if not os.path.exists(src):
		return
	os.remove(dest)
	os.link(src, dest)

tasks = [web_app_upgrade_task, splash_screen_upgrade_task, web_app_image_upgrade_task]

if __name__ == "__main__":
	print("MPOS --- Checking for upgrade file in pendrive")

	if not is_usb_storage_connected():
		print("NO USB PENDRIVE FOUND")
		print("Exiting upgrade...")
	elif not os.path.exists(FIRMWARE_PATH):
			print("No upgrade file found..")
	else:
		for task in tasks:
			task()
