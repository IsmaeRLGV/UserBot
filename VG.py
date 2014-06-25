# -*- coding: utf-8 -*-


import Queue

#Informacion de Conexion
server = []
nick = "UserBot"
realname = nick
ident = nick
chan = '#gazuza'
np = ''
uhso = Queue.Queue()
uhoq = Queue.Queue()
cso = Queue.Queue()
coq = Queue.Queue()
comd = ''

#Variables Globales
db_users = []         #Base de Datos: Usuarios.
db_flags = {}         #Base de Datos: Flags (Esta ligada a la Base de datos de usuarios).
Anti = {}
AntiOP = {}
ABW = {}
AntiFlood = {}
Me = {}               #Moderador Esctricto
Google = {}           #Promueve o restringe el uso de las busquedas de Google como:
                      #Google Images, Search, Etc.
UrlOpen = {}          #Promueve o restringe el uso del aperturador de URLS de un canal especifico.
Part = {}             #Promueve o restringe el uso del comando 'Part' de un canal especifico.
Join = {}             #Promueve o restringe el uso del comando 'Join' de un canal especifico.
Kick = {}             #Promueve o restringe el uso del comando 'Kick' de un canal especifico.
Op = {}               #Promueve o restringe el uso del comando 'Op' de un canal especifico.
Ban = {}              #Promueve o restringe el uso del comando 'Ban' de un canal especifico.
Voice = {}            #Promueve o restringe el uso del comando 'Voice' de un canal especifico.
ChMode = {}           #Promueve o restringe el uso del comando 'ChMode' de un canal especifico.
MGame = {}            #Promueve o restringe el uso TOTAL o PARCIAL de los juegos del BOT
                      #De un canal en especifico
