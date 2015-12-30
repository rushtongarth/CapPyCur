#!/usr/env python


import pycurl,json,os,sys
from cStringIO import StringIO
from operator import itemgetter

from cryptopickle import cryptopickle as cyp,config as cfg

class curlworker(object):
	def __init__(self,page):
		self.c = pycurl.Curl()
		self.opt = self.c.setopt
		self.opt(pycurl.URL,page)
	def loader(self,dat):
		assert(type(dat)==type([]))
		self.opt(pycurl.HTTPPOST,dat)
	def grab(self):
		buf = StringIO()
		self.opt(pycurl.WRITEDATA,buf)
		self.c.perform()
		ostr=buf.getvalue()
		buf.close()
		return ostr
	def alldone(self):
		self.c.close()
class capProj(object):
	def __init__(self,name,loc = None,usecrypt = False):
		self.name = name
		self.usecrypt = usecrypt
		self.loc = os.path.dirname(os.path.realpath(__file__)) if not loc else loc

	def getinfo(self):
		return cyp.CryptoPickle(cfg.storageinfo(keyuser='pickleUser',loc=self.loc))
	def tokretr(self):
		if self.usecrypt:
			_cp = self.getinfo()
			return _cp.fread()[self.name]
		with open(self.loc,'r') as f:
			tmp=f.read()
		tmp = tmp.split('\n')
		
		return filter(lambda x: x.startswith(self.name),tmp)[0].split('@')[1]
class redcurl(curlworker,capProj):
	def __init__(self,proj,cyp=False,keyloc=None):
		curlworker.__init__(self,"https://redcap.vanderbilt.edu/api/")
		capProj.__init__(self,proj,loc=keyloc,usecrypt=cyp)
		self.output = "Nothing Found"
	def _inputhandler(self,incoming):
		if isinstance(incoming,list):
			return ','.join(str(i) for i in incoming)
		elif isinstance(incoming,str) or isinstance(incoming,unicode):
			return incoming if isinstance(incoming,str) else str(incoming)
		else:
			raise TypeError("Input must be str or list\n\tRecieved: %s" %(str(type(incoming))))
	def metagrab(self,style='json'):
		dat = [('token',self.tokretr()),('content','metadata'),('format',style)]
		self.loader(dat)
		self.output = self.grab()
		if style == 'json':
			return json.loads(self.output)
		return self.output
	def fieldnames(self):
		return map(itemgetter('field_name'),self.metagrab('json'))
#	def pullreport
	def pullform(self,recno,forms,style='json'):
		dat = [('token',self.tokretr()),('content','record'),('format',style),('action','export')]
		recno = self._inputhandler(recno)
		topull = self._inputhandler(forms)
		dat.extend([('records',recno),('forms',topull)])
		self.loader(dat)
		self.output = self.grab()
		return json.loads(self.output) if style == 'json' else self.output
	def pullrec(self,recno,style='json',fields=None):
		dat = [('token',self.tokretr()),('content','record'),('format',style),('action','export')]
		recno = self._inputhandler(recno)
		dat.append(('records',recno))
		if fields:
			fields = self._inputhandler(fields)
			dat.append(('fields',fields))
		self.loader(dat)
		self.output = self.grab()
		if style == 'json':
			return json.loads(self.output)
		return self.output
	def pushrec(self,recno,**kwargs):
		data = {'participant_id':recno}
		data.update(kwargs)
		payload = [('content','record')]
		datain = json.dumps([data])
		payload.extend([('type','flat'),('format','json'),('token',self.tokretr()),('data',datain)])
		self.loader(payload)
		self.output = self.grab()
		return self.output

	def fullpull(self,delim=',',recs=[],fields=[]):
		import csv
		if len(fields):
			if isinstance(fields[0],tuple):
				topull,toname = zip(*fields)
			else:
				topull,toname = [fields],[]
			data = {"fields":topull,"fieldnames":toname}
		else:
			data = {"fields":[],"fieldnames":[]}
		recs = self.pullrec(recs,style='csv',fields=data['fields'])
		buff = StringIO(recs)
		#buff = sio(recs)
		if len(data['fieldnames']):
			reader = csv.DictReader(buff,data['fieldnames'],delimiter=delim)
		else:
			reader = csv.DictReader(buff,delimiter=delim)
		out = [row for row in reader]
		buff.close()
		return out

	def pushfile(self,recno,fieldname,localname,rcname,pid=None):
		dat = [('content','file'),('action','import'),('record',recno),('field',fieldname)]
		dat.extend([('file', (pycurl.FORM_FILE, localname, pycurl.FORM_FILENAME, rcname))])
		dat.extend([('token',self.tokretr())])
		if pid:
			dat.extend([('project_id',str(pid))])
		self.loader(dat)
		self.output = self.grab()
		if len(self.output):
			return "Failure: recieved the following message\n"+self.output
		else:
			return "File %s, successfully uploaded\n" %(localname)
	
