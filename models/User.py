from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id=None, name=None, email=None, roles=[]):
        self.id = user_id
        self.user_id = user_id
        self.name = name
        self.email = email
        self.roles = roles

    def is_authenticated(self):
        return self.id is not None

    def is_anonymous(self):
        return self.email is None
