import os,collections
from setuptools import setup, find_packages


def read(fname):
	fp = os.path.join(os.path.dirname(__file__), fname)
	with open(fp,'r') as f:
		o=f.read()
	return o
def load_auth_ver(fname):
	contents = read(fname)
	author,version=map(lambda x: x.strip(),contents.split('\n'))
	return author,version
def getvars():
	a,v = load_auth_ver('info.txt')
	OD = collections.OrderedDict
	d = OD([
		('author',a),
		('version',v),
		("name", "CapPyCurl"),
		("packages",['CapPyCurl']),
		("author_email", "stephen.garth@gmail.com"),
		("description", ("Communicate with the REDCap API via PycURL")),
		("license", "BSD"),
		("keywords", "PycURL REDCap Vanderbilt"),
		("url", "http://cappycurl.readthedocs.org/"),
		("long_description",read('README.md')),
		("classifiers",[
			"Development Status :: 4 - Beta",
			"Intended Audience :: Developers",
			"Programming Language :: Python :: 2.7",
			"Topic :: Utilities",
			"Topic :: Database",
			"License :: OSI Approved :: BSD License",
		]),
		('install_requires',['pycurl']),
		])
	return d
D = getvars()

setup(**D)