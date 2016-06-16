#!/usr/env python


import pycurl
import os,json
from cStringIO import StringIO
from operator import itemgetter
from fetcher import CurlWorker

class RedCurl(CurlWorker):
	"""RedCurl - 
	
	A class for talking to redcap with pycurl
	"""
	def __init__(self,cappage,token=''):
		"""
		
		:param cappage: RedCap API location
		:param token: token to use for future communications.
		N.B. If not provided here the token must be supplied 
			with the command that is to be executed.
		:return: None
		"""

		CurlWorker.__init__(self,cappage)
		self.output = ""
		self.t = token
	def _inputhandler(self,incoming):
		"""inputhelper function
		
		:param incoming: string or list to process
		:return: comma separated list of items
		"""
		if isinstance(incoming,list):
			return ','.join(str(i) for i in incoming)
		elif isinstance(incoming,str) or isinstance(incoming,unicode):
			return incoming if isinstance(incoming,str) else str(incoming)
		else:
			raise TypeError("Input must be str or list\n\tRecieved: %s" %(str(type(incoming))))
	def gettoken(self):
		"""gettoken
		
		:return: API token
		"""
		return self.t
	def settoken(self, token):
		"""settoken
		
		Set the API token value
		:param: API token
		"""
		self.t = token
	def deltoken(self):
		"""deltoken
		
		Remove the token from locals
		"""
		del self.t
	token = property(gettoken, settoken, deltoken, "Token property")

	def metagrab(self,style='json',token=''):
		"""
		metagrab - grab project metadata
		
		:param style: format to return from redcap, defaults to json
		:param token: API token (if not provided earlier)
		:return: redcap project metadata
		"""
		if token:
			self.settoken(token)
		dat = [('token',self.t),('content','metadata'),('format',style)]
		self.loader(dat)
		self.output = self.grab()
		if style == 'json':
			return json.loads(self.output)
		return self.output

	def fieldnames(self,style='json',token=''):
		"""
		fieldnames - get fieldnames from metadata
		
		:param style: format to return from redcap, defaults to json
		:param token: API token (if not provided earlier)
		:return: redcap project metadata
		"""
		return map(itemgetter('field_name'),self.metagrab('json'))
	def pullform(self,recno,forms,style='json',token=''):
		"""
		pullform - pull a Redcap form for a record
		
		:param recno: record(s) to query
		:param forms: form(s) to pull
		:param style: format to return from redcap, defaults to json
		:param token: API token (if not provided earlier)
		:return: form for the record(s) you asked for
		"""
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
		"""
		pullrec - pull Redcap records
		
		:param recno: record(s) to query
		:param style: format to return from redcap, defaults to json
		:param fields: field(s) to pull, defaults to all
		:param token: API token (if not provided earlier)
		:return: Fields from the list of records 
		"""
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
		"""
		pushrec - push Redcap record
		
		:param recno: record to push data to 
			N.B. This is currently implemented for a single record!
		:param kwargs: dictionary whose keys are fieldnames and 
			values are the data to upload to said fields
		:param token: API token (if not provided earlier)
		:return: server response
		"""

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

	def fullpull(self,delim=',',recno='',token=''):
		"""
		fullpull - pull all fields for specified records
		
		:param delim: how to output fields are to be separated
		:param recno: records to pull, defaults to all records
		:param token: API token (if not provided earlier)
		:return: all fields for the records specified
		"""

		if not self.t:
			self.t = self.gettoken()
		import csv
		data = {"fields":[],"fieldnames":[]}
		if not recno:
			recno=[]
		recs = self.pullrec(recno,style='csv',fields=data['fields'])
		buff = StringIO(recs)
		if len(data['fieldnames']):
			reader = csv.DictReader(buff,data['fieldnames'],delimiter=delim)
		else:
			reader = csv.DictReader(buff,delimiter=delim)
		out = [row for row in reader]
		buff.close()
		return out

	def pushfile(self,recno,fieldname,localname,rcname,pid=None,token=''):
		"""
		pushfile - upload a file
		
		:param recno: record to push data to 
			N.B. This is currently implemented for a single record!
		:param fieldname: field to upload the file to
		:param localname: full path to file that is to be uploaded
		:param rcname: name of the file as it should appear on redcap
		:param pid: project id, only necessary if the redcap project is longitudinal
		:param token: API token (if not provided earlier)
		"""
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
	
