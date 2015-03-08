from flask import render_template, request, redirect, g, flash, url_for, jsonify
from flask_login import login_required
from flask.ext.babel import lazy_gettext, gettext
from dateutil import parser
from datetime import datetime
import time
import csv
import os

from web import app, admin_permission

from services.milkcollection_service import MilkCollectionService

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
	backup_location, backup_duration = do_backup()
	msg = "Data backup to \"%(loc)s\" completed successfully in %(dur)s seconds!"
	flash(str(lazy_gettext(msg, loc=backup_location, dur=backup_duration)))
	return redirect(url_for("data_reset"))


@app.route("/get_available_data_backup")
@login_required
def get_available_data_backup():
	p = os.path.join(app.root_path, 'backup')
	paths = filter(lambda x: (not os.path.isfile(x)) and x.isdigit(), os.listdir(p))
	paths.sort(key=lambda x: os.path.getmtime(os.path.join(app.root_path, 'backup/'+x)))
	directory = [(x,datetime.fromtimestamp(int(x))) for x in paths]
	return render_template("backup_list.jinja2", data=directory)

@app.route("/data_restore")
@login_required
@admin_permission.require()
def data_restore():
	p = request.args.get("key", None)
	if p:
		do_restore(p)
	msg = "Data restore successfull!"
	flash(str(lazy_gettext(msg)))
	return redirect(url_for("data_reset"))


def do_backup():
	from db_manager import db
	n = int(time.mktime(datetime.now().timetuple()))
	t = time.time()
	directory = os.path.join(app.root_path, 'backup/%d' % (n))
	if not os.path.exists(directory):
			os.makedirs(directory)
	print "Backup to folder %s" % (directory)

	for table in db.metadata.tables.values():		
		filename = '%s.csv' % (table.name)
		fpath = os.path.join(directory, filename)

		with open(fpath, 'wb') as outfile:
			outcsv = csv.writer(outfile)
			outcsv.writerow([column.name for column in table.columns])
			records = db.session.query(table).all()
			[outcsv.writerow([getattr(curr, column.name) for column in table.columns]) for curr in records]
			outfile.close()
	
	backup_duration = (time.time() - t)
	print "Backup done in %s sec" % (backup_duration)
	return directory, backup_duration

def do_restore(p):
	from db_manager import db
	t = time.time()
	for table in db.metadata.tables.values():
		t0 = time.time()
		filename = 'backup/%s/%s.csv' % (p, table.name)
		fpath = os.path.join(app.root_path, filename)

		if not os.path.isfile(fpath):
			continue

		table.drop(db.engine)
		table.create(db.engine)
		print "Restore %s " % (filename)
		with open(fpath, 'rb') as outfile:
			cf = csv.DictReader(outfile, delimiter=',')
			smt = table.insert()
			data = [row for row in cf]
			if len(data) > 0:
				if "created_at" in row.keys():
					for row in data:
						row["created_at"] = parser.parse(row["created_at"])
						if len(row["updated_at"]) > 0:
							row["updated_at"] = parser.parse(row["updated_at"])
						else:
							row["updated_at"] = None
							row["updated_by"] = None
						row["status"] = row["status"] == "True"
				db.engine.execute(smt, data)
		print "Done in %s sec" % (time.time() - t0)
	print "Total time: %s sec" % (time.time() - t)
	db.session.commit()
