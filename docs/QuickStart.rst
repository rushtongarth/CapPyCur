Quick Start Guide
=======================

.. contents::

Basic Setup
**********************************

    >>> from CapPyCurl import RedCurl
    >>> proj = "<your project API token>"
    >>> page = "<your api URL>"
    >>> rc = RedCurl(page)

Pull the project Metadata
*************************
Here we define two methods for pulling metadata for a project

Method 1
--------
This method assumes basic setup step has been done

    >>> md = rc.metagrab(token=proj)
    >>> print md
    [{'key1':'val1'},{'key2':'val2'}]
    >>> rc.exit()

Method 2 
--------
This method assumes basic setup step has not been done

    >>> proj = "<your project API token>"
    >>> page = "<your api URL>"
    >>> rc2 = redcurl(page,token=proj)
    >>> md2 = rc2.metagrab()
    >>> print md2
    [{'key1':'val1'},{'key2':'val2'}]
    >>> rc.exit()

Pull Data from RedCap
*********************
The following methods outline how to pull data in various situations

Pull One Field from One Record
------------------------------
Let ``page`` and ``proj`` be as above and suppose that we are looking to pull the `age` field from the record `record1`.

    >>> rc = RedCurl(page,token=proj)
    >>> data = rc.pullrec('record1',fields='age')
    >>> print data
    [{'age':'99'}]
    >>> rc.exit()

Pull Multiple fields from One Record
------------------------------------
Let ``page`` and ``proj`` be as above and suppose that we are looking to pull the `id`, `weight` and `handedness` fields from the record `record1`.

    >>> rc = RedCurl(page,token=proj)
    >>> data = rc.pullrec('record1',fields=['id','weight','handedness'])
    >>> print data
    [{'id':'record1','weight':'999','handedness':'0'}]
    >>> rc.exit()

OR

    >>> rc = RedCurl(page,token=proj)
    >>> data = rc.pullrec('record1',fields='id,weight,handedness')
    >>> print data
    [{'id':'record1','weight':'999','handedness':'0'}]
    >>> rc.exit()

Pull Multiple fields from Multiple Records
------------------------------------------
Let ``page`` and ``proj`` be as above and suppose that we are looking to pull the `id`, `weight` and `handedness` fields from the records `record1` and `record2`.

    >>> rc = RedCurl(page,token=proj)
    >>> data = rc.pullrec(['record1','record2'],fields=['id','weight','handedness'])
    >>> print data
    [{'id':'record1','weight':'999','handedness':'0'},{'id':'record2','weight':'999','handedness':'0'}]
    >>> rc.exit()

OR

    >>> rc = RedCurl(page,token=proj)
    >>> data = rc.pullrec('record1,record2',fields='id,weight,handedness')
    >>> print data
    [{'id':'record1','weight':'999','handedness':'0'},{'id':'record2','weight':'999','handedness':'0'}]
    >>> rc.exit()

As you've probably noticed RedCurl doesn't really care if you give it a list of fields or a csv format of field names.  Under the hood it is reformatting a list input 
into a comma separated string.  Which ever input is easiest for your process is the one you should use.

Note: if no fields are provided then all fields will be pulled

Pull All Data from all Records
------------------------------
There are cases when attempting to output in json format fails due to the large number of fields, ergo to pull all fields for all records the ``fullpull`` method 
leverages the csv format.  Let ``page`` and ``proj`` be as above and suppose we want to pull all fields from all records where all records consists of 50 records.

    >>> rc = RedCurl(page,token=proj)
    >>> db = rc.fullpull()
    >>> len(db)
    50
    >>> rc.exit()


Upload data to RedCap
*********************
The following methods outline how to upload data to redcap in various situations

Upload Record Data
---------------------
Let ``page`` and ``proj`` be as above and suppose that we are looking to set the `age` field to `98` for the record identified by `record1`.

    >>> rc = RedCurl(page,token=proj)
    >>> data = rc.pushrec('record1',{'age':'98'})
    >>> print data #print the server's response
    1
    >>> rc.exit()

This method is only implemented for a single record.  There was nothing special about the choice to populate `age`, we could have provided as many ``(key,value)`` pairs
as we wanted to upload to `record1` e.g. assuming ``rc`` from above we have:

    >>> data = rc.pushrec('record1',{'age':'98','handedness':'0','weight':'889'})
    >>> print data #print the server's response
    1
    >>> rc.exit()

The code above would update the `age`, `handedness` and `weight` fields to the values provided.

Upload a file to RedCap
-----------------------
Let ``page`` and ``proj`` be as above and suppose that we are looking to upload the local file `report.pdf` to the field `report_1` for the record identified by `record1`.

    >>> rc = RedCurl(page,token=proj)
    >>> file2load = '/local/path/to/report.pdf'
    >>> data = rc.pushfile('record1','report_1',file2load,'report.pdf')
    >>> print data
    1
    >>> rc.exit()

note that the 4th argument was `report.pdf` this is the name as it should appear in RedCap.  Hence if we wanted to rename our file to `final_report.pdf` we could have written:

    >>> file2load = '/local/path/to/report.pdf'
    >>> data = rc.pushfile('record1','report_1',file2load,'final_report.pdf')
    >>> print data
    1
    >>> rc.exit()