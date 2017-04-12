""" 
Date   : December 16, 2016
Author  : Radha 
Purpose : The script illustrates the usage of Datafusion APIs 
"""

import pycurl
import json
import StringIO
import time
import re

# Get the Token for DDS Test
def getToken():
    """
    Get an access token given the username and password
    """
	credentials = ("eric.tham@thomsonreuters.com","datafusion")
	url       =  "https://dds-test.thomsonreuters.com/datafusion/oauth/token"
	#token = 'Bearer '+ get_access_token(url, credentials[0], credentials[1])
    auth = { 'username' : credentials[0], 'password' : credentials[1] }
    auth_json = json.dumps(auth)
    #pdb.set_trace()
    buffer    = StringIO.StringIO()
    c         = pycurl.Curl()
    c.setopt(c.URL,url)
    c.setopt(c.HTTPHEADER, ["Content-Type: application/json",'Accept: application/json'])
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.POST,True)
    c.setopt(c.POSTFIELDS, auth_json)
    c.setopt(c.SSL_VERIFYHOST, 0)
    c.setopt(c.SSL_VERIFYPEER, False)
    c.perform()
    c.close()
    access_token = json.loads(buffer.getvalue())['access_token']
    return access_token

# Parse the http address
def htmlcode(wd):
    wd=re.sub(',','%2C',wd)
    wd=re.sub(' ','%20',wd)
    wd=re.sub('|','%7C',wd)
    wd=re.sub(':','%3A',wd)
    wd=re.sub('/','%2F',wd)
	wd=re.sub("<",'%3C',wd)
    wd=re.sub(">",'%3E',wd)
    return wd

def unixtime(dtime)
    unixtime = int(time.mktime(dtime.timetuple()) * 1000)
	return unixtime
	
# Get the data given an URL
def get_data(url, token):
    '''
    Gets the data given a url and a token
    '''
    buffer    = StringIO.StringIO()
    c         = pycurl.Curl()
    c.setopt(c.URL,url)
    c.setopt(c.HTTPHEADER, ["Content-Type: application/json",
                            'Authorization: '+token])
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.SSL_VERIFYHOST, 0)
    c.setopt(c.SSL_VERIFYPEER, False)
    c.perform()
    c.close()
    results = json.loads(buffer.getvalue())
    return results

