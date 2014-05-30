# -*- coding: utf-8 -*-

import time
import logger
import socket

class cliente:
	def __init__(self, Param00):
		self.s =  Param00
		
	def send_msg(self, msg):
		"""Send Msg. """
		self.s.send("%s\r\n" % msg)
		logger.log(msg).LogSend()
		
	def privmsg(self, target, text):
		"""Send a PRIVMSG command."""
		time.sleep(1)
		self.s.send("PRIVMSG %s :%s\n" % (target, text))
		logger.log("PRIVMSG %s :%s" % (target, text)).LogSend()
	
	def notice(self, target, text):
		"""Send a NOTICE command."""
		time.sleep(1)
		self.s.send("NOTICE %s :%s\n" % (target, text))
		logger.log("NOTICE %s :%s" % (target, text)).LogSend()
	
	def Join(self, channel, key=""):
		"""Send a JOIN command."""
		if channel != "0":
			time.sleep(1)
			self.s.send("JOIN %s%s\n" % (channel, (key and (" " + key))))
			logger.log("JOIN %s%s" % (channel, (key and (" " + key)))).LogSend()
	
	def part(self, channel, message=""):
		"""Send a PART command."""
		time.sleep(1)
		self.s.send("PART %s%s\n" % (channel, (message and (" :" + message))))
		logger.log("PART %s%s" % (channel, (message and (" :" + message)))).LogSend()
	
	def kick(self, channel, nick, comment=""):
		"""Send a KICK command."""
		time.sleep(1)
		self.s.send("KICK %s %s%s\n" % (channel, nick, (comment and (" :" + comment))))
		logger.log("KICK %s %s%s" % (channel, nick, (comment and (" :" + comment)))).LogSend()
		
	def remove(self, channel, nick, comment=""):
		"""Send a REMOVE command."""
		time.sleep(1)
		self.s.send("REMOVE %s %s%s\n" % (channel, nick, (comment and (" :" + comment))))
		logger.log("REMOVE %s %s%s" % (channel, nick, (comment and (" :" + comment)))).LogSend()
	
	def mode(self, channel, target, command=""):
		"""Send a MODE command."""
		time.sleep(1)
		self.s.send("MODE %s %s%s\n" % (channel, target, (command and (" " + command))))
		logger.log("MODE %s %s%s" % (channel, target, (command and (" " + command)))).LogSend()
	
	def topic(self, channel, new_topic=None):
		"""Send a TOPIC command."""
		if new_topic is None:
			time.sleep(1)
			self.s.send("TOPIC %s\n" % channel)
			logger.log("TOPIC %s" % channel).LogSend()
		else:
			time.sleep(1)
			self.s.send("TOPIC %s :%s\n" % (channel, new_topic))
			logger.log("TOPIC %s :%s" % (channel, new_topic)).LogSend()
	
	def ctcp_version(self, user):
		time.sleep(1)
		self.s.send("NOTICE %s :IRCBot. UserBot by Kwargs.\n" % user)
		logger.log("NOTICE %s :IRCBot. UserBot by Kwargs." % user).LogSend()
		
	def ctcp_ping(self, user, target):
		self.s.send("NOTICE %s :PING  %s\n" % (user, target))
		logger.log("NOTICE %s :PING  %s" % (user, target)).LogSend()
								
			
