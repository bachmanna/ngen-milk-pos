from models import *
from db_manager import db
from sqlalchemy import Date, cast


class MilkSaleService:
    def __init__(self):
        pass

    def add(self, shift, qty, cattle_type, rate, created_by):
        total = rate * qty
        sale = MilkSale(shift=shift,
                        qty=qty,
                        cattle_type=cattle_type,
                        rate=rate,
                        total=total,
                        created_by=created_by)
        db.session.add(sale)
        db.session.commit()
        return sale.id

    def get(self, _id):
        entity = MilkSale.query.filter_by(id=_id).one()
        return entity

    def search(self, _id=None, shift=None, cattle_type=None, date=None):
        query = MilkSale.query
        if _id:
            query = query.filter_by(id=_id)
        if shift:
            query = query.filter_by(shift=shift)
        if cattle_type:
            query = query.filter_by(cattle_type=cattle_type)
        if date:
            query = query.filter(cast(MilkSale.created_at,Date) == created_at)

        query = query.order_by(MilkSale.created_at.desc())
        lst = query.all()
        return lst

    def update(self, _id, qty, cattle_type):
        sale = self.get(_id)
        sale.set(qty=qty, cattle_type=cattle_type)
        db.session.commit()

    def import_data(self, csv_data):
        pass

    def export_data(self):
        return None
