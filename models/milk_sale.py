from db_manager import db


class MilkSale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shift = db.Column(db.String(10))
    cattle_type = db.Column(db.String(10))

    qty =db.Column(db.Float(precision=2))
    rate = db.Column(db.Float(precision=2))
    total = db.Column(db.Float(precision=2))

    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Boolean, default=True)