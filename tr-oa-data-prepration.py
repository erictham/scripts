""" 
Date   : December 27, 2016
Author  : Radha 
Purpose : This script is to retrieve company information from SCB OA data
"""

from getdftoken import get_token, get_data, get_token_ddstest
import json
from pandas.io.json import json_normalize
import requests
import pandas as pd
import time

#---------------------------------
# Get all the entity types
token = get_token()
prefix       = 'http://10.21.208.205/datafusion/api/'
api_call     = 'entity/types'
postfix      = ''
df_api_call  = prefix + api_call + postfix
results      = get_data(df_api_call, token)
entity_types = json_normalize(results)
entity_types

#---------------------------------
# How many entities are there in the database
token = get_token()

url       =  'http://10.21.208.205/datafusion/api/entity/search'
headers = {'Authorization': token,'Accept': 'application/json'}

extra_fields = "PermID_attr,PermIdLink_attr,CommonName_attr,officialName_attr,"
extra_fields += "shortName_attr,akaName_attr,fkaName_attr,isDomiciledIn_attr,"
extra_fields += "isIncorporatedIn_attr,legalRegistrationCommonAddress_attr,"
extra_fields += "headquartersAddress_attr,headquartersCommonAddress_attr,"
extra_fields += "organizationAddressLine1_attr,organizationAddressLine2_attr,"
extra_fields += "organizationAddressLine3_attr,organizationAddressLine4_attr,"
extra_fields += "organizationAddressLine5_attr,organizationAddressPostalCode_attr,"
extra_fields += "organizationCity_attr,organizationStateProvince_attr,organizationCountry_attr,"
extra_fields += "organizationCountryCode_attr,registeredPhone_attr"

payload = {'entityTypeId':5,
         'start' : 0, 
         'limit' : 1000, 
         'includePredicates':False,
         'includeRelDir':False, 
         'filterType':'and',
         'includeHiddenFields':False}

r = requests.get(url, headers= headers, params=payload, verify=False)
result = json.loads(r.content)
print "There are ", result['totalCount'], " entities under Organization"
total_entities = result['totalCount']
#---------------------------------#
# There are 6047714 entities
headers = {'Authorization': token,'Accept': 'application/json'}

# The main pandas dataframe that contains the data
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
extracted_entities = 0
resume_token = "*"
k = 0
while(extracted_entities < total_entities) :
    results = pd.DataFrame()
    start = time.clock()
    payload = {'entityTypeId':5,
         'limit' : 10000, 
         'includePredicates':False,
         'includeRelDir':False, 
         'filterType':'and',
         'extraFields':extra_fields,
          'resumeToken':resume_token,
         'includeHiddenFields':False}
    r = requests.get(url, headers= headers, params=payload, verify=False)
    result = json.loads(r.content)
    resume_token = result.get('nextResumeToken','DONE')
    sample_oa         = pd.DataFrame(range(len(result['entities'])))
    sample_oa['PermID']= [ a.get('PermID_attr',None) for a in result['entities'] ]
    sample_oa['PermIdLink']= [ a.get('PermIdLink_attr',None) for a in result['entities'] ]
    sample_oa['CommonName']= [ a.get('CommonName_attr',None) for a in result['entities'] ]
    sample_oa['officialName']= [ a.get('officialName_attr',None) for a in result['entities'] ]
    sample_oa['shortName']= [ a.get('shortName_attr',None) for a in result['entities'] ]
    sample_oa['akaName']= [ a.get('akaName_attr',None) for a in result['entities'] ]
    sample_oa['fkaName']= [ a.get('fkaName_attr',None) for a in result['entities'] ]
    sample_oa['isDomiciledIn']= [ a.get('isDomiciledIn_attr',None) for a in result['entities'] ]
    sample_oa['isIncorporatedIn']= [ a.get('isIncorporatedIn_attr',None) for a in result['entities'] ]
    sample_oa['legalRegistrationCommonAddress']= [ a.get('legalRegistrationCommonAddress_attr',None) for a in result['entities'] ]
    sample_oa['headquartersAddress']= [ a.get('headquartersAddress_attr',None) for a in result['entities'] ]
    sample_oa['headquartersCommonAddress']= [ a.get('headquartersCommonAddress_attr',None) for a in result['entities'] ]
    sample_oa['organizationAddressLine1']= [ a.get('organizationAddressLine1_attr',None) for a in result['entities'] ]
    sample_oa['organizationAddressLine2']= [ a.get('organizationAddressLine2_attr',None) for a in result['entities'] ]
    sample_oa['organizationAddressLine3']= [ a.get('organizationAddressLine3_attr',None) for a in result['entities'] ]
    sample_oa['organizationAddressLine4']= [ a.get('organizationAddressLine4_attr',None) for a in result['entities'] ]
    sample_oa['organizationAddressLine5']= [ a.get('organizationAddressLine5_attr',None) for a in result['entities'] ]
    sample_oa['organizationAddressPostalCode']= [ a.get('organizationAddressPostalCode_attr',None) for a in result['entities'] ]
    sample_oa['organizationCity']= [ a.get('organizationCity_attr',None) for a in result['entities'] ]
    sample_oa['organizationStateProvince']= [ a.get('organizationStateProvince_attr',None) for a in result['entities'] ]
    sample_oa['organizationCountry']= [ a.get('organizationCountry_attr',None) for a in result['entities'] ]
    sample_oa['organizationCountryCode']= [ a.get('organizationCountryCode_attr',None) for a in result['entities'] ]
    sample_oa['registeredPhone']= [ a.get('registeredPhone_attr',None) for a in result['entities'] ]
    extracted_entities = extracted_entities + sample_oa.shape[0]
    
    print "Extracted ", extracted_entities ," % done " , extracted_entities*100./total_entities
    results = sample_oa
    elapsed = (time.clock() - start)
    print "time elapsed ", elapsed
    k=k+1
    if k = 2: break
    results.to_json("./data/scoa/oa-"+str(k)+".json")

    
# Work on the csv files
all_oa_data_1 = pd.DataFrame()
all_oa_data_2 = pd.DataFrame()
all_oa_data_3 = pd.DataFrame()
all_oa_data_4 = pd.DataFrame()
all_oa_data_5 = pd.DataFrame()
all_oa_data_6 = pd.DataFrame()

i = 1
for i in range(1, 101):
    print i 
    temp = pd.read_csv("./data/scoa/oa-"+str(i)+".csv")
    all_oa_data_1 = all_oa_data_1.append(temp)

i = 101
for i in range(101, 201):
    print i 
    temp = pd.read_csv("./data/scoa/oa-"+str(i)+".csv")
    all_oa_data_2 = all_oa_data_2.append(temp)

i = 201
for i in range(201, 301):
    print i 
    temp = pd.read_csv("./data/scoa/oa-"+str(i)+".csv")
    all_oa_data_3 = all_oa_data_3.append(temp)


i = 301
for i in range(301, 401):
    print i 
    temp = pd.read_csv("./data/scoa/oa-"+str(i)+".csv")
    all_oa_data_4 = all_oa_data_4.append(temp)

i = 401
for i in range(401, 501):
    print i 
    temp = pd.read_csv("./data/scoa/oa-"+str(i)+".csv")
    all_oa_data_5 = all_oa_data_5.append(temp)

i = 501
for i in range(501, 606):
    print i 
    temp = pd.read_csv("./data/scoa/oa-"+str(i)+".csv")
    all_oa_data_6 = all_oa_data_6.append(temp)

all_oa_data = pd.DataFrame()
all_oa_data = all_oa_data.append(all_oa_data_1)
all_oa_data = all_oa_data.append(all_oa_data_2)
all_oa_data = all_oa_data.append(all_oa_data_3)
all_oa_data = all_oa_data.append(all_oa_data_4)
all_oa_data = all_oa_data.append(all_oa_data_5)
all_oa_data = all_oa_data.append(all_oa_data_6)

all_oa_data.to_csv("./data/all-tr-oa-data.csv")

# The above script creates all-tr-oa-data.csv. This can be further analyzed
