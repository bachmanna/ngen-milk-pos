from db_manager import db
from pony.orm import Required, Optional
import datetime


class MilkSale(db.Entity):
    shift = Required(str, 10)

    cattle_type = Required(str, 8)
    qty = Required(float)
    rate = Required(float)
    total = Required(float)

    created_at = Required(datetime.datetime, sql_default='CURRENT_TIMESTAMP')
    created_by = Required(int)
    updated_at = Optional(datetime.datetime)
    updated_by = Optional(int)
    status = Required(bool, default=True)