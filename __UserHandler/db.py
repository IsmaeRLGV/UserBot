
import logger

try:
	import cPickle as pickle
except ImportError as e:
	import pickle
	logger.log(e).LogError()

Dir = 'DB/DB/'

def save(filename, content, m_str="w"):
	logger.log("ROUTE: " + Dir + filename + ".db" ).Logger()
	logger.log("SAVE: %s" %  content).Logger()
	filename = file(Dir + filename + ".db", m_str)
	pickle.dump(content, filename)
	filename.close()

def load(filename):
	logger.log("LOADING: " + Dir + filename + '.db').Logger()
	return pickle.load(file(Dir + filename + '.db'))
