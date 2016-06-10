# CapPyCurl
=======
## Basic Setup
    >>> from CapPyCurl import RedCurl
    >>> proj = "<your project API token>"
    >>> page = "<your api URL>"
    >>> rc = RedCurl(page)
    ... RedCurl commands ...
### Pull MetaData
#### Method 1 (assumes basic setup step has been done)
    >>> md = rc.metagrab(token=proj)
    >>> print md
    ... Your Metadata ...
    >>> rc.exit()
#### Method 2 (assumes basic setup step has not been done)
    >>> proj = "<your project API token>"
    >>> page = "<your api URL>"
    >>> rc2 = redcurl(page,token=proj)
    >>> md2 = rc2.metagrab()
    >>> print md2
    ... Your MetaData ...
### More to come...
