import os

from flask_security import Security

from cebulany.auth.ldap_client import LdapDB
from cebulany.auth import ldap_store
from cebulany.auth import fake


def init_ldap_auth(app):
    server = os.environ.get('LDAP_SERVER', None)
    user = os.environ.get('LDAP_USER', None)
    password = os.environ.get('LDAP_PASSWORD', None)
    user_dn = os.environ.get('LDAP_USER_DN', None)
    role_dn = os.environ.get('LDAP_ROLE_DN', None)
    #db = LdapDB('ldap://172.17.0.2', 'cn=admin,dc=example,dc=org', 'admin', 'ou=Members,dc=example,dc=org', 'ou=Roles,dc=example,dc=org')
    db = LdapDB(server, user, password, user_dn, role_dn)

    user_datastore = ldap_store.LdapUserDatastore(db)
    return Security(app, user_datastore)

def init_fake_auth(app):
    user_datastore = fake.FakeUserDatastore()
    return Security(app, user_datastore)

def init_auth(app):
    if os.environ.get('LDAP_SERVER', None):
        init_ldap_auth(app)
    else:
        init_fake_auth(app)
