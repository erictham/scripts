# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 14:14:17 2016

@author: U6038155
"""

import requests
from os import chdir, getcwd
import datetime, time, json, pycurl, StringIO

def getDFToken(url, username, password):
    """
    Get an access token given the username and password
    """
    auth = { 'username' : username, 'password' : password }
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


def postFile():
    pass

# Obtain contextual lists:
url_dds_test = "http://dds-test.thomsonreuters.com/app/api/context/list"
url_dds = "https://dds.thomsonreuters.com/app/api/context/list"

def retURL(url):
    headers = {  'Content-Type': 'application/json'   , 'Authorization' : 'Bearer hboalirnc3d4n04phhvv2bas8fdjd6h9' } 
    response = requests.get(url, headers=headers)
    
    try:
        if response.status_code <> 200:
            raise ValueError('Error in HTTP ')
        else:
            data = response.json()  # output is in Python list
            print 'HTTP request is successful with code ' + str(response.status_code )
    except:
        print 'Error in HTTP call ' + str(response.status_code )
        data = ""
    return data

def postannotatejson(annotate):   
    url = "https://dds-test.thomsonreuters.com/app/api/annotation/bulk"# change this
    headers = {'Content-Type': 'application/json', 'Accept': 'text/plain', 'Authorization' : 'Bearer ' + token_DF }
    response = requests.post(url, data = json.dumps(annotate), headers=headers, verify = False)
    print "Response code is " + str(response.status_code)# response code if ok should be 
    print response.text
    
if __name__ == "__main__":
    sdate = datetime.date(2016,12,1)
    edate = datetime.date(2016,12,31)    
    sunixtime = int(time.mktime(sdate.timetuple()) * 1000)
    eunixtime = int(time.mktime(sdate.timetuple()) * 1000)
    
    pwd = 'C:\\Users\\u6038155\\Documents\\Clients\\SCB'    #change this
    chdir(pwd)
    
    fname = 'transactions_scb_dec_20_2016.csv'   
    fname_pred = 'rdf_pred.nt'
    fname_annotate = 'rdf_annotate.json'
    fname_pred = open(fname_pred, 'wb')
    fname_annotate = open(fname_annotate, 'wb')
    
    annot_list=[]
    with open(fname, 'rb') as fname:
        next(fname)     # header line
        for line in fname:
            try:
                # predicate
                ddata = line.replace('\n','').replace('\r','').split(',')
                #(no, customer_link_id,counterparty_link_id,customer_permid,counterparty_permid,value,buy_to_sell )               
                subj_uri = "<"+ddata[3]+">"
                if ddata[6] <> "BUYER":
                    pred_uri = "<http://ont.sc.com/SellTo>"
                else:
                    pred_uri = "<http://ont.sc.com/BuyFrom>"
                obj_uri = "<"+ddata[4]+">"
                pred_rdf = subj_uri + ' ' + pred_uri + ' ' + obj_uri + ' .\n'
                fname_pred.write(pred_rdf)
                
                # annotation
                jdict ={}
                jdict['subject'] = subj_uri
                jdict['predicate'] = pred_uri
                jdict['object'] = obj_uri
                jdict['score'] = -1 # to determine strength of predicate
                jdict['activeRange'] = str(sunixtime) + ' ' + str(eunixtime)
                jdict['properties'] = {'TxnAmt' : {'value' : str(ddata[5]), 'type': 'NUMBER'}}
                
                annot_list.append(jdict)
            except ValueError:  # last line
                pass
    annot_json = {'items': annot_list}
    json.dump(annot_json, fname_annotate)
    
    fname_pred.close()
    fname.close()
    fname_annotate.close()
    
    # to get access token
    credentials = ("radha.pendyala@thomsonreuters.com","johngalt")
    url       =  "https://dds-test.thomsonreuters.com/datafusion/oauth/token"
    token = 'Bearer '+ getDFToken(url, credentials[0], credentials[1])
    