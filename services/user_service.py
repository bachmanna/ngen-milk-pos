from models.membership import Membership
from db_manager import db


class UserService:
    def __init__(self):
        pass

    def add(self, name, password, email, roles, created_by=1,created_at=None):
        user = self.search(name=name)
        if user:
            print "%s user already exists" % (name)
            return
        str_roles = ",".join([str(x) for x in roles])
        user = Membership(name=name, password=password, email=email, roles=str_roles, created_by=created_by, created_at=created_at, status=True)
        db.session.add(user)
        db.session.commit()
        return user.id

    def get(self, _id):
        user = Membership.query.filter_by(id=_id).one()
        return user

    def update(self, _id, name, password):
        user = self.get(_id)
        if not user:
            return False
        user.name = name
        if password:
            user.password = password
        db.session.commit()
        return True

    def search(self, name=None, email=None):
        query = Membership.query
        if name:
            query = query.filter_by(name=name)
        if email:
            query = query.filter_by(email=email)
        lst = query.all()
        return lst

    def delete(self, _id):
        pass

    def import_data(self, csv_data):
        pass

    def export_data(self):
        return None