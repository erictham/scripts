# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 12:16:29 2017

@author: U6038155
"""

from df_genwin import get_DFtoken, post_url
from os import chdir, getcwd
import pandas as pd
import requests, math
import re

if __name__ == "__main__":
    
    credentials = ("eric.tham@thomsonreuters.com","4uh-tH4-xLV-r89")
    url="http://54.241.175.235/datafusion/oauth/token"
    token=get_DFtoken(credentials, url)
    #token = get_DFtoken()
    chdir("C:\Users\u6038155\Documents\Clients\KYC Utilities")
    # input csv
    fname = "UOB.csv"
    url="http://54.241.175.235/datafusion/api/entity"
   # url="https://dds-test.thomsonreuters.com/datafusion/api/entity"
    csvdata = pd.read_csv(fname, sep=",", header =0)
    uobdata= csvdata[['Name Screened','Case ID','Entity Type','Nationality']]
    uobdata=uobdata.drop_duplicates()
    
    uobdata['Nationality']= uobdata['Nationality'].fillna("") 
    
    for index, row in uobdata.iterrows():
        label=row['Name Screened']
        uri="http://kyc.thomsonreuters.com/entity/"+re.sub(" ","", label)
        urib="<"+uri+"> "
        if row['Entity Type']=="Org":
            entitytype=5
            enttypeuri="<http://rdf.entagen.com/ns/type/organization> "
        elif row['Entity Type']=="Ind":
            entitytype=6
            enttypeuri="<http://rdf.entagen.com/ns/type/person> "
        caseid=row['Case ID']
        if True:
            nationality=row['Nationality']
        else:
            nationality=""
        payload = {'entityTypeId':entitytype,       # 16 for organisation
         'newEntityUri' : uri, 
         'preferredLabelPredicate' : 'http://www.w3.org/2000/01/rdf-schema#label', 
         'contextId' : 5}     #4 for UOB
        data=urib
        data=data+"<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> "
        data=data+enttypeuri+" .\n"
        data=data+urib
        data=data+"<http://www.w3.org/2000/01/rdf-schema#label> \""
        data=data+label+"\" .\n"
        data=data+urib
        data=data+"<http://kyc.thomsonreuters.com/caseid> "
        data=data+"\""+caseid+"\" .\n"
        data=data+urib
        data=data+"<http://kyc.thomsonreuters.com/nationality> "
        data=data+"\""+nationality+"\" .\n"
        post_url(url, token, payload, data)
    