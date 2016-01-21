
import os

from CryptoPickle import CryptoPickle
from CryptoPickle import config


class CapProj(object):
	"""
	name: the project name as listed in the CryptoPickle
	loc: the location of the CryptoPickle file 
		that contains API tokens. defaults to PWD
	usercrypt: the user to use for opening the keyfile
		defaults to pickleUser"""
	def __init__(self,name,loc = None,usercrypt = None):
		self.name = name
		self.usercrypt = 'pickleUser' if not usercrypt else usercrypt
		self.loc = os.path.dirname(os.path.realpath(__file__)) if not loc else loc

	def tokretr(self):
		cfg = config.storageinfo(keyuser=self.usercrypt,loc=self.loc)
		_cp = CryptoPickle(cfg())
		return _cp.fread()[self.name]
