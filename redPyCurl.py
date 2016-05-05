#!/usr/env python


import pycurl
import os,json
from cStringIO import StringIO
from operator import itemgetter
from fetcher import CurlWorker




class RedCurl(CurlWorker):
	def __init__(self,cappage,token=''):
		CurlWorker.__init__(self,cappage)
		self.output = ""
		self.t = token
	def _inputhandler(self,incoming):
		if isinstance(incoming,list):
			return ','.join(str(i) for i in incoming)
		elif isinstance(incoming,str) or isinstance(incoming,unicode):
			return incoming if isinstance(incoming,str) else str(incoming)
		else:
			raise TypeError("Input must be str or list\n\tRecieved: %s" %(str(type(incoming))))
	def gettoken(self): 
		return self.t
	def settoken(self, token):
		self.t = token
	def deltoken(self):
		del self.t
	token = property(gettoken, settoken, deltoken, "Token property")

	def metagrab(self,style='json',token=''):
		if token:
			self.settoken(token)
		dat = [('token',self.t),('content','metadata'),('format',style)]
		self.loader(dat)
		self.output = self.grab()
		if style == 'json':
			return json.loads(self.output)
		return self.output

	def fieldnames(self,style='json',token=''):
		return map(itemgetter('field_name'),self.metagrab('json'))
	def pullform(self,recno,forms,style='json',token=''):
		if not self.t:
			self.t = self.gettoken()

		dat = [('token',self.t),('content','record'),('format',style),('action','export')]
		recno = self._inputhandler(recno)
		topull = self._inputhandler(forms)
		dat.extend([('records',recno),('forms',topull)])
		self.loader(dat)
		self.output = self.grab()
		return json.loads(self.output) if style == 'json' else self.output
	def pullrec(self,recno,style='json',fields=None,token=''):
		if not self.t:
			self.t = self.gettoken()

		dat = [('token',self.t),('content','record'),('format',style),('action','export')]
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
	def pushrec(self,recno,token='',**kwargs):
		if not self.t:
			self.t = self.gettoken()

		data = {'participant_id':recno}
		data.update(kwargs)
		payload = [('content','record')]
		datain = json.dumps([data])
		payload.extend([('type','flat'),('format','json'),('token',self.t),('data',datain)])
		self.loader(payload)
		self.output = self.grab()
		return self.output

	def fullpull(self,delim=',',recs=[],fields=[],token=''):
		if not self.t:
			self.t = self.gettoken()

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
		if len(data['fieldnames']):
			reader = csv.DictReader(buff,data['fieldnames'],delimiter=delim)
		else:
			reader = csv.DictReader(buff,delimiter=delim)
		out = [row for row in reader]
		buff.close()
		return out

	def pushfile(self,recno,fieldname,localname,rcname,pid=None,token=''):
		if not self.t:
			self.t = self.gettoken()
		dat = [('content','file'),('action','import'),('record',recno),('field',fieldname)]
		dat.extend([('file', (pycurl.FORM_FILE, localname, pycurl.FORM_FILENAME, rcname))])
		dat.extend([('token',self.t)])
		if pid:
			dat.extend([('project_id',str(pid))])
		self.loader(dat)
		self.output = self.grab()
		if len(self.output):
			return "Failure: recieved the following message\n"+self.output
		else:
			return "File %s, successfully uploaded\n" %(localname)
	
