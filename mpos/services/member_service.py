from models.member import Member
from db_manager import db
from datetime import datetime

class MemberService:
    def __init__(self):
        pass

    def add(self, name, cattle_type, mobile, created_by, created_at, _id=None):
        if _id:
            member = Member(id=_id, name=name, cattle_type=cattle_type, mobile=mobile, created_by=created_by, created_at=created_at, status=True)
        else:
            member = Member(name=name, cattle_type=cattle_type, mobile=mobile, created_by=created_by, created_at=created_at, status=True)
        db.session.add(member)
        db.session.commit()
        return member.id

    def get(self, _id):
        member = Member.query.filter_by(id=_id).first()
        return member

    def update(self, _id, name, cattle_type, mobile):
        member = self.get(_id)
        if not member:
            return False
        member.name = name
        member.mobile = mobile
        member.cattle_type = cattle_type
        db.session.commit()
        return True

    def search(self, name=None, mobile=None, cattle_type=None):
        query = Member.query
        if name:
            query = query.filter_by(name=name)
        if mobile:
            query = query.filter_by(mobile=mobile)
        if cattle_type:
            query = query.filter_by(cattle_type=cattle_type)
        # query = query.order_by(Member.created_at.desc())
        query = query.order_by(Member.id)
        lst = query.all()
        return lst

    def delete(self, _id):
        pass

    def import_data(self, csv_data):
        pass

    def export_data(self):
        return None
