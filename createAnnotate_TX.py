# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 14:14:17 2016

@author: U6038155
"""

#import requests
from os import chdir, getcwd
import datetime, time, json, pycurl, StringIO

if __name__ == "__main__":
    sdate = datetime.date(2016,12,1)
    edate = datetime.date(2016,12,31)    
    sunixtime = int(time.mktime(sdate.timetuple()) * 1000)
    eunixtime = int(time.mktime(sdate.timetuple()) * 1000)
    chdir("/data/trstore")
    fname = "sc_model_tr_groupby.csv"
    fnameout = "sc_model_tr_groupby.json"
    fname_annotate = open(fnameout, "wb")
    
    annot_list=[]
    with open(fname, 'rb') as fname:
        next(fname)     # header line
        for line in fname:
            try:
                # predicate
                out = line.replace('\n','').split('\t')
                subj_uri="<http://ont.scb.com/partyid/"+out[0]+">"
                obj_uri="<http://ont.scb.com/partyid/"+out[1]+">"
                pred_uri= "<http://ont.scb.com/property/hasTransaction>"
                tx_amt=str(out[2])
                # annotation
                jdict ={}
                jdict['subject'] = subj_uri
                jdict['predicate'] = pred_uri
                jdict['object'] = obj_uri
                if tx_amt > 100000000:	# 
                    jdict['score'] = 1 # to determine strength of predicate
                elif tx_amt > 10000000:	
                    jdict['score'] = 0.5
                else:
                    jdict['score'] = 0.2
                jdict['activeRange'] = str(sunixtime) + ' ' + str(eunixtime)
                jdict['properties'] = {'TxnAmt' : {'value' : tx_amt, 'type': 'NUMBER'}}
                
                annot_list.append(jdict)
            except ValueError:  # last line
                pass
    annot_json = {'items': annot_list}
    json.dump(annot_json, fname_annotate)
    
    fname.close()
    fname_annotate.close()
    
    # to get access token
   #credentials = ("radha.pendyala@thomsonreuters.com","johngalt")
   # url       =  "https://dds-test.thomsonreuters.com/datafusion/oauth/token"
   # token = 'Bearer '+ getDFToken(url, credentials[0], credentials[1])
    