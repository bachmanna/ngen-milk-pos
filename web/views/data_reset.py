from flask import render_template, request, redirect, g, flash, url_for
from flask_login import login_required
from flask.ext.babel import lazy_gettext, gettext
from dateutil import parser
import time
import csv
import os

from web import app

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
def factory_reset():
	from initdb import create_db
	create_db()
	msg = "Successfully reseted the system with factory data!!"
	flash(str(lazy_gettext(msg)))
	return redirect(url_for("data_reset"))


@app.route("/data_backup")
@login_required
def data_backup():
	do_backup()
	msg = "Data backup successfull!"
	flash(str(lazy_gettext(msg)))
	return redirect(url_for("data_reset"))


@app.route("/data_restore")
@login_required
def data_restore():
	do_restore()
	msg = "Data restore successfull!"
	flash(str(lazy_gettext(msg)))
	return redirect(url_for("data_reset"))


def do_backup():
	from db_manager import db
	import os
	t = time.time()
	for table in db.metadata.tables.values():
		filename = 'backup/%s.csv' % (table.name)
		print "Backup %s " % (filename)
		with open(os.path.join(app.root_path, filename), 'wb') as outfile:
			outcsv = csv.writer(outfile)
			outcsv.writerow([column.name for column in table.columns])
			records = db.session.query(table).all()
			[outcsv.writerow([getattr(curr, column.name) for column in table.columns]) for curr in records]
			outfile.close()
	print "Backup done in %s sec" % (time.time() - t)

def do_restore():
	from db_manager import db
	db.drop_all()
	db.create_all()
	t = time.time()
	for table in db.metadata.tables.values():
		t0 = time.time()
		filename = 'backup/%s.csv' % (table.name)
		fpath = os.path.join(app.root_path, filename)

		if not os.path.isfile(fpath):
			continue
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
