# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 14:14:17 2016

@author: U6038155
"""

from df_genwin import get_DFtoken, get_url1
import networkx as nx, re as re
import json
from sets import Set
import time, math

start = time.clock()

# Areas of improvement: 
# i. Type of relationships: HasNTBTxn, HasETBTxn, 
# Add transactional amounts on SCB server

# populate this from file
anchordict={"test":"test","General Electric":"GE", 
            "H&M":"HM", 
            "Inditex":"Inditex"}

#==============================================================================
# def populateFields(entity):
#     labelfields=['isDomiciledIn_attr','hasURL_attr','scbLEID_attr']
#     ptylist=[]
#     if 'isDomiciledIn_attr' in entity.keys(): 
#         ptylist.append(label)
#         
#         search_entities[i[u'subjectUris'][0]] = (i[u'label'], i[u'isDomiciledIn_attr'] ) 
#     else:
#         search_entities[i[u'subjectUris'][0]] = (i[u'label'], 'Others')
#==============================================================================

if __name__ == "__main__":   
    searchString= "General Electric"
    # 1 to get access token 
    df_token = get_DFtoken("http://10.21.208.205/datafusion/oauth/token")
    print df_token
    
    url = "http://10.21.208.205/datafusion/api/entity/search"
    # 2.1 SEARCH stage through entities for 'General Electric'  (SEARCH)
    extra_fields = "isDomiciledIn_attr,hasURL_attr,scbLEID_attr"
   # extra_fields += "PermIdLink_attr,organizationCountry_attr,scbLEID_attr"
    payload={}
    payload = {'entityTypeId':5,       # for organisation
             'start' : 0, 
             'limit' : 5000, 
             'includePredicates':False,
             'includeRelDir':False, 
             'filterType':'and',
             'includeHiddenFields':False,
           #  'qf': 'context~OA',        # change this
           #  'qf': 'context~ETB',        # change this
            #  'queryFilter': 'context|||OA',
             'extraFields':extra_fields}
    payload['searchString'] = searchString    
    connSearch = get_url1(url, df_token, payload)

    # 2.2 populate searched results  
    search_entities={}     # original dict of GE entities
    for i in connSearch[u'entities']:
        #if i[u'subjectUris'][0].find("permid")<> -1:        # change this to include other entities
        fieldlist=[i[u'label']]
        if u'isDomiciledIn_attr' in i.keys(): fieldlist.append(i[u'isDomiciledIn_attr']) 
        else: fieldlist.append('Others')
        if u'hasURL_attr' in i.keys(): fieldlist.append(i[u'hasURL_attr']) 
        else: fieldlist.append('NoUrl')   
        if u'scbLEID_attr' in i.keys(): fieldlist.append(i[u'scbLEID_attr']) 
        else: fieldlist.append('ntb')   
        search_entities[i[u'subjectUris'][0]]=tuple(fieldlist)
#        if u'isDomiciledIn_attr' in i.keys(): 
#            search_entities[i[u'subjectUris'][0]] = (i[u'label'], i[u'isDomiciledIn_attr'] ) 
#        else:
#            search_entities[i[u'subjectUris'][0]] = (i[u'label'], 'Others')
    print len(search_entities)
    
    # 3 ANALYZE Search stage through the anchors-(searched entities) 
    resume_token = "*"
    
    url = "http://10.21.208.205/datafusion/api/entity/analyze/search"
    payload={}
    payload = {'entityTypeId':5,       # for organisation
         'start' : 0, 
         'level' : 1, 
         'limit' : 1000, 
         'filterType':'and',
         'extraFields':extra_fields,
         'rowsPerLevel':40,
         'token': resume_token,
        # 'searchString':'*:*',
       #  'searchString': "CommonName_attr:"+searchString,
         'filterQuery': "organizationTypeCode_attr:\"Business Organization\""}
    j=0
    analyse_nodes={}
    analyse_links={}
    anchor = search_entities
    #anchor = {"http://permid.org/1-4295903128": ('General Electric Co', 'United States')}
    no = 1
    G=nx.Graph()
    Gtry=nx.Graph()
    idxnode_map={}
    nodeidx_map={}
    
    for permID in nodesWithLinks:
        idxnode_map[j]=permID
        nodeidx_map[permID]=j
        j=j+1
        
    for urikey, urival in anchor.iteritems():
        payload['uri'] = urikey
        # adding anchor nodes
        Gtry.add_node(j, 'index'=j, 'label'=urival[0],'country'=urival[1], 'homepage'= urival[2], 'SCB_LEID'=urival[3])
        idxnode_map[j]=urikey
        nodeidx_map[urikey]=j
        analyse_nodes[urikey] ={'index':j, 'label':urival[0],'country':urival[1], 'homepage': urival[2], 'SCB_LEID':urival[3]}
        connAnalyse = get_url1(url, df_token, payload)
        for i in connAnalyse[u'entities']:  # entities from analysing paths of anchor
            fieldlist=[i[u'label']]
            if u'isDomiciledIn_attr' in i.keys(): fieldlist.append(i[u'isDomiciledIn_attr']) 
            else: fieldlist.append('Others')
            if u'hasURL_attr' in i.keys(): fieldlist.append(i[u'hasURL_attr']) 
            else: fieldlist.append('NoUrl')   
            if u'scbLEID_attr' in i.keys(): fieldlist.append(i[u'scbLEID_attr']) 
            else: fieldlist.append('ntb')
            # add related entities to anchor nodes
            Gtry.add_node(j, 'index'=j, 'label'=urival[0],'country'=urival[1], 'homepage'= urival[2], 'SCB_LEID'=urival[3])
            analyse_nodes[i[u'subjectUris'][0]]= {'index':j, 'label':fieldlist[0],'country':fieldlist[1], 'homepage': fieldlist[2], 'SCB_LEID':fieldlist[3]}
            #tuple(fieldlist)
            j=j+1
            
        for path in connAnalyse[u'paths'] :  # analysing paths of anchor
            for i in range(len(path['predicates'])):    # loop through the different predicates; i refers to the level of relationship 0,1,2 for 1st, 2nd and 3rd levels
                # http://permid.org/sc/supplierof_uri
                # http://ont.scb.com/property/hasNtbTransaction
                # http://ont.scb.com/property/hasEtbTransaction
           #     print path['predicates'][i].keys()[0].lower()
           # retrieve transactional amount # loops through the types of relationships for the SAME path
           # 0 is for the first type of relationship     
                if path['predicates'][i].keys()[0].lower().find('hasntbtransaction') <> -1 :
                    try:
                        pred= path['predicates'][i].keys()[0]
                        txnamt= path['predicates'][i][pred][0][u'properties'][0][u'value']
                        txnsum=math.fsum(txnamt)
                    except IndexError:
                        txnsum=0.0
                    analyse_links[(path['uris'][i],path['uris'][i+1])]=(i,"hasntbtransaction", txnamt)
                    try:
                        pred= path['predicates'][i].keys()[0]
                        txnamt= path['predicates'][i][pred][0][u'properties'][0][u'value']
                        txnsum=math.fsum(txnamt)
                    except IndexError:
                        txnsum=0.0
                    analyse_links[(path['uris'][i],path['uris'][i+1])]=(i,"hasetbtransaction",txnamt)
                elif path['predicates'][i].keys()[0].lower().find("supply") <> -1:
                    analyse_links[(path['uris'][i],path['uris'][i+1])]=(i,"supply")
                elif path['predicates'][i].keys()[0].lower().find("supplier") <> -1:
                    analyse_links[(path['uris'][i],path['uris'][i+1])]=(i,"supplier")
                    # consider only the first predicate
        print "no of supply links " + str(len(analyse_links))
        print "no is : " + str(no)
        no=no+1
    # 4 List of companies with and without links
    nodesWithLinks= Set()
    for key in analyse_links.keys():
        nodesWithLinks.add(key[0])
        nodesWithLinks.add(key[1])
    nodesWithoutLinks = Set(analyse_nodes.keys())-nodesWithLinks

    idxnode_map={}
    nodeidx_map={}
    j=0
    for permID in nodesWithLinks:
        idxnode_map[j]=permID
        nodeidx_map[permID]=j
        j=j+1
    # number greater than this has no links
    NbNodesWithoutLinks=len(nodesWithoutLinks)
    NbNodesWithLinks = len(nodesWithLinks)
    for permID in nodesWithoutLinks:
        idxnode_map[j]=permID
        nodeidx_map[permID]=j
        j=j+1
    
    for permID in nodesWithLinks:
        analyse_nodes[permID].update({'index':nodeidx_map[permID]})
    for permID in nodesWithoutLinks:
        analyse_nodes[permID].update({'index':nodeidx_map[permID]})
    
    # 5. Populate GraphX data and do analysis - finish data download from DataFusion:
    
    G.add_nodes_from([i for i in range(len(analyse_nodes))])
    for key,val in analyse_links.iteritems():
        G.add_edge(analyse_nodes[key[0]]['index'],analyse_nodes[key[1]]['index'])
    for key, val in analyse_nodes.iteritems():
        try:
            analyse_nodes[key]['degree']=G.degree(val['index'])
        except KeyError:    # these nodes have no degree / nor links
            analyse_nodes[key]['degree']=0

    # 6. Populate d3json file
    NbLinks = G.number_of_edges()
    nodeslist=[]
    analyse_nodes={nodeidx_map[key]:val for key, val in analyse_nodes.iteritems()}
    # Add up all the connections.
    for key, val in analyse_nodes.iteritems():
        #if key in nodesWithLinks:   # only populate nodes with links 
        score =  1+ 10*val['degree']/NbLinks# determines size of circle depending on notional
        ntb=0
        if val['SCB_LEID']<>'ntb' : ntb=1 
        node= {'index': val['index'],
               'uris': idxnode_map[key],
               'label': val['label'],
               'country': val['country'],
               'degree': val['degree'],
               'notional': 10,    
               'score': score, # determines size of circle
               'id':1000+val['index'],
              # "level": 1
              'ntb': ntb,
              'website':val['homepage'],
              'SCB_LEID':val['SCB_LEID']}
        if idxnode_map[key].find('permid') <> -1:
            permid = re.split('-',idxnode_map[key])[1]
            node['EikonWeb_attr']="https://apps.cp.thomsonreuters.com/web/Explorer/Default.aspx?s="+permid+"&st=OAPermID"
        else:
            node['EikonWeb_attr']=""
        node['links']=[]
        for edge in G.edges():
            if val['index'] == edge[0]: node['links'].append(edge[1])
            if val['index'] == edge[1]: node['links'].append(edge[0])
        nodeslist.append(node)
        
    # populating the links in the ds3json
    linkslist=[]
    #for key, val in analyse_links.iteritems():
    for edge in G.edges():
        link ={"source": edge[0], "target": edge[1]}
        link["weight"]= 0.5 # function of transactional amount
        linkslist.append(link)
    d3json = {"nodes":nodeslist,"links":linkslist, "nodelink": len(nodesWithLinks)}
    json.dump(d3json, open("C:\\Users\\1261391\\Documents\\Website\\scb\\data\\"+anchordict[searchString]+".json", "wb"))
    
    elapsed = (time.clock() - start)

