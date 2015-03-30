from flask import render_template, request, redirect, g, flash, url_for, jsonify
from flask_login import login_required
from flask.ext.babel import lazy_gettext, gettext

from web import app, admin_permission, get_backup_directory, is_usb_storage_connected

from services.milkcollection_service import MilkCollectionService
from services.export_import_service import ExportImportService

@app.route("/data_reset")
@login_required
def data_reset():
  return render_template("data_reset.jinja2")


@app.route("/clear_collection_bills")
@login_required
def clear_collection_bills():
	service = MilkCollectionService()
	count = service.clear_collection_bills()
	msg = "%s Milk collection data deleted!" % (count)
	flash(str(lazy_gettext(msg)))
	return redirect(url_for("data_reset"))


@app.route("/factory_reset")
@login_required
@admin_permission.require()
def factory_reset():
	from initdb import create_db
	create_db()
	msg = "Successfully reseted the system with factory data!!"
	flash(str(lazy_gettext(msg)))
	return redirect(url_for("data_reset"))


@app.route("/data_backup")
@login_required
def data_backup():
  	service = ExportImportService(None)
	backup_location, backup_duration = service.do_backup()
	msg = "Data backup to \"%(loc)s\" completed successfully in %(dur).2f seconds!"
	flash(str(lazy_gettext(msg, loc=backup_location, dur=backup_duration)))
	return redirect(url_for("data_reset"))


@app.route("/get_available_data_backup")
@login_required
def get_available_data_backup():
	import os
	from datetime import datetime
	directory = get_backup_directory()
	paths = filter(lambda x: (not os.path.isfile(x)) and x.isdigit(), os.listdir(directory))
	paths.sort(key=lambda x: -os.path.getmtime(os.path.join(directory, x)))
	directory = [(x,datetime.fromtimestamp(int(x))) for x in paths]
	return render_template("backup_list.jinja2", data=directory)


@app.route("/data_restore")
@login_required
@admin_permission.require()
def data_restore():
	p = request.args.get("key", None)
	if p:
		service = ExportImportService(None)
		service.do_restore(p)
	msg = "Data restore successfull!"
	flash(str(lazy_gettext(msg)))
	return redirect(url_for("data_reset"))


@app.route("/get_usb_storage_devices")
@login_required
def get_usb_storage_devices():
	devices = []

	if is_usb_storage_connected():
		try:
			import subprocess as sp
			vendor = sp.check_output(["cat", "/sys/class/block/sda/device/vendor"]).strip("\n").strip(" ")
			model = sp.check_output(["cat", "/sys/class/block/sda/device/model"]).strip("\n").strip(" ")
			name = vendor + model
			devices.append(name)
		except Exception as e:
			print e
	return render_template("usb_devices.jinja2", devices=devices)