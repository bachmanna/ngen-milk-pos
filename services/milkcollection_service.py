from models import *
from pony.orm import commit, select


class MilkCollectionService:
    def __init__(self):
        pass

    def add(self, entityDic):
        collection = MilkCollection(**entityDic)
        commit()
        return collection.id

    def get(self, _id):
        entity = MilkCollection[_id]
        # entity.member.name
        return entity

    def search(self, member_id=None, shift=None, date=None):
        query = select(p for p in MilkCollection)
        if member_id:
            query = query.filter(lambda x: x.member.id == member_id)
        if shift:
            query = query.filter(lambda x: x.shift == shift)
        if date:
            query = query.filter(lambda x: x.created_at == date)

        query = query.order_by(MilkCollection.created_at.desc())
        lst = query[:]
        return lst

    def update(self, _id, entityDic):
        collection = self.get(_id)
        collection.set(**entityDic)
        commit()

    def import_data(self, csv_data):
        pass

    def export_data(self):
        return None
