# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 14:14:17 2016

@author: U6038155
"""

from df_genwin import get_DFtoken, get_url
from os import chdir, getcwd
from sets import Set
import pandas as pd, pickle as pk
import networkx as nx, re as re

if __name__ == "__main__":
    # 1 to get access token 
    df_token = get_DFtoken()
    url = "https://dds-test.thomsonreuters.com/datafusion/api/entity/search"
    
    # 2.1 SEARCH stage through entities for 'General Electric'  (SEARCH)
    extra_fields = "PermID_attr,isDomiciledIn_attr, officialName_attr"
    extra_fields += "organizationCountry_attr"
    payload={}
    payload = {'entityTypeId':16,       # for organisation
             'start' : 0, 
             'limit' : 500, 
             'includePredicates':False,
             'includeRelDir':False, 
             'filterType':'and',
             'includeHiddenFields':False,
             'qf': 'context~OA',        # change this
             'extraFields':extra_fields}
    payload['searchString'] = 'General Electric'    
    data = get_url(url, df_token, payload)

    # 2.2 populate searched results  
    search_dict={}     # original dict of GE entities
    for i in data[u'entities']:
        if i[u'subjectUris'][0].find("permid")<> -1:        # change this
            if u'isDomiciledIn_attr' in i.keys(): 
                search_dict[i[u'subjectUris'][0]] = (i[u'label'], i[u'isDomiciledIn_attr'] ) 
            else:
                search_dict[i[u'subjectUris'][0]] = (i[u'label'], 'Others' ) 
    
    # 3 ANALYZE Search stage through the anchors-(searched entities) 
    anchor = search_dict.keys()
    anchor =  ["http://permid.org/1-4295903128"]
    supply='supplier'
    resume_token = "*"
    
    url="https://dds-test.thomsonreuters.com/datafusion/api/entity/analyze/search"
    payload={}
    payload = {'entityTypeId':16,       # for organisation
         'start' : 0, 
         'level' : 3, 
         'limit' : 1000, 
         'filterType':'and',
         'extraFields':extra_fields,
         'rowsPerLevel':40,
         'token': resume_token,
        # 'searchString':'*:*',
         'searchString':'*General Electric*',
        # 'filterQuery': "NOT tm_id:\"http://rdf.tr.com/entity/1\""}
       #   'filterQuery': "NOT organizationTypeCode_attr:\"Government Department / Agency\""}
         'filterQuery': "organizationTypeCode_attr:\"Business Organization\""}
    j=0
    analyse_nodes={}
    analyse_links={}
    for urikey in anchor:
        payload['uri'] = urikey
        conndata_0 = get_url(url, df_token, payload)
        uri_entities= conndata_0[u'entities']
        uris = [ i[u'subjectUris'][0] for i in uri_entities]
        analyse_paths= conndata_0[u'paths']
     #   anal_matchuri= conndata_0[u'entities']
        analyse_token= conndata_0[u'resumptionTokens']
        
        for i in uri_entities:
            if u'isDomiciledIn_attr' in i.keys(): 
                analyse_nodes[i[u'subjectUris'][0]] ={'index':j, 'label':i[u'label'],'country':i[u'isDomiciledIn_attr']}
            else:
                analyse_nodes[i[u'subjectUris'][0]] ={'index':j, 'label':i[u'label'],'country':'others'}
            j=j+1

   #  do pagination
        for path in analyse_paths:
            for i in range(len(path['predicates'])):
                if path['predicates'][i].keys()[0].lower().find(supply) <> -1:  # consider only the first predicate
                        analyse_links[(path['uris'][i],path['uris'][i+1])]=(i,supply)
                        
    # 4 . Populate GraphX data - finish data download from DataFusion:
    G=nx.Graph()
    G.add_nodes_from([i for i in range(len(analyse_nodes))])
    for key,val in analyse_links.iteritems():
        G.add_edge(analyse_nodes[key[0]]['index'],analyse_nodes[key[1]]['index'])

    for key, val in analyse_nodes.iteritems():
        analyse_nodes[key]['degree']=G.degree(val['index'])
    #    uri_nodes[i[u'subjectUris'][0]]
        
        
    d3input ={}
    nodeslist=[]
    nodeidx_map = {val['index']:key for key, val in analyse_nodes.iteritems()}
    idxnode_map = {key:val['index'] for key, val in analyse_nodes.iteritems()}
    for key, val in analyse_nodes.iteritems():
        node= {'index': val['index'],
                    'uris': key,
                    'label': val['label'],
                    'country': val['country'],
                    'degree': val['degree'],
                    'notional': 100,
                    'id':1000+val['index']}
        if key.find('permid') <> -1:
            permid = re.split('-',key)[1]
            node['EikonWeb_attr']="https://apps.cp.thomsonreuters.com/web/Explorer/Default.aspx?s="+permid+"&st=OAPermID"
        else:
            node['EikonWeb_attr']=""
        node['links']=[]
        for edge in G.edges():
            if val['index'] == edge[0]: node['links'].append(edge[1])
            if val['index'] == edge[1]: node['links'].append(edge[0])
                
        nodeslist.append(node)
                            
    pk.dump(analyse_links, open('C:\\Users\\u6038155\\Documents\\Scripts\\jsoninput.pk', 'wb'))
    pk.dump(data, open('C:\\Users\\u6038155\\Documents\\Scripts\\data.pk', 'wb'))
        
# kick off the iteration from the first results
    # do the first level of relationships
#    json1={}
#    nb=1
#    resume_token = uri_token[0]
#    print "1st Resume token " + str(resume_token[u'complete'])
#    while not resume_token[u'complete'] :
#        payload={ 'entityTypeId':16,       # for organisation
#                  'start' : 0, 
#                  'level' : 2, 
#                  'limit' : 10, 
#                  'rowsPerLevel':25,
#                  'filterQuery': "organizationTypeCode_attr:\"Business Organization\""
##                  "resumptionTokens": [
##                    {
##                      "lastCursorMark": resume_token[u'nextCursorMark'],
##                      #"nextCursorMark": resume_token[u'nextCursorMark'],
##                      "count": resume_token[u'count'],
##                      "totalCount": resume_token[u'totalCount']
##                    }
##                  ]
#                }
#        payload['uri'] = anchor[0]
#        data = {"resumptionTokens": [
#                    {
#                      #"lastCursorMark": resume_token[u'nextCursorMark'],
#                      "nextCursorMark": resume_token[u'lastCursorMark'],
#                      "count": resume_token[u'count'],
#                      "totalCount": resume_token[u'totalCount']
#                    }
#                  ]}
#        conndata_1 = get_url(url, df_token, payload , data)
#        uri_entities= conndata_1[u'entities']
#        uris = [ i[u'subjectUris'][0] for i in uri_entities]
#        uri_paths= conndata_1[u'paths']
#        uri_matchuri= conndata_1[u'entities']
#        uri_token= conndata_1[u'resumptionTokens']
#        print "Size of dict" + str(len(json1))
#        for path in uri_paths:
#            for i in range(len(path['predicates'])):
#                if path['predicates'][i].keys()[0].lower().find(supply) <> -1:  # consider only the first predicate
#                    json1[(path['uris'][i],path['uris'][i+1])]=(i,supply)
#        resume_token = uri_token[0]
#        print 'resume_token: ' + str(nb) + 'token size ' + str(resume_token[u'totalCount'])
#        print "lastCursorMark " + resume_token[u'lastCursorMark']
#        print "nextCursorMark " + resume_token[u'nextCursorMark']
#        print "count "+ str(resume_token[u'count'])
#        print "totalCount " + str(resume_token[u'totalCount'])
#        print "Subsequent Resume token " + str(resume_token[u'complete'])
#        print "nb " + str(nb)
#        nb=nb+1
#        