# -*- coding: utf-8 -*-

import time
Dir = "DB/LOGS/"


class log:
	def __init__(self, string, print_str=False):
		self.string = string
		md = time.asctime().split()
		self.md = "%s/%s(%s)" % (md[2], md[1], md[3])
		self.format = "log"
		self.str_mode = "a"
		self.print_str = print_str
				
	def Logger(self):
		Filelog = file(Dir+"log." + self.format, self.str_mode)
		Filelog.write("LOG[%s]: %s\n" % (self.md, self.string))
		Filelog.close()
		if self.print_str:
			print "LOG[%s]: %s\n" % (self.md, self.string)
					
	def LogError(self):
		Filelog = file(Dir+"log_error." + self.format, self.str_mode)
		Filelog.write("LOG:ERROR:[%s]: %s\n" % (self.md, self.string))
		Filelog.close()
		if self.print_str:
			print "LOG:ERROR:[%s]: %s\n" % (self.md, self.string)
					
	def LogSend(self):
		Filelog = file(Dir+"log_send." + self.format, self.str_mode)
		Filelog.write("LOG:SEND:[%s]: %s\n" % (self.md, self.string))
		Filelog.close()
		if self.print_str:
			print "LOG:SEND:[%s]: %s\n" % (self.md, self.string)
					
	def LogRecv(self):
		Filelog = file(Dir+"log_recv." + self.format, self.str_mode)
		Filelog.write("LOG:RECV:[%s]: %s\n" % (self.md, self.string))
		Filelog.close()	
		if self.print_str:
			print "LOG:RECV:[%s]: %s\n" % (self.md, self.string)
