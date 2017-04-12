# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 14:14:17 2016

@author: U6038155
"""

#import requests
from df_genlinux import htmlcode, unixtime, getToken
from os import chdir
import subprocess,re
import datetime, time, json, pycurl, StringIO

url="\'http://10.21.208.205/datafusion/api/annotation?" 

def postannotatejson(subject, predicate, objectt, tx_amt, activeRange, score, token):       
    url=url+"subject="+ htmlcode(subject)+"&predicate="+htmlcode(predicate)+"&object="+htmlcode(objectt)+"&score=" + str(score)
    url=url+"&activeRange="+str(activeRange[0])+"%20"+str(activeRange[1])+"\'"

    cmd1 = "curl -s -o output.html -X POST --header \'Content-Type: text/plain' --header \'Accept: application/json\' "
    cmd2 = "--header \'Authorization: Bearer " + token + "\' "
    cmd3 = "-d \'{ \"TXN_AMT\": {\"value\": " +str(tx_amt) + ", \"type\": \"NUMBER\"} }\' "
    cmd=cmd1+cmd2+cmd3+url
    #print cmd

    subprocess.call(cmd, shell=True) #, stdout=subprocess.PIPE) # out=STDOUT)

if __name__ == "__main__":
    sdate = datetime.date(2014,6,1)
    edate = datetime.date(2016,12,31)    
    sunixtime = int(time.mktime(sdate.timetuple()) * 1000)
    eunixtime = int(time.mktime(edate.timetuple()) * 1000)
    chdir("/data/trstore")
    fname = "sc_model_tr_groupby.csv"
    #fname_annotate = open(fnameout, "wb")
    token=getToken()
	i=1
    
#    offset = 0  # memory buffer
#    line_offset=[]
    n= 1090000
    
    with open(fname, 'rb') as ffile:
#        for line in fname:
#            line_offset.append(i)
#            offset+=len(line)
        
    #    next(ffile)     # header line
    #    ffile.seek(line_offset[n])
        for line in ffile:
            if i > n:
                try:
                    if not line.find("NULL") <> -1:
                        out = line.replace('\n','').split('\t')
                        
                        subj_uri="<http://ont.scb.com/partyid/"+out[0]+">"
                        obj_uri="<http://ont.scb.com/partyid/"+out[1]+">"
                        pred_uri= "<http://ont.scb.com/property/hasTransaction>"
                        tx_amt=out[2]
                        score =-1
                    
                        if tx_amt > 100000000:	# 
                            score = 1 # to determine strength of predicate
                        elif tx_amt > 10000000:	
                            score = 0.5
                        else:
                            score = 0.2
                        activeRange = [str(sunixtime) , str(eunixtime)]
                        #print activeRange
                        postannotatejson(subj_uri, pred_uri, obj_uri, int(tx_amt), activeRange, score, token)
                except ValueError:  # last line
                    pass
            i=i+1
            if i%5000 ==0:
                print str(i) + " Completed"

    ffile.close()
