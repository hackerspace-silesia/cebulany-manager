from flask_security import UserMixin
from flask_security import RoleMixin
from flask_security.datastore import UserDatastore
from flask_security.datastore import Datastore


FAKE_USERS = {'admin' : {'id_': 'admin',
                         'email': 'admin',
                         'password': 'admin'
                         }}


class FakeUser(UserMixin):
    def __init__(self, id_, email, password):
        self.id = email
        self.email = email
        self.password = password
        self.roles = []
        self.active = True


class FakeRole(RoleMixin):
    def __init__(self, name, description):
        self.name = name
        self.description = description


class FakeDatastore(Datastore):
    def __init__(self):
        pass

    def commit(self):
        pass

    def put(self, model):
        raise NotImplementedError

    def delete(self, model):
        raise NotImplementedError


class FakeUserDatastore(FakeDatastore, UserDatastore):
    """A LDAP datastore implementation for Flask-Security.
    """
    def __init__(self):
        FakeDatastore.__init__(self)
        UserDatastore.__init__(self, FakeUser, FakeRole)

    def get_user(self, identifier):
        return self.find_user(identifier)

    def find_user(self, **kwargs):
        if 'id' in kwargs:
            id_ = kwargs['id']
        elif 'email' in kwargs:
            id_ = kwargs['email']

        if id_ in FAKE_USERS:
            return FakeUser(**FAKE_USERS[id_])

        return None

    def find_role(self, role):
        # TODO:
        pass
