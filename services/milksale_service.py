from models import *
from pony.orm import commit, select


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
        commit()
        return sale.id

    def get(self, _id):
        entity = MilkSale[_id]
        return entity

    def search(self, _id=None, shift=None, cattle_type=None, date=None):
        query = select(p for p in MilkSale)
        if _id:
            query = query.filter(lambda x: x.id == _id)
        if shift:
            query = query.filter(lambda x: x.shift == shift)
        if cattle_type:
            query = query.filter(lambda x: x.cattle_type == cattle_type)
        if date:
            query = query.filter(lambda x: x.created_at == date)

        query = query.order_by(MilkSale.created_at.desc())
        lst = query[:]
        return lst

    def update(self, _id, qty, cattle_type):
        sale = self.get(_id)
        sale.set(qty=qty, cattle_type=cattle_type)
        commit()

    def import_data(self, csv_data):
        pass

    def export_data(self):
        return None
