from db_manager import db
from pony.orm import Required, Optional, Set
import datetime


class Member(db.Entity):
    name = Required(unicode, 100)
    mobile = Required(str, 13, unique=True)
    cattle_type = Required(str, 8)

    created_at = Optional(datetime.datetime, sql_default='CURRENT_TIMESTAMP')
    created_by = Optional(int)
    updated_at = Optional(datetime.datetime)
    updated_by = Optional(int)
    status = Required(bool, default=True)

    milk_collections = Set("MilkCollection")