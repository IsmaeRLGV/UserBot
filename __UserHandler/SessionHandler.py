# -*- coding: utf-8 -*-

import db
import VG
import logger
import hashlib
import userinfo


def login(username, hostname, password):
    try:
        if hashlib.md5(password).hexdigest() == userinfo.info(username, 'password'):
            if userinfo.info(username, 'status') is 'desconectado':
                index = userinfo.registered(username)[1]
                VG.db_users[index]['status'] = 'conectado'
                VG.db_users[index]['hostname'] = hostname
                db.save('DB_Users', VG.db_users)
                logger.log('Usuario logeado a: '+username).Logger()
            else:
                raise UnboundLocalError(username + '. Ya se encuentra conectado.')
        else:
            raise ValueError(username + '. Contraseña erronea.')

    except (TypeError, ValueError, UnboundLocalError) as e:
        logger.log(e).LogError()
        return e

def logout(username, hostname):
	try:
		if userinfo.info(username, 'hostname') == hostname:
			if userinfo.info(username, 'status') is 'conectado':
				index = userinfo.registered(username)[1]
				VG.db_users[index]['status'] = 'desconectado'
				VG.db_users[index]['hostname'] = ''
				db.save('DB_Users', VG.db_users)
				logger.log('Usuario deslogueado: ' + username).Logger()
			else:
				raise UnboundLocalError(username + '. Ya se enuentra desconectado.')
		else:
			raise ValueError(hostname + '. El host no coincide.')
					
	except (TypeError, ValueError, UnboundLocalError) as e:
		logger.log(e).LogError()
		return e
