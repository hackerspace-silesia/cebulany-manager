import json
import ldap
import ldap.modlist as modlist


USER_DN = 'ou=Members,dc=example,dc=org'
ROLE_DN = 'ou=Roles,dc=example,dc=org'


class LdapDB(object):
    def __init__(self, address, username, password, user_dn, role_dn):
        self._l = ldap.initialize(address)
        #self._l.start_tls_s()
        self._l.simple_bind(username, password)
        self.user_dn = user_dn
        self.rolde_dn = role_dn

    def find_user(self, login):
        cn = 'cn={}'.format(login)
        users = self._l.search_st(self.user_dn, ldap.SCOPE_SUBTREE, filterstr=cn)
        if not users:
            return None
        if len(users) > 1:
            raise 'More than one users with login {}'.format(login)
        return users[0][1]

    def find_role(self, role):
        raise NotImplementedError

    def create_user(self, name, surname, mail, phone, joined):
        cn = mail
        dn = 'cn={0},{1}'.format(cn, self.user_dn)
        attrs = {}
        attrs['objectclass'] = ['top', 'inetOrgPerson']
        attrs['cn'] = cn
        attrs['mail'] = mail
        attrs['givenName'] = name
        attrs['sn'] = surname
        attrs['mobile'] = phone
        attrs['description'] = json.dumps({'joined': joined})
        ldif = modlist.addModlist(attrs)
        self._l.add_s(dn, ldif)

    def create_role(self, name, description):
        raise NotImplementedError
