""" 
Date   : December 16, 2016
Author  : Radha 
Purpose : The script illustrates the usage of Datafusion APIs 
"""

import pycurl
import json
import StringIO
import requests

    #url="https://dds-test.thomsonreuters.com/datafusion/api/entity/#search/q/" 
    #url="https://dds-test.thomsonreuters.com/explorer/#search/q/defType=edismax&q=United"

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Get the Token for DDS Test
def get_DFtoken(credentials="", url=""):
    """
    Get an access token given the username and password
    """
    if not credentials <> "":
        credentials = ("eric.tham@thomsonreuters.com","datafusion")
        url =  "https://dds-test.thomsonreuters.com/datafusion/oauth/token"
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
    wd.replace(',','%2C')
    wd.replace(' ','%20')
    wd.replace('|','%7C')
    wd.replace(':','%3A')
    wd.replace('/','%2F')
    return wd
	
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
	
# Get the data given an URL using requests
def get_url(url, token, payload="", data = ""):
    headers = {'Content-Type': 'application/json'   , 'Authorization' : 'Bearer ' + token } 
    if payload <> "":
        response = requests.get(url, headers=headers, params=payload, data=data, verify = False)
    elif data <> "":
        response = requests.get(url, headers=headers, data=data, verify = False)
    else:
        response = requests.get(url, headers=headers, verify = False)
        
    try:
        if response.status_code <> 200:
            raise ValueError('Error in HTTP ')
        else:
            #data = response.json()  # output is in Python list
            data = json.loads(response.content)
            #print 'HTTP request is successful with code ' + str(response.status_code )
    except:
        print 'Error in HTTP call ' + str(response.status_code )
        data = ""
    return data

# Get the data given an URL using requests
def post_url(url, token, payload="", data=""):
    headers = {'Content-Type': 'text/plain', 'Authorization' : 'Bearer ' + token } 
    response = requests.post(url, headers=headers, params=payload, data=data, verify = False)
    
    try:
        if response.status_code <> 201:
            raise ValueError('Error in HTTP ')
    except:
        print 'Error in HTTP call ' + str(response.status_code )
    return response.status_code