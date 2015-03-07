# Set the path
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web import db


from default_db_data import DefaultDbData

def create_db():
  t = time.time()
  db.drop_all()
  db.create_all()
  print "Drop & create time: %s sec" % (time.time() - t)

  test = DefaultDbData()
  t = time.time()
  test.create_members()
  print "Created members in %s sec" % (time.time() - t)

  t = time.time()
  test.test_settings()
  print "Created settings in %s sec" % (time.time() - t)

  t = time.time()
  test.create_default_users()
  print "Created users in %s sec" % (time.time() - t)

  t = time.time()
  test.test_rate_setup()
  print "Created rate setup in %s sec" % (time.time() - t)
  #test.datetime_test()
  db.session.commit()

if __name__ == "__main__":
    create_db()