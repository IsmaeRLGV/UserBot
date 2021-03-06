# -*- coding: utf-8 -*-

import VG
import hashlib
import logger
import db
import re

from userinfo import (registered, info)


def RegisterUser(username, hostname, password):
    if not registered(username)[0]:
        username = username.replace('\\', '\\').replace('{', '\{').replace(
        '}', '\}').replace('[', '\[',).replace(']', '\]').replace('|', '\|'
        ).replace('^', '\^').replace('.', '\.')
        Rusername = re.compile(r'' + username, re.IGNORECASE)
        VG.db_users.append({
        'username': (Rusername, username),
        'hostname': hostname,
        'password': hashlib.md5(password).hexdigest(),
        'status': 'conectado',
        'other': []
        })
        db.save('usersdata', VG.db_users)
        logger.log('Intento de Registro: %s... Completado.' % username).Logger()
        return True
    else:
        return 'El nick(%s) ya esta registrado.' % username


def RegisterChannel(username, channel):
    try:
        for j in VG.db_flags.keys():
            if j.match(channel):
                raise StopIteration('El canal(%s) ya se encuentra registrado.' % channel)
        Ch = channel
    except StopIteration as e:
        logger.log(e).LogError()
        return e
    else:
        if registered(username)[0]:
            channel = channel.replace('\\', '\\').replace('{', '\{').replace(
                '}', '\}').replace('[', '\[',).replace(']', '\]').replace(
                '|', '\|').replace('^', '\^').replace('.', '\.')
            channel = re.compile(r'' + channel, re.IGNORECASE)
            VG.db_flags[channel] = {info(username, 'username') : list('Scfkrmovs')}
            VG.Anti[channel] = 'on'
            VG.AntiOP[channel] = 'off'
            VG.Me[channel] = 'off'
            VG.AntiFlood[channel] = 'off'
            VG.ABW[channel] = 'off'
            VG.Google[channel] = 'on'
            VG.UrlOpen[channel] = 'on'
            db.save('flagsdata', VG.db_flags)
            VG.CHANNELS += Ch + ','
            sc = file('DB/CONFIG/CHANNELS', 'w')
            sc.write('"""{0}"""'.format(VG.CHANNELS))
            sc.close()
            return True
        else:
            return 'No estas registrado.'
