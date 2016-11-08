from flask_security import UserMixin
from flask_security import RoleMixin
from flask_security.datastore import UserDatastore
from flask_security.datastore import Datastore


class LdapUser(UserMixin):
    def __init__(self, id_, email, password):
        self.id = email
        self.email = email
        self.password = password
        # TODO:
        self.roles = []
        self.active = True


class LdapRole(RoleMixin):
    def __init__(self, name, description):
        self.name = name
        self.description = description


class LdapDatastore(Datastore):
    def __init__(self, db):
        self.db = db

    def commit(self):
        pass

    def put(self, model):
        raise NotImplementedError

    def delete(self, model):
        raise NotImplementedError


class LdapUserDatastore(LdapDatastore, UserDatastore):
    """A LDAP datastore implementation for Flask-Security.
    """
    def __init__(self, db):
        LdapDatastore.__init__(self, db)
        UserDatastore.__init__(self, LdapUser, LdapRole)

    def get_user(self, identifier):
        if self._is_numeric(identifier):
            pass
        else:
            return self.find_user(identifier)

    def _is_numeric(self, value):
        try:
            int(value)
        except (TypeError, ValueError):
            return False
        return True

    def find_user(self, **kwargs):
        if 'id' in kwargs:
            id = kwargs['id']
        elif 'email' in kwargs:
            id = kwargs['email']
        attr = self.db.find_user(id)
        if attr:
            return LdapUser(id_=attr['cn'][0],
                            email=attr['mail'][0],
                            password=attr['userPassword'][0])
                            # TODO:roles=[]
        return None

    def find_role(self, role):
        # TODO:
        attr = self.db.find_role(role)
