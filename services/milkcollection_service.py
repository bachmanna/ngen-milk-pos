from models import *
from datetime import datetime, date
from db_manager import db
from sqlalchemy import Date, cast

class MilkCollectionService:
    def __init__(self):
        pass

    def add(self, entity):
        collection = MilkCollection(member=entity["member"]
            ,shift=entity["shift"],fat = entity["fat"],snf = entity["snf"]
            ,clr = entity["clr"],aw = entity["aw"],qty = entity["qty"]
            ,rate = entity["rate"],total = entity["total"],created_by = entity["created_by"]
            ,created_at = entity["created_at"],status = entity["status"])
        db.session.add(collection)
        db.session.commit()
        return collection.id

    def get(self, _id):
        entity = MilkCollection.query.filter_by(id=_id).one()
        # entity.member.name
        return entity

    def search(self, member_id=None, shift=None, created_at=None):
        query = MilkCollection.query
        if member_id and isinstance(member_id, int):
            query = query.filter_by(member_id=member_id)
        if shift and (isinstance(shift, str) or isinstance(shift, unicode)) and len(shift) > 0:
            query = query.filter_by(shift=shift)
        if created_at and isinstance(created_at, date):
            query = query.filter(cast(MilkCollection.created_at,Date) == cast(created_at,Date))
        query = query.order_by(MilkCollection.created_at.desc())
        lst = query.all()
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
        db.session.commit()

    def import_data(self, csv_data):
        pass

    def export_data(self):
        return None
