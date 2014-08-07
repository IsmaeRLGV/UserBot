# -*- coding: utf-8 -*-

#Config
SC = []
IC = {}
ADMIN = None
TWITTER = None
CHANNELS = ''

lssc = {}

#Queues
import Queue
uhso = Queue.Queue()
uhoq = Queue.Queue()
cso = Queue.Queue()
coq = Queue.Queue()
comd = '&'

#Variables Globales
db_users = []         #Base de Datos: Usuarios.
db_flags = {}         #Base de Datos: Flags (Esta ligada a la Base de datos de usuarios).

#Control
Anti = {}
AntiOP = {}
ABW = {}
AntiFlood = {}
Me = {}
Google = {}
UrlOpen = {}
