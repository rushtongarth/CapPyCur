#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Stephen Garth <stephen.r.garth@vanderbilt.edu>'
__copyright__ = 'Copyright 2015 Vanderbilt University. All Rights Reserved'
__desc__ = 'CapPyCurl is a package to access the RedCap API via PyCurl'


from CapPyCurl.RedCurl import RedCurl
from CapPyCurl.RedCurl import CurlWorker

VERSION = (1,0,0)

def get_version():
	return '.'.join(str(i) for i in VERSION)

__version__ = get_version()
