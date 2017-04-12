# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 11:01:39 2017

@author: 1557264
"""

from os import getcwd, chdir
from pycurl import

chdir("/data/trstore")
fname = "sc_model_tr_groupby.csv"
fnameout = "sc_model_tr_groupby.nt"
fout = open(fnameout, "wb")

with open(fname, "rb") as ffile:
    next(ffile)
    for l in ffile:
        if not l.find("NULL") <> -1:
            out= l.split("\t")
            r1="<http://ont.scb.com/partyid/"+out[0]+"> "
            r2="<http://ont.scb.com/property/hasTransaction> "
            r3="<http://ont.scb.com/partyid/"+out[1]+"> .\n"
            r=r1+r2+r3
            fout.write(r)
fout.close()
ffile.close()

