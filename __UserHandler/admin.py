# -*- coding: utf-8 -*-

import VG
import hashlib
from userinfo import registered
from db import save


def LoginAdmin(username, password):
    if username[1] in VG.ADMIN:
        if VG.ADMIN[username[1]] == hashlib.md5(password).hexdigest():
            info = registered(username[0])
            if info[0] is True:
                if not 'ADMIN' in VG.db_users[info[1]]['other']:
                    VG.db_users[info[1]]['other'].append('ADMIN')
                    save('usersdata', VG.db_users)
    return True if 'ADMIN' in VG.db_users[info[1]]['other'] else False


def LogoutAdmin(username):
    if username[1] in VG.ADMIN:
        info = registered(username[0])
        if info[0] is True:
            if 'ADMIN' in VG.db_users[info[1]]['other']:
                VG.db_users[info[1]]['other'].remove('ADMIN')
                save('usersdata', VG.db_users)
    return True if not 'ADMIN' in VG.db_users[info[1]]['other'] else False


def IsAdmin(username):
    info = registered(username[0])
    if info[0] is True:
        return True if 'ADMIN' in VG.db_users[info[1]]['other'] else False
