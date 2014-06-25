# -*- coding: utf-8 -*-

import VG


def FlagsList(channel):
    try:
        for j in VG.db_flags.keys():
            if j.match(channel):
                CR = (True, j)
                raise StopIteration
        CR = (False)
    except StopIteration:
        pass
    if CR[0]:
        F = ['\002\00301Lista de FLAGS: \00302%s']
        for i in VG.db_flags[CR[1]].items():
            F.append("\002\00301%s - %s" % (i[0][1], "".join(i[1])))
        return F


def registered(username):
    for i in VG.db_users:
        try:
            if i['username'][0].match(username):
                return (True, VG.db_users.index(i))
        except KeyError:
            pass
    return (False, None)


def info(username, key=""):
    Registered = registered(username)
    if Registered[0]:
        if VG.db_users[Registered[1]]['username'][0].match(username):
            return VG.db_users[Registered[1]][key]
    else:
        return 'El usuario ' + username + 'no se encuentra registrado.'
