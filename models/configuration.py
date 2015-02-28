from db_manager import db
from pony.orm import Required, Optional


class Configuration(db.Entity):
    key = Required(str, 50, unique=True)
    value = Optional(str, 255)