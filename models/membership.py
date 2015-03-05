from db_manager import db
from pony.orm import Required, Optional
import datetime

class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(255), unique=True)
    roles = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Boolean, default=True)