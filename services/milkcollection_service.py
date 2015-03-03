from models import *
from pony.orm import commit, select


class MilkCollectionService:
    def __init__(self):
        pass

    def add(self, entity):
        collection = MilkCollection(member=entity["member"]
            ,shift=entity["shift"],fat = entity["fat"],snf = entity["snf"]
            ,clr = entity["clr"],aw = entity["aw"],qty = entity["qty"]
            ,rate = entity["rate"],total = entity["total"],created_by = entity["created_by"]
            ,created_at = entity["created_at"],status = entity["status"])
        commit()
        return collection.id

    def get(self, _id):
        entity = MilkCollection[_id]
        # entity.member.name
        return entity

    def search(self, member_id=None, shift=None, created_at=None):
        query = select(p for p in MilkCollection)
        if member_id:
            query = query.filter(lambda x: x.member.id == member_id)
        if shift:
            s = unicode(shift)
            query = query.filter(shift=s)
        if created_at:
            query = query.filter(lambda x: x.created_at.date() == created_at)

        query = query.order_by(MilkCollection.created_at.desc())
        lst = query[:]
        return lst

    def update(self, _id, entity):
        collection = self.get(_id)
        #collection.member = entity["member"]
        collection.shift = entity["shift"]
        collection.fat = entity["fat"]
        collection.snf = entity["snf"]
        collection.clr = entity["clr"]
        collection.aw = entity["aw"]
        collection.qty = entity["qty"]
        collection.rate = entity["rate"]
        collection.total = entity["total"]
        commit()

    def import_data(self, csv_data):
        pass

    def export_data(self):
        return None
