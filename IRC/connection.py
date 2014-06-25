# -*- coding: utf-8 -*-

import modes
import string
import socket
import threading

import client

import VG
import logger


def Conectar(server, port, SASL):
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((server, port))
    irc.send('CAP REQ :sasl\r\n')
    irc.send("NICK %s\n" % VG.nick)
    irc.send("USER %s %s * * :%s\r\n" % (VG.ident, VG.nick, VG.realname))
    if SASL:
        import base64
        irc.send('AUTHENTICATE PLAIN\r\n')
        irc.send('AUTHENTICATE {0} \r\n'.format(base64.encodestring(VG.np)))
        irc.send('CAP END\r\n')
    else:
        irc.send('CAP END\r\n')
    VG.server.append({'server': server,
                      'port': port,
                      'SASL': SASL})
    return irc


class Loop_sc(threading.Thread):

    def __init__(self, server, port=6667, SASL=False):
        threading.Thread.__init__(self)
        self.SASL = SASL
        self.server = server
        self.port = port
        logger.log('Conexion en segundo plano.').Logger()
        logger.log('SERVER=%s PORT=%s SASL=%s' % (server, port, SASL)).Logger()

    def run(self):
        readbuffer = ""
        s = Conectar(self.server, self.port, self.SASL)
        Client = client.cliente(s)
        while True:
            readbuffer = readbuffer + s.recv(4096)
            temp = string.split(readbuffer, '\n')
            readbuffer = temp.pop()
            for j in temp:
                logger.log(j).LogRecv()
                try:
                    mlen = j.split()
                    user = j.split('!')[0].split(':')[1]
                    host = mlen[0].split('@')[1]
                    mlex = j.split('%s %s %s :' % (mlen[0], mlen[1], mlen[2]))[1]
                except (IndexError, ValueError):
                    if mlen[0] == 'PING':
                        Client.send_msg('PONG ' + mlen[1])
                try:
                    try: n_e = int(mlen[1])
                    except ValueError: n_e = '0'
                    if type(n_e) == type(0):
                        if n_e == 376:
                            Client.Join(VG.chan)
                            if not self.SASL:
                                Client.privmsg("NickServ", 'IDENTIFY %s' % VG.np)
                        if n_e == 401:
                            del mlenx
                        if n_e == 403:
                            del mlen
                        if n_e == 411:
                            del mlen
                        if n_e == 473:
                            Client.privmsg("ChanServ", "INVITE " + mlen[3])
                        if n_e == 474:
                            Client.privmsg("ChanServ", "UNBAN " + mlen[3])
                            Client.Join(mlen[3])
                        if n_e == 475:
                            Client.privmsg("ChanServ", "GETKEY " + mlen[3])
                    if mlen[1] in ["PART", "JOIN", "NICK", "QUIT"]:
                        del mlen
                        del mlex
                    if mlen[1] in ["KICK","MODE","INVITE"]:
                        if mlen[1] == 'KICK':
                            if mlen[3] == VG.nick:
                                Client.Join(mlen[2])
                        if mlen[1] == 'MODE':
                            pnm = modes.pcm(''.join(mlen[3:]))
                            for i in pnm:
                                if i[0] == '-' and i[1] == 'o':
                                    if i[2] == VG.nick:
                                        Client.privmsg("ChanServ", "OP" + mlen[2])
                                if i[0] == '+' and i[1] == 'o':
                                    if i[2] != VG.nick:
                                        try:
                                            for i in VG.AntiOP.keys():
                                                if i.match(mlen[2]):
                                                    raise StopIteration
                                        except StopIteration:
                                            if VG.AntiOP[i] == 'on':
                                                Client.mode(mlen[2], '-o', i[2])
                        if mlen[1] == 'INVITE':
                            Client.Join(mlex)
                except (NameError, IndexError):
                    pass

                try:
                    VG.uhso.put(s)
                    VG.cso.put(s)
                    VG.uhoq.put('%s!%s@%s %s' % (user, mlen[2], host, mlex))
                    VG.coq.put('%s!%s@%s %s' % (user, mlen[2], host, mlex))
                except (IndexError, NameError):
                    VG.uhoq.put('_-Null-_!_-Null-_@localhost None None')
                    VG.coq.put('_-Null-_!_-Null-_@localhost None None')
