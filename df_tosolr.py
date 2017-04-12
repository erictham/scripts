""" 
Date   : December 27, 2016
Author  : Radha 
Purpose : This script is to retrieve company information from SCB OA data
"""

from gettoken import get_token, get_data, htmlcode
import json
from pandas.io.json import json_normalize
import requests
import pandas as pd
import time

extra_fields = "PermID_attr,PermIdLink_attr,CommonName_attr,officialName_attr,"
extra_fields += "shortName_attr,akaName_attr,fkaName_attr,isDomiciledIn_attr,"
extra_fields += "isIncorporatedIn_attr,legalRegistrationCommonAddress_attr,"
extra_fields += "headquartersAddress_attr,headquartersCommonAddress_attr,"
extra_fields += "organizationAddressLine1_attr,organizationAddressLine2_attr,"
extra_fields += "organizationAddressLine3_attr,organizationAddressLine4_attr,"
extra_fields += "organizationAddressLine5_attr,organizationAddressPostalCode_attr,"
extra_fields += "organizationCity_attr,organizationStateProvince_attr,organizationCountry_attr,"
extra_fields += "organizationCountryCode_attr,registeredPhone_attr"
    
#---------------------------------
# Get token
credentials = ("eric.tham@thomsonreuters.com","datafusion")
url       =  "https://dds-test.thomsonreuters.com/datafusion/oauth/token"
token = get_token(url, credentials[0], credentials[1])
#---------------------------------
# How many entities are there in the database
url       =  'https://dds-test.thomsonreuters.com/datafusion/api/entity/search?'
headers = {'Authorization': 'Bearer '+ token,'Accept': 'application/json'}

payload = {'entityTypeId':16,
         'start' : 0, 
         'limit' : 10, 
         'includePredicates':False,
         'includeRelDir':False, 
         'queryFilter': 'context|||OA',
         'filterType':'and',
         'includeHiddenFields':False}

r = requests.get(url, headers= headers, params=payload, verify=False)
result = json.loads(r.content)
print "There are ", result['totalCount'], " entities under Organization"
total_entities = result['totalCount']
#---------------------------------#
# There are 5372324 entities

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
    payload = {'entityTypeId':16,
         'limit' : 1000, 
         'includePredicates':False,
         'includeRelDir':False, 
         'filterType':'and',
         'extraFields':extra_fields,
         'queryFilter': 'context|||OA',
         'resumeToken':resume_token,
         'includeHiddenFields':False}
    r = requests.get(url, headers= headers, params=payload, verify=False)
    result = json.loads(r.content)
    resume_token = result.get('nextResumeToken','DONE')
    sample_oa         = pd.DataFrame(range(len(result['entities'])))
    sample_oa['PermID']= [ a.get('PermID_attr','') for a in result['entities'] ]
    sample_oa['PermIdLink']= [ a.get('PermIdLink_attr','') for a in result['entities'] ]
    sample_oa['CommonName']= [ a.get('CommonName_attr','') for a in result['entities'] ]
    sample_oa['officialName']= [ a.get('officialName_attr','') for a in result['entities'] ]
    sample_oa['shortName']= [ a.get('shortName_attr','') for a in result['entities'] ]
    sample_oa['akaName']= [ a.get('akaName_attr','') for a in result['entities'] ]
    sample_oa['fkaName']= [ a.get('fkaName_attr','') for a in result['entities'] ]
    sample_oa['isDomiciledIn']= [ a.get('isDomiciledIn_attr','') for a in result['entities'] ]
    sample_oa['isIncorporatedIn']= [ a.get('isIncorporatedIn_attr','') for a in result['entities'] ]
    sample_oa['legalRegistrationCommonAddress']= [ a.get('legalRegistrationCommonAddress_attr','') for a in result['entities'] ]
    sample_oa['headquartersAddress']= [ a.get('headquartersAddress_attr','') for a in result['entities'] ]
    sample_oa['headquartersCommonAddress']= [ a.get('headquartersCommonAddress_attr','') for a in result['entities'] ]
    sample_oa['organizationAddressLine1']= [ a.get('organizationAddressLine1_attr','') for a in result['entities'] ]
    sample_oa['organizationAddressLine2']= [ a.get('organizationAddressLine2_attr','') for a in result['entities'] ]
    sample_oa['organizationAddressLine3']= [ a.get('organizationAddressLine3_attr','') for a in result['entities'] ]
    sample_oa['organizationAddressLine4']= [ a.get('organizationAddressLine4_attr','') for a in result['entities'] ]
    sample_oa['organizationAddressLine5']= [ a.get('organizationAddressLine5_attr','') for a in result['entities'] ]
    sample_oa['organizationAddressPostalCode']= [ a.get('organizationAddressPostalCode_attr','') for a in result['entities'] ]
    sample_oa['organizationCity']= [ a.get('organizationCity_attr','') for a in result['entities'] ]
    sample_oa['organizationStateProvince']= [ a.get('organizationStateProvince_attr','') for a in result['entities'] ]
    sample_oa['organizationCountry']= [ a.get('organizationCountry_attr','') for a in result['entities'] ]
    sample_oa['organizationCountryCode']= [ a.get('organizationCountryCode_attr','') for a in result['entities'] ]
    sample_oa['registeredPhone']= [ a.get('registeredPhone_attr','') for a in result['entities'] ]
    extracted_entities = extracted_entities + sample_oa.shape[0]
    
    print "Extracted ", extracted_entities ," % done " , extracted_entities*100./total_entities
    #results = sample_oa
    elapsed = (time.clock() - start)
    print "time elapsed ", elapsed
    k=k+1
    if k == 2: break
        
# enter into solr index
    solr_url = 'http://localhost:8983/solr/permid/update/json/docs'
    headers = {'Content-Type': 'application/json'}
    #requests.post(solr_url, json = results.to_json() )
    #results.to_json("./oa-"+str(k)+".json")

    


# The above script creates all-tr-oa-data.csv. This can be further analyzed
