import os

thisdir = os.path.expanduser("~")+os.sep+'.gnupg'
thisusr = os.getenv("USER")
stdname = 'keys.cfg'

class storageinfo(object):
	def __init__(self,keyuser=None,home=None,fname=None,loc=''):
		self.u = thisusr if not keyuser else keyuser
		self.h = thisdir if not home else home
		emailexn = '@example.com'
		self.fname = stdname if not fname else fname
		self.keyloc = loc+os.sep if len(loc) else loc
	def getcryptname(self):
		tmp = self.fname.split('.')
		return self.keyloc+'.'.join(i for i in tmp[:-1])+'.crypto.'+tmp[-1]
		
	
