from flask import render_template, request, redirect, g, flash, url_for
from flask_login import login_required
from flask.ext.babel import lazy_gettext, gettext

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
	import csv
	from db_manager import db
	from models.member import Member
	import os
	for table in db.metadata.tables.values():
		filename = 'backup/%s.csv' % (table.name)
		with open(os.path.join(app.root_path, filename), 'wb') as outfile:
			outcsv = csv.writer(outfile)
			outcsv.writerow([column.name for column in table.columns])
			records = db.session.query(table).all()
			[outcsv.writerow([getattr(curr, column.name) for column in table.columns]) for curr in records]
			outfile.close()


def do_restore():
	import csv
	from db_manager import db
	from models.member import Member
	import os
	db.drop_all()
	db.create_all()
	for table in db.metadata.tables.values():
		filename = 'backup/%s.csv' % (table.name)
		fpath = os.path.join(app.root_path, filename)

		if not os.path.isfile(fpath):
			continue
		print "Restore %s " % (filename)
		with open(fpath, 'rb') as outfile:
			cf = csv.DictReader(outfile, delimiter=',')
			for row in cf:
				smt = table.insert().values(**row)
				db.engine.execute(smt)
		print "Done"
	db.session.commit()
