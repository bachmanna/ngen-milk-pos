from db_manager import db


class FATCollectionRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cattle_type = db.Column(db.String(10))
    min_value = db.Column(db.Float(precision=2))
    max_value = db.Column(db.Float(precision=2))
    rate = db.Column(db.Float(precision=2))


class FATAndSNFCollectionRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cattle_type = db.Column(db.String(10))
    fat_value = db.Column(db.Float(precision=2))
    snf_value = db.Column(db.Float(precision=2))
    rate = db.Column(db.Float(precision=2))


class TS1CollectionRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cattle_type = db.Column(db.String(10))
    fat_value = db.Column(db.Float(precision=2))
    snf_value = db.Column(db.Float(precision=2))
    fat_rate = db.Column(db.Float(precision=2))
    snf_rate = db.Column(db.Float(precision=2))


class TS2CollectionRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cattle_type = db.Column(db.String(10))
    min_value = db.Column(db.Float(precision=2))
    max_value = db.Column(db.Float(precision=2))
    rate = db.Column(db.Float(precision=2))
