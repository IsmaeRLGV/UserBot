# -*- coding: utf-8 -*-

                          
import Queue
import string
import socket
import threading

from IRC import client

import VG
import logger

socke_handler = []
Out_Queue = Queue.Queue()

def Conectar():
	irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	irc.connect((VG.server, VG.port))
	logger.log('Conectado. Ahora registrandose').Logger()
	irc.send("NICK %s\n" % VG.nick)
	logger.log("NICK %s" % VG.nick).LogSend()
	irc.send("USER %s %s * * :%s\r\n" % (VG.ident, VG.nick , VG.realname))
	logger.log("USER %s %s * * :%s" % (VG.ident, VG.nick , VG.realname)).LogSend()
	socke_handler.append(irc)
	return socke_handler.index(irc)

class Loop_sc(threading.Thread):
	logger.log('Conexion en segundo plano.').Logger()
	def run(self):
		readbuffer = ""
		sc = Conectar()
		s = socke_handler[sc]
		Client = client.cliente(s)
		while True:
			readbuffer = readbuffer+s.recv(4096)
			temp = string.split(readbuffer, '\n')
			readbuffer = temp.pop()
			for j in temp:
				logger.log(j).LogRecv()
				try:
					mlen = j.split()
					user = j.split('!')[0].split(':')[1]
					host = mlen[0].split('@')[1]
					mlex = j.split('%s %s %s :' % (mlen[0], mlen[1], mlen[2]))[1]
					mlenx = mlex.split()
					
				except (IndexError, ValueError):
					if mlen[0] is 'PING':
						Client.send_msg('PONG ' + mlen[1])
				
				try:
					try:
						n_e = int(mlen[1])
					except ValueError:
						n_e = 0	
					if type(n_e) is type(0):
						if n_e == 376:
							Client.Join(VG.chan)
							Client.privmsg("NickServ", "IDENTIFY " + "")
						if n_e == 401:
							mlenx = ["None"]                            # Debug
						if n_e == 403:
							mlen = ["None"]                             # Debug
						if n_e == 404:
							mlen = ["None"]                             # Debug
						if n_e == 473:
							Client.privmsg("ChanServ", "INVITE " + mlen[3])
						if n_e == 474:
							Client.privmsg("ChanServ", "UNBAN " + mlen[3])
							Client.Join(mlen[3])
						if n_e == 475:
							Client.privmsg("ChanServ", "GETKEY " + mlen[3])
					if mlen[1] in ["PART", "JOIN", "NICK", "QUIT"]:
						if mlen[1] == "JOIN" and user == VG.nick:
							pass
					if mlen[1] in ["KICK","MODE","INVITE"]:
						pass
				except IndexError:
					pass
				Out_Queue.put(j)

Loop_sc().start()
