# -*- coding: utf-8 -*-

import modes
import string
import socket
import threading

import client

import VG


def Conectar(server, port, SASL):
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((server, port))
    irc.send('CAP REQ :sasl\r\n')
    irc.send("NICK %s\n" % VG.IC['NICK'])
    irc.send("USER %s %s * * :%s\r\n" % (VG.IC['IDENT'], VG.IC['NICK'], VG.IC['REALNAME']))
    if SASL is True:
        import base64
        irc.send('AUTHENTICATE PLAIN\r\n')
        irc.send('AUTHENTICATE %s\r\n' % base64.encodestring(VG.np))
        irc.send('CAP END\r\n')
    else:
        irc.send('CAP END\r\n')
    VG.lssc[server] = irc
    return irc


class Loop_sc(threading.Thread):

    def __init__(self, server, port=6667, SASL=False):
        threading.Thread.__init__(self)
        self.SASL = SASL
        self.server = server
        self.port = port

    def run(self):
        readbuffer = ""
        sc = {'SC': Conectar(self.server, self.port, self.SASL)}
        Client = {'SC': client.cliente(sc['SC'])}
        while True:
            readbuffer = readbuffer + sc['SC'].recv(4096)
            temp = string.split(readbuffer, '\n')
            if len(temp[0]) == 0:
                sc['SC'] = Conectar(self.server, self.port, self.SASL)
                Client['SC'] = client.cliente(sc['SC'])
            readbuffer = temp.pop()
            for j in temp:
                try:
                    mlen = j.split()
                    user = j.split('!')[0].split(':')[1]
                    host = mlen[0].split('@')[1]
                    mlex = j.split('%s %s %s :' % (mlen[0], mlen[1], mlen[2]))[1]
                except (IndexError, ValueError):
                    if mlen[0] == 'PING':
                        Client['SC'].send_msg('PONG ' + mlen[1])
                try:
                    try: n_e = int(mlen[1])
                    except ValueError: n_e = '0'
                    if type(n_e) == int:
                        if n_e == 376:
                            Client['SC'].Join(VG.CHANNELS)
                            if not self.SASL:
                                Client['SC'].privmsg("NickServ", 'IDENTIFY %s' % VG.IC['NP'])
                        if n_e == 401:
                            del mlex
                        if n_e == 403:
                            del mlen
                        if n_e == 411:
                            del mlen  # lint:ok
                        if n_e == 473:
                            Client['SC'].privmsg("ChanServ", "INVITE " + mlen[3])
                        if n_e == 474:
                            Client['SC'].privmsg("ChanServ", "UNBAN " + mlen[3])
                            Client['SC'].Join(mlen[3])
                        if n_e == 475:
                            Client['SC'].privmsg("ChanServ", "GETKEY " + mlen[3])
                    if mlen[1] in ["PART", "JOIN", "NICK", "QUIT"]:
                        del mlen
                        del mlex
                    if mlen[1] in ["KICK","MODE","INVITE"]:
                        if mlen[1] == 'KICK':
                            if mlen[3] == VG.IC['NICK']:
                                Client['SC'].Join(mlen[2])
                        if mlen[1] == 'MODE':
                            pnm = modes.pcm(''.join(mlen[3:]))
                            for i in pnm:
                                if i[0] == '-' and i[1] == 'o':
                                    if i[2] == VG.IC['NICK']:
                                        Client['SC'].privmsg("ChanServ", "OP" + mlen[2])
                                if i[0] == '+' and i[1] == 'o':
                                    if i[2] != VG.IC['NICK']:
                                        try:
                                            for i in VG.AntiOP.keys():
                                                if i.match(mlen[2]):
                                                    raise StopIteration
                                        except StopIteration:
                                            if VG.AntiOP[i] == 'on':
                                                Client['SC'].mode(mlen[2], '-o', i[2])
                        if mlen[1] == 'INVITE':
                            Client['SC'].Join(mlex)
                except (NameError, IndexError):
                    pass

                try:
                    VG.uhso.put(sc['SC'])
                    VG.cso.put(sc['SC'])
                    VG.uhoq.put('%s!%s@%s %s' % (user, mlen[2], host, mlex))
                    VG.coq.put('%s!%s@%s %s' % (user, mlen[2], host, mlex))
                except (IndexError, NameError):
                    VG.uhoq.put('_-Null-_!_-Null-_@localhost None None')
                    VG.coq.put('_-Null-_!_-Null-_@localhost None None')
