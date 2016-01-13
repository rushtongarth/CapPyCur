#!/usr/env python

import pycurl,json

class CurlWorker(object):
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