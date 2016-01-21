# CapPyCurl
## Basic Usage
    >>> import os
    >>> from CapPyCurl.redPyCurl import redcurl
    >>> user = os.getenv("USER")
    >>> proj = "<your project key name (see CryptoPickle)>"
    >>> page = "<your api URL>"
    >>> locn = os.getcwd()
    >>> rc = redcurl(proj,page,usercrypt=user,keyloc=locn)
    >>> s = rc.metagrab()
    >>> rc.exit()
    >>> print s
    ... Your Metadata ...
