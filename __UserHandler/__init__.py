# -*- coding: utf-8 -*-

import db
import re
import VG
import flags
import userinfo
import register
import threading
import IRC.client
import IRC.connection
import SessionHandler

from commands.newCommand__ import newCommand

class MainLoop(threading.Thread):
	def __init__(self, Out_Queue, SocketObject):
		threading.Thread.__init__(self)
		self.Out_Queue = Out_Queue
		self.SocketObject = SocketObject
		
	def run(self):
		while True: 
			Client = client.cliente(self.SocketObject.get())
			args = self.Out_Queue.get()
			args = msg.split()
			data = args[0].replace('!', ' ').replace('@', ' ').split()
			if newCommand('registro', args[1]):
				if data[0] is VG.nick:
					if register.RegisterUser(data[1], data[2], args[2]):
						Client.notice(data[1], "\00303Registrado de forma exitosa.")
					else:
						Client.notice(data[1], "\00304ERROR\00301: No se pudo registrar.")			
				else:
					if register.RegisterChannel(data[1], data[0]) is None:
						Client.notice(data[0], "\00303Canal registrado de forma exitosa.")
					else:
						Client.notice(data[0], '\00304ERROR\00301: El canal ya se encuentra registrado')
			if newCommand('login', args[1]):
				A = SessionHandler.login(data[1], data[2], args[2])
				if A is None:
					Client.notice(data[1], "\00303Logueado de forma exitosa.")
				else:
					Client.notice(data[1], A)
					del A
			if newCommand('logout', args[1]):
				A = SessionHandler.logout(data[1], data[2])
				if A is None:
					Client.notice(data[1], "\00303Deslogueado de forma exitosa.")
				else:
					Client.notice(data[1], A)
					del A
			if newCommand('access', args[1]):
				A  = flags.Flags(data[1], data[0], args[2])
				a = A.SetFlags()
				if a[0] is True:
					Client.notice(data[0], a[1])
				elif a[0] is False:
					A = flags.Flags(data[1], data[0], args[2])
					a = A.SetFlags()
					if a[0] is True:
						Client.notice(data[0], a[1])
				elif a[0] is None:
					Client.notice(data[0], a[1])
