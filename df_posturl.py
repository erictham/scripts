# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 14:14:17 2016

@author: U6038155
"""

from df_genwin import get_DFtoken
import requests
from os import chdir, getcwd
import datetime, time, json, pycurl, StringIO
import pandas as pd




if __name__ == "__main__":
    ndate = datetime.datetime.now()
    eunixtime = int(time.mktime(ndate.timetuple()) * 1000)
    
    #payload = {'entitytype}
    
    # to get access token
    token = get_DFtoken()
    
    
    pwd = 'C:\\Users\\u6038155\\Documents\\Clients\\SCB\\'    #change this
    chdir(pwd)
    ffname = "macysclients.txt"
    ffile = open(ffname, 'rb')

    result=[]
    res ={}
    clients = [u.replace('\r\n','') for u in ffile ]
    properties = pd.DataFrame(range(len(clients)))
#    q_1 = htmlcode('entityTypeId=16&includePredicates=false&includeRelDir=false&includeHiddenFields=true')
#    q_2 = htmlcode('&queryFilter=context|||OA&filterType=and')
#    q_3 = htmlcode('&extraFields=organizationCountry_attr,CommonName_attr,officialName_attr,headquartersCommonAddress_attr')
    q_1 = "properties?uri=" 
    q_3 = "&properties=CommonName_attr%2CorganizationCountry_attr"

    result=[]
    i=1
    #q_2 = htmlcode(q_2)   
    for c in clients:
        q = q_1 + htmlcode(c) + htmlcode(q_3)

        url = url_dds_test + q
    
        data = retURL(url, token)
        res = {i['predicate'] : i[u'object'] for i in data}
        res['permid'] = c
        result.append(res)
        i=i+1
        print i
    df_res = pd.DataFrame(result)
        #properties['PermID_attr'] = [ a.get('PermID_attr',None) for a in data ]
#        res[u'permid']=c
#        try:
#            res[u'organizationCountry_attr']=data[0][u'object']
#            res[u'CommonName_attr']=data[1][u'object']
#            result.append(res)
#        except IndexError:
#            continue
        #print data
