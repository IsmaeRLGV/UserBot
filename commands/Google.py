# -*- coding: utf-8 -*-


import simplejson
import socket
import urllib2

def Search(target, query):
	ut = ["Resultados de la busqueda de \002\00312G\00304o\00308o\00312g\00303l\00304e\003:"]
	query = urlencode({'q' : query})
	rs_search = urllib.urlopen("http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s" % query)
	results = json['responseData']['results']
	for i in results:
		ut.append("\002%s \00311%s" % (i['titleNoFormatting'], i['url']))
	return "\00313|\003".join(ut)

def Images(target, query):
	u = ["\002\00312G\00304o\00308o\00312g\00303l\00304e" +
	     "\00312I\00304m\00308a\00312g\00303e\00304n\003: "]
	busqueda = urllib.quote_plus(query)
	ip = socket.gethostbyname(socket.gethostname())
	size = "imgsz=small|medium|large|xlarge"
	as_filetype = "png|jpg"
	resultados = "rsz="+str(1)
	url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 
	       'v=1.0&q=%s&userip=%s&as_filetype=%s&%s&%s' % (busqueda, ip, size, resultados))
	request = urllib2.Request(url, None, {'Referer': 'http://bobbelderbos.com'})
	response = urllib2.urlopen(request)
	json = simplejson.load(response)
	resultados = json['responseData']['results']
	for i in resultados:
		u.append("\00311%s" % i['url'])
	return "\00311".join(u)
