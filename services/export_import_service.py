from dateutil import parser
import os
import sys
import csv
import time
from datetime import datetime

from flask import g
from web import get_backup_directory
from db_manager import db

class ExportImportService(object):
	def __init__(self, table, filename=None):
		self.path = get_backup_directory()
		self.table = table
		self.filename = filename

		if not self.filename and self.table is not None:
			self.filename = str(self.table.name)

		if self.filename and "." not in self.filename:
			self.filename = self.filename + ".csv"
		pass


	def do_export(self):
		if self.table is None:
			return False
		try:
		  fpath = os.path.join(self.path, self.filename)
		  print "Export data to the folder %s" % (fpath)
		  with open(fpath, 'wb') as outfile:
		      outcsv = csv.writer(outfile)
		      outcsv.writerow([column.name for column in self.table.columns])
		      records = db.session.query(self.table).all()
		      [outcsv.writerow([getattr(curr, column.name) for column in self.table.columns]) for curr in records]
		      outfile.close()
		  return True
		except Exception as e:
			print e
		return False


	def do_import(self):
		if self.table is None:
			return False
		try:
			fpath = os.path.join(self.path, self.filename)
			print "Import data from folder %s" % (fpath)
			if not os.path.isfile(fpath):
				return False
			with open(fpath, 'rb') as infile:
				# delete all rows
				db.engine.execute(self.table.delete())
				cf = csv.DictReader(infile, delimiter=',')
				smt = self.table.insert()
				data = [row for row in cf]
				if len(data) > 0:
					self.update_date_time_objects(row, data)
					db.engine.execute(smt, data)
				infile.close()
			return True
		except Exception as e:
			print e
		return False


	def update_date_time_objects(self, row, data):
		if "created_at" in row.keys():
			for row in data:
				row["created_at"] = parser.parse(row["created_at"])
				if len(row["updated_at"]) > 0:
					row["updated_at"] = parser.parse(row["updated_at"])
				else:
					row["updated_at"] = None
					row["updated_by"] = None
					row["status"] = row["status"] == "True"

	
	def do_backup(self):
		bdir = str(int(time.mktime(datetime.now().timetuple())))
		t = time.time()
		directory = os.path.join(self.path, bdir)

		if not os.path.exists(directory):
			os.makedirs(directory)

		for table in db.metadata.tables.values():		
			self.filename = '%s.csv' % (table.name)
			self.table = table
			self.path = directory
			self.do_export()
		
		backup_duration = (time.time() - t)
		print "Backup done in %s sec" % (backup_duration)
		return directory, backup_duration


	def do_restore(self, selected_bak_path):
		t = time.time()
		for table in db.metadata.tables.values():
			t0 = time.time()
			filename = '%s/%s.csv' % (selected_bak_path, table.name)
			fpath = os.path.join(self.path, filename)
			if not os.path.isfile(fpath):
				continue

			self.filename = filename
			self.table = table

			table.drop(db.engine)
			table.create(db.engine)

			self.do_import()

			print "...done in %s sec" % (time.time() - t0)

		print "Total time: %s sec" % (time.time() - t)
		db.session.commit()
