"""
Date    : January 13, 2017
Author  : Radha 
Purpose : The purpose of the file is to perform entity resolution
"""

import random
from getdftoken import get_token, get_data, get_token, get_token_ddstest
import json
import pandas as pd 
from pandas.io.json import json_normalize
import requests
import re
import distance
import numpy as np
import time

# These functions compute the string that is nearest to the input_string
# based on levenstein distance
def find_closest_string_from_list(input_string, population):
    temp_dist = [distance.levenshtein(a[1].lower(),input_string) for a in population]
    lev_distance = min(temp_dist)
    return (population[np.argmin(temp_dist)],lev_distance)


def entity_resolution(input_data, id_col,name_col, cleansed_name_col,
                      country_col, country_filter, limit ):
    temp                              = input_data
    token                             = get_token()
    prefix                             = 'http://10.21.208.205/datafusion/api'
    match_results                     = pd.DataFrame()
    match_results['name']             = None
    match_results['matched_name']     = None
    match_results['normalized_name']  = None
    match_results[id_col]             = None
    match_results['matches']          = 0
    match_results['match_status']     = 0
    match_results['score']            = 0
    match_results['permid']           = None
    match_results['samples']          = None
    match_results['levenstein']       = 0
    api_call                          = '/entity/search'
    postfix                           = ''
    df_api_call                       = prefix + api_call + postfix
    url                               = df_api_call
    headers                           = {'Authorization': token,'Accept': 'application/json'}
    i                                 = 0
    total_matches                     = 0
    total_records                     = len(temp)
    i = 0
    start                             = time.time()
    for i  in range(total_records):
        print i
        temp_country =  temp[[country_col]].iloc[i,0] 
        temp_name   =  temp[[name_col]].iloc[i,0]
        normalized_name = temp[[cleansed_name_col]].iloc[i,0]
        temp_id         = temp[[id_col]].iloc[i,0] 
        lev_distance = 0
        if country_filter==False:
            search_string = 'CommonName_attr:'+ normalized_name + '*'
        else:
            search_string = 'CommonName_attr:'+normalized_name+'*'+ ' AND organizationCountry_attr:'+temp_country
        payload = {'entityTypeId':5,
                   'searchString':search_string,
                   'start' : 0, 
                   'limit' : limit,
                   'queryFilter':'context|||OA',
                   'includePredicates':False,
                   'includeRelDir':False, 
                   'filterType':'and',
                   'extraFields':'CommonName_attr',
                   'includeHiddenFields':False}
        r = requests.get(url, headers= headers, params=payload, verify=False)
        result = json.loads(r.content)
        matches  = result['totalCount']
        match_status = (matches>0)*1
        match_results.loc[i,id_col]            = temp_id
        match_results.loc[i,'name']            = temp_name
        match_results.loc[i,'normalized_name'] = normalized_name
        if matches == 0 :
            continue
        v = 0
        j = 0
        # Do a string distance matching if number of matches > 1
        if matches > 1 :
            name_matches = []
            for v0 in range(len(result['entities'])):
                common_names = result['entities'][v0].get('CommonName_attr',None)
                if common_names is not None:
                    if type(common_names) is list :
                        for v1 in range(len(common_names)):
                            name_matches = name_matches + [(v0,result['entities'][v0]['CommonName_attr'][v1])]
                    else:
                         name_matches = name_matches + [(v0,result['entities'][v0]['CommonName_attr'])]
                else:
                    common_names = result['entities'][v0].get('label',None)
                    if common_names is not None :
                        name_matches = name_matches + [(v0,result['entities'][v0]['label'])]
                    else:
                        continue
            if len(name_matches) == 0 :
                continue
            match_results.loc[i,'samples'] = " XXXX ".join([a[1] for a in name_matches])
            find_closest  = find_closest_string_from_list(temp_name.lower(), name_matches)
            j             = find_closest[0][0]
            match_string  = find_closest[0][1]
            lev_distance  = find_closest[1]
        else:
            match_string = result['entities'][j]['CommonName_attr']
            if match_string is None :
                match_string = result['entities'][j].get('label',None)
            if match_string is None:
                continue
            if type(match_string) is list : 
                match_string = match_string[0]
        print i, " : ", temp_name, " matched with ", match_string
        match_results.loc[i,id_col]                = temp_id
        match_results.loc[i,'name']                = temp_name
        match_results.loc[i,'normalized_name']     = normalized_name
        match_results.loc[i,'match_status']        = match_status
        total_matches                              = total_matches + match_status
        match_results.loc[i,'matches']             = matches
        match_results.loc[i,'permid']              = result['entities'][j]['subjectUris'][0]
        match_results.loc[i,'score']               = result['entities'][j]['score']
        match_results.loc[i, 'matched_name']       =  match_string
        match_results.loc[i, 'levenstein']         =  lev_distance
        print "Matches =" , total_matches," Processed = ", (i+1), " ER % =",total_matches*100./(i+1)
    elapsed = (time.time() - start)
    print "Time taken ", elapsed 
    total_er_matches = match_results[['match_status']].sum()
    print "total matches = ", total_er_matches
    return match_results



# results= entity_resolution(temp[1:10], id_col, name_col,
#                        cleansed_name_col, country_col,
#                        country_filter, limit)
# results.to_csv("./data/match-results-global-corp-jan-13-2017-v1.csv", encoding='utf-8')

