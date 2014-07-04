# -*- coding: utf-8 -*-

import VG
import re

from __UserHandler import (flags, userinfo)
from IRC.client import cliente

CommandList = []


def newCommand(CommandName, Descripcion='', Sintax=''):
    Sintax = ' \2\00301Sintax:\3 %s%s' % (VG.Config['COMD'], Sintax)
    a = [re.compile(r'\%s(%s)' % (VG.Config['COMD'], CommandName)), CommandName,
        Descripcion + Sintax]
    CommandList.append(a)
    a = CommandList.index(a)
    return a


def ThisCommand(posc, CommandName):
    return True if CommandList[posc][0].match(CommandName) else False


def ifOK(data, flagname, SocketObject):
    ERROR = []
    if userinfo.registered(data[0])[0]:
        if flags.Flags(data[0], data[1], '').ChannelRegistered():
            if flagname in flags.Flags(data[0], data[1], '').FlagsList():
                if userinfo.info(data[0], 'status') == 'conectado':
                    if userinfo.info(data[0], 'hostname') == data[2]:
                        return True
                    else:
                        ERROR.append('\00304ERROR\3: El host no coincide.')
                else:
                    ERROR.append('\00304ERROR\3: Estas desconectado.')
            else:
                ERROR.append('\00304ERROR\3: Usted no está autorizado para ' +
                'realizar esta operación. \2\00301Requiere(+%s)' % flagname)
        else:
            ERROR.append('\00304ERROR\3: Canal(%s) no registrado.' % data[0])
    else:
        ERROR.append('\00304ERROR\3: No estas registrado.')
    client = cliente(SocketObject)
    for i in ERROR:
        client.notice(data[0], i)
