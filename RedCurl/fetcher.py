#!/usr/env python

import pycurl,json
from cStringIO import StringIO


class CurlWorker(object):
	"""
	CurlWorker class
	
	Class for communicating with external API
	:param page: external API URL
	"""
	def __init__(self,page):
		self.c = pycurl.Curl()
		self.opt = self.c.setopt
		page = page if page.endswith('/') else page+'/'
		self.opt(pycurl.URL,page)
	def loader(self,dat):
		"""loader function
		
		:param dat: a list of data to be submitted via post to the URL provided
		"""
		assert(isinstance(dat,list))
		self.opt(pycurl.HTTPPOST,dat)
	def grab(self):
		"""grab function
		
		N.B. This function creates a new IO stream everytime it is called in 
		later versions this will be removed, so plan accordingly!
		:param None: No input paramegers this function makes the call to the API
		via pycurl's `perform` method.
		:returns: server response as a string.
		"""
		buf = StringIO()
		self.opt(pycurl.WRITEDATA,buf)
		self.c.perform()
		ostr=buf.getvalue()
		buf.close()
		return ostr
	def exit(self):
		"""exit
		
		This method closes the curl object and purges 
		the contents from memory
		"""
		self.c.reset()
		self.c.close()
		