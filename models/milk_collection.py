from db_manager import db
from member import Member
from pony.orm import Required, Optional
import datetime


class MilkCollection(db.Entity):
    member = Required(Member, lazy=False)
    shift = Required(str, 10)

    fat = Required(float)
    snf = Required(float)
    qty = Required(float)
    clr = Required(float)
    aw = Required(float)
    rate = Required(float)
    total = Required(float)

    created_at = Required(datetime.datetime, sql_default='CURRENT_TIMESTAMP')
    created_by = Required(int)
    updated_at = Optional(datetime.datetime)
    updated_by = Optional(int)
    status = Required(bool, default=True)