#!/usr/bin/python3

import ldap3, os

# return an empty string for success
# a fail message otherwise
def authenticate(zid, zpass, bind_password=None, debug=False):
    server_uri = 'ldaps://ad.unsw.edu.au'
    bind_dn = 'svcCSEMaestro@ad.unsw.edu.au'
    base_dn = 'ou=IDM_People,ou=IDM,dc=ad,dc=unsw,dc=edu,dc=au'
    search_filter = '(sAMAccountName=%s)' % zid
    attributes = ["displayName", "mail"]
    try:
        if not bind_password:
            with open(os.path.join(os.environ.get('HOME', '.'), '.unsw_ldap_password')) as f:
                bind_password = f.read().strip()
        server = ldap3.Server(server_uri)
        connection = ldap3.Connection(server, user=bind_dn, password=bind_password, auto_bind=True)
        connection.search(base_dn, search_filter, attributes=attributes)
        if len(connection.response) != 1:
            return 'Authentication failed, search returned incorrect number of matches for zid: ', + str(connection.response)
        c = ldap3.Connection(server, user=connection.response[0]['dn'], password=zpass)
        if c.bind():
            fail_message = ''
            c.unbind()
        else:
            fail_message = 'zpass/zpass did not authenticate'
        connection.unbind()
        return fail_message
    except (ldap3.LDAPException,OSError) as e:
        return 'Authentication failed due to exception: '+ str(e) + zpass

if __name__ == "__main__":
    zid = input()
    zpass= input()
    fail_message = authenticate(zid, zpass)
    if fail_message == '':
        print("Authenticated")
    else:
        print("Authentication failed")
