# -*- coding: utf-8 -*-
import VG
import userinfo
import IRC.modes
import logger
import db

class Flags:
	def __init__(self, username, channel, flags):
		userinf0 = userinfo.registered(username)
		self.username = username
		self.index = userinf0[1]
		self.flags = IRC.modes.pnm(flags)
		self.registered = userinf0[0]
		self.channel = channel
		del userinf0
		try:
			for i in VG.db_flags.keys():
				if i.match(channel):
					self.CR = (True, i) # Canal Registrado (CR)
					raise StopIteration
		except StopIteration:
			try:
				VG.db_flags[self.CR[1]][userinfo.info(username, 'username')]
			except KeyError:
				self.UR = False
			else:
				self.UR = True
		else:
			self.UR = None
			
	def SetFlags(self):
		Info = userinfo.info(self.username, 'username')
		if self.registered:
			if self.CR[0]:
				if self.UR:
					for l in self.flags:
						if l[1] in ['A', 'S', 'f', 'k', 'r', 'm', 'o', 'v', 's']:
							if l[0] is '+':
								if not l[1] in VG.db_flags[self.CR[1]][Info]:
									VG.db_flags[self.CR[1]][Info].append(l[1])
							elif l[0] is '-':
								if l[1] in VG.db_flags[self.CR[1]][Info]:
									VG.db_flags[self.CR[1]][Info].remove(l[1])
					after = ''.join(VG.db_flags[self.CR[1]][Info])								
					db.save('DB_Flags', VG.db_flags)
					del Info
					return (True, '\002\00301%s: %s(+%s).' % (self.channel, self.username, after))
				elif self.UR is False:
					VG.db_flags[self.CR[1]][Info] = []
					return 'Reply'
			else:
				return '\002\00301Canal: \00304No registrado.'	
		else:
			return '\002\00301Usuario: \00304No registrado.'
