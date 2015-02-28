from models.membership import Membership
from pony.orm import commit, select


class UserService:
    def __init__(self):
        pass

    def add(self, name, password, email, roles, created_by=1):
        user = self.search(name=name)
        if user:
            print "%s user already exists" % (name)
            return
        str_roles = ",".join([str(x) for x in roles])
        user = Membership(name=name, password=password, email=email, roles=str_roles, created_by=created_by, status=True)
        commit()
        return user.id

    def get(self, _id):
        user = Membership[_id]
        return user

    def update(self, _id, name, password):
        user = self.get(_id)
        if not user:
            return False
        user.name = name
        if password:
            user.password = password
        commit()
        return True

    def search(self, name=None, email=None):
        query = select(p for p in Membership)
        if name:
            query = query.filter(lambda x: x.name == name)
        if email:
            query = query.filter(lambda x: x.email == email)
        lst = query[:]
        return lst

    def delete(self, _id):
        pass

    def import_data(self, csv_data):
        pass

    def export_data(self):
        return None