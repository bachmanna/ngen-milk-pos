#from pony.orm import *
#db = Database('sqlite', ':memory:')
#db = Database('sqlite', 'test_mpos_db.sqlite', create_db=True)

from flask_sqlalchemy import SQLAlchemy

from web import app

db = SQLAlchemy(app)