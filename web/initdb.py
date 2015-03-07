# Set the path
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web import db


from default_db_data import DefaultDbData

def create_db():
  db.drop_all()
  db.create_all()
  test = DefaultDbData()
  print "Creating Members..."
  test.create_members()
  print "Creating Settings..."
  test.test_settings()
  print "Creating Users..."
  test.create_default_users()
  print "Creating Rate setup..."
  test.test_rate_setup()
  #test.datetime_test()
  db.session.commit()

if __name__ == "__main__":
    create_db()