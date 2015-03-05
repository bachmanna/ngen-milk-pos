from db_manager import db


class MilkCollection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shift = db.Column(db.String(80))
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    member = db.relationship('Member',
        backref=db.backref('milk_collections', lazy='dynamic'))

    fat = db.Column(db.Float(precision=2))
    snf = db.Column(db.Float(precision=2))
    qty = db.Column(db.Float(precision=2))
    clr = db.Column(db.Float(precision=2))
    aw = db.Column(db.Float(precision=2))
    rate = db.Column(db.Float(precision=2))
    total = db.Column(db.Float(precision=2))

    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Boolean, default=True)