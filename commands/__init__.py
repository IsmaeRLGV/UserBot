# -*- coding: utf-8 -*-

import Google
import AutoModerator
import wikipedia
import tweepy
import logger
import threading
import VG
import IRC

import time

from __UserHandler import admin
from newCommand import (newCommand, ThisCommand, ifOK, CommandList)

# Comandos sobre el IRC
kick = newCommand('kick|k',
      'Expulsa a un usuario de un canal especifico.',
      'kick <usuario> <Comentario Opciona>')
remove = newCommand('remove|rm',
        'Saca a un usuario de un canal especifico.',
        'remove <usuario>')
op = newCommand('op',
    'Otorga estado de operador a un usuario.',
    'op <usuario>')
deop = newCommand('deop',
    'Quita estado de operador a un usuario.',
    'deop <usuario>')
voice = newCommand('voice|voice',
    'Otorga voz a un usuario.',
    'voice <usuario>')
devoice = newCommand('devoice|dv',
    'Quita voz a un usuario.',
    'devoice <usuario> ó simplemente devoice')
ban = newCommand('ban|b',
    'Banea a un usuario de un canal en especifico.',
    'b <nick!ident@host>')
unban = newCommand('unban|ub',
    'Quita veto a un usuario en un canal especifico.',
    'ub <nick!ident@host>')
part = newCommand('part|p',
    'Hace que el Bot abandone un canal.',
     'p <canal> <Comentario Opcional>')
join = newCommand('join|j',
    'Hace que el Bot ingrese a un canal.',
    'j <canal> <Clave Opcional>')

# Comandos sobre los Servicios
flags = newCommand('flags|fl',
    'Cambia los Flags de un usuario via ChanServ',
    'flags <usuario> <(+|-)<FLAGS>')
Set = newCommand('set|st',
    'permite configurar indicadores de control de canales via ChanServ',
    'set <Target> (on|off)')

# Otros comandos.
traducir = newCommand('traducir|translate|tr',
    'Traduce una frase de un idioma a otro.',
    'tr <in> <out> <Frase>')
imagen = newCommand('imagen|img',
    'Busca una imagen de un Objeto Especificado.',
    'img <Objeto>')
google = newCommand('google|gl',
    'Realiza una busqueda en google de algo en concreto.',
    'gl <Objeto>')
wiki = newCommand('wiki|wikipedia',
    'Realiza una busqueda en wikipedia de algo en concreto.',
    'wiki <Objeto>')
ip = newCommand('ip',
    'Geolocaliza una ip.',
    'ip <IP>')
twitter = newCommand('tweet|twitter',
    'Publica un nuevo tweet.',
    'tweet <Mensaje>')
endis = newCommand('ctrl|control',
    'Regula o controla el uso de algunos comandos en un canal.',
    'control <Comando> on|off')
ayuda = newCommand('ayuda|help',
    'muestra la ayuda disponible de un comando.',
    'ayuda <Comando>')
red = newCommand('red|irc',
    'Establece o desconecta una conexion a algun servidor IRC.',
    'red add|del <server>:<port>:<sasluse>')

wikipedia.set_lang('es')


class MainLoop(threading.Thread):

    def __init__(self, Out_Queue, SocketObject):
        threading.Thread.__init__(self)
        self.Out_Queue = Out_Queue
        self.SocketObject = SocketObject
        logger.log('Se lanzo el manejador de comandos.').Logger()

    def run(self):
        af = {'UR': time.time(), 'TM': 4, 'MM': 6, 'MR': 0, 'UU': ''}
        while True:
            sc = self.SocketObject.get()
            Client = IRC.client.cliente(sc)
            args = self.Out_Queue.get().split()
            #print 'Commands -> ' + ' '.join(args[1:])
            data = args[0].replace('!', ' ').replace('@', ' ').split()
            # Procesando Comandos Sobre el IRC
            try:
                if ThisCommand(kick, args[1]):
                    if ifOK(data, 'k', sc):
                        if args[2] != VG.IC['NICK']:
                            Client.kick(data[1], args[2], ' '.join(args[3:]))
                if ThisCommand(remove, args[1]):
                    if ifOK(data, 'k', sc):
                        if args[2] != VG.IC['NICK']:
                            Client.remove(data[1], args[2], ' '.join(args[3:]))
                if ThisCommand(op, args[1]):
                    if ifOK(data, 'o', sc):
                        try: args[2]
                        except IndexError: Client.mode(data[1], '+o', data[0])
                        else: Client.mode(data[1], '+o', args[2])
                if ThisCommand(deop, args[1]):
                    if ifOK(data, 'o', sc):
                        try: Client.mode(data[1], '-o', args[2])
                        except IndexError: Client.mode(data[1], '-o', data[0])
                if ThisCommand(voice, args[1]):
                    if ifOK(data, 'v', sc):
                        try: args[2]
                        except IndexError: Client.mode(data[1], '+v', data[0])
                        else: Client.mode(data[1], '+v', args[2])
                if ThisCommand(devoice, args[1]):
                    if ifOK(data, 'v', sc):
                        try: args[2]
                        except IndexError: Client.mode(data[1], '-o', data[0])
                        else: Client.mode(data[1], '-v', data[0])
                if ThisCommand(ban, args[1]):
                    if ifOK(data, 'r', sc):
                        Client.mode(data[1], '+b', args[2])
                if ThisCommand(unban, args[1]):
                    if ifOK(data, 'r', sc):
                        Client.mode(data[1], '-b', args[2])
                if ThisCommand(part, args[1]):
                    if ifOK(data, 'c', sc):
                        Client.part(args[2], ' '.join(args[3:]))
                if ThisCommand(join, args[1]):
                    if ifOK(data, 'c', sc):
                        Client.Join(args[2], ' '.join(args[3:]))
                if ThisCommand(endis, args[1]):
                    try:
                        for j in eval('VG.%s' % args[2]).keys():
                            if j.match(data[1]):
                                raise StopIteration
                    except StopIteration:
                        h={'on': '\00303on', 'off': '\00304off'}
                        if args[3] in ['on', 'off']:
                            eval('VG.%s' % args[2])[j] = args[3]
                            Client.notice(data[1], '\2\00301%s %s' % (args[2], h[args[3]]))
                    except NameError:
                        Client.notice(data[1], '\00304ERROR\3:%s No existe.' % args[2])
                    else:
                        Client.notice(data[1], '\00304ERROR\3: ¿El canal no esta registrado?')
                if ThisCommand(wiki, args[1]):
                    try:
                        a='\2\00301%s\2\3: %s' % (args[2], wikipedia.summary(args[2], 1))
                        Client.notice(data[1], a.encode('UTF-8'))
                    except wikipedia.exceptions.PageError:
                        Client.notice(data[1], '\00304ERROR\3: Pruebe con -> ' +
                        "\2\00304, \2\3".join(wikipedia.search(args[2])))
                    except:
                        Client.notice(data[1], 'Ohh Internet lento :(')
                if ThisCommand(ayuda, args[1]):
                    try:
                        commandls = {}
                        for i in CommandList:
                            commandls[i[1]] = i[2]
                        Client.notice(data[1], commandls.get(args[2],
                        '\00304ERROR\3: El comando no existe'))
                    except IndexError:
                        pr = 'IRCBot. \2UserBot-3.9.7\2 by Kwargs.'
                        pr += ' Inicio de comandos: %s' % VG.comd
                        pr += '. Comandos disponibles: '
                        Client.notice(data[1], pr)
                        Client.notice(data[1], ', '.join(commandls.keys()))
                        Client.notice(data[1], '\2Fin de la ayuda.')
                if ThisCommand(traducir, args[1]):
                    Client.notice(data[1], Google.translate(' '.join(args[4:]), args[2], args[3]).encode('UTF-8')
                if ThisCommand(red, args[1]):
                    info = args[3].split(':')
                    if args[2] == 'add':
                        IRC.connection.Loop_sc(info[0], int(info[1]), bool(info[2])).start()

            except IndexError:
                Client.notice(data[0], "\00304ERROR\3: Faltan parametros")
            except:
                Client.notice(data[1],
                "\2\00304ERROR FATAL\3\2: Sistema de Comandos")
            try:
                for i in VG.AntiFlood.keys():
                    if i.match(data[1]):
                        raise StopIteration
            except StopIteration:
                if VG.AntiFlood[i] == 'on':
                    t = (af['UR'] - time.time()) * 1
                    if t < af['TM'] and af['MR'] >= af['MM'] and data[0] == af['UU']:
                        Client.kick(data[1], data[0], '\2\00300,04ALTO AL FLOOD')
                    elif t > af['TM'] and af['MR'] <= af['MM'] and data[0] == af['UU']:
                        af['UR'] = time.time()
                        af['MR'] = 1
                    elif t < af['TM'] and af['MR'] <= af['MM'] and data[0] == af['UU']:
                        af['MR'] += 1
                    elif data[0] != af['UU']:
                        af['UR'] = time.time()
                        af['MR'] = 1
                        af['UU'] = data[0]
            except IndexError:
                pass
