# -*- coding: utf-8 -*-

import VG
import flags
import admin
from logger import log
import register
import threading
import IRC.client
import SessionHandler

from commands.newCommand import (newCommand, ThisCommand, ifOK)

registro = newCommand('register|registro',
    'Registra un Usuario o un Canal.',
    'registro <usuario>')
login = newCommand('login|loguear',
    'Marca como conectado una cuenta de Usuario.',
    'login <contrase\303\261a>')
logout = newCommand('logout|desloguear',
    'Marca como desconectado una cuenta de Usuario.',
    'logout')
access = newCommand('access',
    'Cambia los flags de un usuario en un canal.',
    'access <usuario> (+|-)<Flags>')


class MainLoop(threading.Thread):

    def __init__(self, Out_Queue, SocketObject):
        threading.Thread.__init__(self)
        self.Out_Queue = Out_Queue
        self.SocketObject = SocketObject
        log('Se lanzo el manejador de usuarios.').Logger()

    def run(self):
        while True:
            sc = self.SocketObject.get()
            Client = IRC.client.cliente(sc)
            args = self.Out_Queue.get().split()
            #print '__UserHandler -> ' + ' '.join(args[1:])
            data = args[0].replace('!', ' ').replace('@', ' ').split()
            try:
                if ThisCommand(registro, args[1]):
                    if data[1] == VG.IC['NICK']:
                        if register.RegisterUser(data[0], data[2], args[2]):
                            Client.notice(data[0],
                            "Nick(%s) registrado de forma exitosa." % data[0])
                        else:
                            Client.notice(data[1],
                            "\00304ERROR\3: " +
                            "El nick(%s) ya se encuentra registrado." % data[0])
                    else:
                        src = register.RegisterChannel(data[0], data[1])
                        if src is True:
                            Client.notice(data[0],
                            "Canal(%s) registrado de forma exitosa." % data[1])
                        else:
                            Client.notice(data[0], '\00304ERROR\3: %s' % src)
                            del src
                if ThisCommand(login, args[1]):
                    Status = SessionHandler.login(data[0], data[2], args[2])
                    if Status is None:
                        Client.notice(data[0], "Logueado de forma exitosa.")
                    else:
                        Client.notice(data[0], "\00304ERROR\3: %s" % Status)
                        del Status
                if ThisCommand(logout, args[1]):
                    Status = SessionHandler.logout(data[0], data[2])
                    if Status is None:
                        Client.notice(data[0], "Deslogueado de forma exitosa.")
                    else:
                        Client.notice(data[0], "\00304ERROR\3: %s" % Status)
                        del Status
                if ThisCommand(access, args[1]):
                    if ifOK(data, 'S', sc):
                        if args[3] != 'list':
                            __Flags = flags.Flags(args[2], data[1], args[3]).SetFlags()
                            if not __Flags:
                                __Flags = flags.Flags(args[2], data[1], args[3]).SetFlags()
                                Client.notice(data[0], __Flags)
                            else:
                                Client.notice(data[0], __Flags)
                        elif args[3] == 'list':
                            Client.notice(data[0], '%s: %s(+%s)' % (data[1],
                            args[2], ''.join(flags.Flags(args[2], data[1],
                            args[3]).FlagsList())))

            except IndexError:
                Client.notice(data[0], "\00304ERROR\3: Faltan parametros")
            #except:
             #   Client.notice(data[1],
             #   "\2\00304ERROR FATAL\3\2: Sistema de Usuarios")
        log('El manejador de usuarios a finalizado').LogError()

