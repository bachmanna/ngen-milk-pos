from db_manager import db
from pony.orm import Required, Optional
import datetime

class Membership(db.Entity):
    name = Required(unicode, 100)
    password = Required(str, 100)
    email = Required(str, 255)
    roles = Required(str, 100)

    created_at = Required(datetime.datetime, sql_default='CURRENT_TIMESTAMP')
    created_by = Required(int)
    updated_at = Optional(datetime.datetime)
    updated_by = Optional(int)
    status = Required(bool, default=True)