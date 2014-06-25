#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       register.py
#
#       Copyright (c) 2014 Ismael Lugo
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import VG
import hashlib
import logger
import db
import re

from userinfo import registered
from userinfo import info


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
            VG.Part[channel] = 'on'
            VG.Join[channel] = 'on'
            VG.Kick[channel] = 'on'
            VG.Op[channel] = 'on'
            VG.Ban[channel] = 'on'
            VG.Voice[channel] = 'on'
            VG.ChMode[channel] = 'on'
            VG.MGame[channel] = 'on'
            db.save('flagsdata', VG.db_flags)
            return True
        else:
            return 'No estas registrado.'
