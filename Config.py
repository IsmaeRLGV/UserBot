# -*- coding: utf-8 -*-

import VG
import hashlib
import cPickle as pickle
import threading
import IRC.connection
from os.path import exists
from base64 import decodestring as decodificar
import commands
import __UserHandler

SOURCES = ['DB/CONFIG/SC',
           'DB/CONFIG/IC',
           'DB/CONFIG/ADMIN',
           'DB/CONFIG/TWITTER',
           'DB/CONFIG/CHANNELS',
           'DB/DB/CTRL.db',
           'DB/DB/usersdata.db',
           'DB/DB/flagsdata.db']

status = []


def exist(filename):
    if exists(filename):
        status.append((filename, True))
        return True
    else:
        status.append((filename, False))
        return False


def LoadConfig():
    if exist(SOURCES[0]) is True:
        VG.SC = eval(open(SOURCES[0]).read().replace('\n', ' '))
    if exist(SOURCES[1]) is True:
        VG.IC = eval(open(SOURCES[1]).read().replace('\n', ' '))
    if exist(SOURCES[2]) is True:
        VG.ADMIN = eval(open(SOURCES[2]).read().replace('\n', ' '))
    if exist(SOURCES[3]) is True:
        VG.TWITTER = eval(open(SOURCES[3]).read().replace('\n', ' '))
    if exist(SOURCES[4]) is True:
        VG.CHANNELS = eval(open(SOURCES[4]).read().replace('\n', ' '))
    return status


def SaveConfig(l='all', pic=False):
    if l != 'all':
        sc = file(l, 'w')
        sc.write('{0}'.format(eval('VG.' + l.replace('/', ' ').split()[2])))
        sc.close()
    elif l == 'all':
        for l in SOURCES[0:5]:
            sc = file(l, 'w')
            sc.write('{0}'.format(eval('VG.' + l.replace('/', ' ').split()[2])))
            sc.close()

lsc = {}


def AdminConfigure():
    if type(VG.ADMIN) != type(None):
        return True
    else:
        VG.ADMIN = {}
        return True
    if len(VG.ADMIN) > 0:
        return True
    else:
        return False


def ConfigAdmin(NICK, password):
    if AdminConfigure() is True:
        if not NICK in VG.ADMIN.keys():
            if len(password) >= 10:
                VG.ADMIN[NICK] = hashlib.md5(password).hexdigest()
                return True
    return False


def ControlSave():
    filename = file(SOURCES[5], 'w')
    pickle.dump({'Anti': VG.Anti,
                 'AntiOP': VG.AntiOP,
                 'ABW': VG.ABW,
                 'AntiFlood': VG.AntiFlood,
                 'Me': VG.Me,
                 'Google': VG.Google,
                 'UrlOpen': VG.UrlOpen}, filename)
    filename.close()


def ControlLoad():
    return pickle.load(file(SOURCES[5]))


def LoginInServer(sc):
    lis = ['SASL', 'USERNAME', 'PASSWORD']
    try:
        OK = 0
        recv = decodificar(lsc[sc][0].recv(1024)).split()
        print recv
        if recv[0] in lis:
            if recv[0] == lis[0]:
                if recv[1] == lis[1]:
                    if recv[2] in VG.ADMIN:
                        OK += 1
                        if recv[3] == lis[2]:
                            if VG.ADMIN[recv[2]] == hashlib.md5(recv[4]).hexdigest():
                                OK += 1
    except IndexError:
        lsc[sc][0].close()
        del lsc[sc]
        print 'Rechazado'
    else:
        if OK == 2:
            del lsc[sc][1]
            lsc[sc].append(True)
            print 'Aceptado'


def CommandLine(sc):
    while True:
        recv = sc.recv(1024)
        if len(recv) > 0:
            args = eval(decodificar(recv))
            try:
                VG.uhso.put(args['server'])
                VG.cso.put(args['server'])
                VG.uhoq.put('%s!%s@%s %s' % (
                args['user'], args['target'], args['host'], args['msg']))
                VG.coq.put('%s!%s@%s %s' % (
                args['user'], args['target'], args['host'], args['msg']))
            except KeyError:
                VG.uhoq.put('_-Null-_!_-Null-_@localhost None None')
                VG.coq.put('_-Null-_!_-Null-_@localhost None None')
            except:
                sc.send('ERROR FATAL: Cerrando conexion.\n')
                lsc[sc][0].close()
                del lsc[sc]
        else:
            lsc[sc][0].close()
            print 'Se ha desconectado: %s' % lsc[sc][1]
            del lsc[sc]


def ServerConfig(server='localhost', port=10024, listen=5):
    import socket
    print('Servidor de administradores lanzado.')
    s = socket.socket()
    s.bind((server, port))
    s.listen(listen)
    while True:
        sc, addr = s.accept()
        lsc[addr[1]] = [sc, False]
        print addr
        login = threading.Thread(target=LoginInServer, args=(addr[1], ))
        login.start()
        login.join(10)
        if lsc[addr[1]][1] is True:
            lsc[addr[1]][0].send('Bienvenido\n')
            lsc[addr[1]][0].send('Lista de redes disponibles:\n')
            servers = list(VG.lssc.keys())
            servers.append('sc - Su conexion.\n')
            for X in servers:
                lsc[addr[1]][0].send('    ' + X)
            threading.Thread(target=CommandLine, args=(addr[1], )).start()
        elif lsc[addr[1]][1] is False:
            lsc[addr[1]][0].close()
            del lsc[addr[1]]


def main():
    lc = LoadConfig()
    print 'Estado de la configuración:'
    for l in lc:
        print('    %-20s [%s]' % tuple(l))
    if lc[2][1] is False:
        print('Cree un usuario administrador.')
        print('Administrador configurado [%s]' % ConfigAdmin(
            raw_input('Nick: '), raw_input('Password:')))
        SaveConfig(SOURCES[2])
    elif not AdminConfigure():
        print('Cree un usuario administrador.')
        print('Administrador configurado [%s]' % ConfigAdmin(
            raw_input('Nick: '), raw_input('Password: ')))
        SaveConfig(SOURCES[2])
    if lc[1][1] is False:
        print('Informacion de Conexion.')
        VG.IC['NICK'] = raw_input('NICK: ')
        VG.IC['IDENT'] = raw_input('IDENT: ')
        VG.IC['REALNAME'] = raw_input('REALNAME: ')
        VG.IC['NP'] = raw_input('NICKSERV PASSWOR: ')
        SaveConfig(SOURCES[1])
    if lc[0][1] is True:
        print('Ciclando a los siguientes servidores: ')
        for i in VG.SC:
            server, port, SASL = i
            print('    %s:%s, SASL: %s' % (server, port, SASL))
            IRC.connection.Loop_sc(server, port, SASL).start()
    if exists('DB/DB/flagsdata.db') and exists('DB/DB/usersdata.db'):
		VG.db_users = __UserHandler.db.load('usersdata')
		VG.db_flags = __UserHandler.db.load('flagsdata')
		print('Base de datos cargada.')
    threading.Thread(target=ServerConfig).start()
    __UserHandler.MainLoop(VG.uhoq, VG.uhso).start()
    commands.MainLoop(VG.coq, VG.cso).start()

if __name__ == '__main__':
    main()
