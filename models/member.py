from db_manager import db


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    mobile = db.Column(db.String(20), unique=True)
    cattle_type = db.Column(db.String(10))

    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Boolean, default=True)