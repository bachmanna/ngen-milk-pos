from models.member import Member
from pony.orm import commit, select


class MemberService:
    def __init__(self):
        pass

    def add(self, name, cattle_type, mobile, _id=None):
        if _id:
            member = Member(id=_id, name=name, cattle_type=cattle_type, mobile=mobile, status=True)
        else:
            member = Member(name=name, cattle_type=cattle_type, mobile=mobile, status=True)
        commit()
        return member.id

    def get(self, _id):
        member = Member[_id]
        return member

    def update(self, _id, name, cattle_type, mobile):
        member = self.get(_id)
        if not member:
            return False
        member.name = name
        member.mobile = mobile
        member.cattle_type = cattle_type
        commit()
        return True

    def search(self, name=None, mobile=None, cattle_type=None):
        query = select(p for p in Member)
        if name:
            query = query.filter(lambda x: x.name == name)
        if mobile:
            query = query.filter(lambda x: x.mobile == mobile)
        if cattle_type:
            query = query.filter(lambda x: x.cattle_type == cattle_type)
        query = query.order_by(Member.created_at.desc())
        lst = query[:]
        return lst

    def delete(self, _id):
        pass

    def import_data(self, csv_data):
        pass

    def export_data(self):
        return None
