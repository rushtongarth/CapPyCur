# CapPyCurl
=======
## Basic Usage
    >>> from CapPyCurl import RedCurl
    >>> proj = "<your project API token>"
    >>> page = "<your api URL>"
    >>> rc = redcurl(page)
    >>> s = rc.metagrab(token=proj)
    >>> rc.exit()
    >>> rc2 = redcurl(page,token=proj)
    >>> s2 = rc2.metagrab()
    >>> s==s2
    True
    >>> s
    ... Your Metadata ...
