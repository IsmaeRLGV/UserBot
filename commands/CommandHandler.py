# -*- coding: utf-8 -*-

import VG

class CommandHandler:
	def __init__(self, handler, channel, Set='on' ):
		self.handler = handler
		self.channel = channel
		self.Set = Set
	
	def SetCommand(self):
		try:
			for j in eval('VG.%s' % self.handler).keys():
				if j.match(self.channel):
					raise StopIteration('StopIteration')
		except (NameError, StopIteration) as e:
			if e is 'StopIteration':
				eval('VG.%s' % self.handler)[j] = self.Set
				return True
		else:
			return False
