# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 15:33:57 2016

@author: U6038155
"""

import re, sys
from os import listdir, chdir, getcwd, system, popen, makedirs
from os.path import isfile, join, exists, basename

reload(sys)
sys.setdefaultencoding('utf8')

# for OpenCalais & PermID
CALAIS_URL = "https://api.thomsonreuters.com/permid/calais"
SCB_URL= "http://10.21.208.208/tag/rs/enrich"
ACCESS_TOKEN = "D9SMlZ7K9fPDzsmduzzhVDDdcnVAbDK3"
TRITGEN_TIMEOUT = 5

# convert rdf files to nt format
def convert_nt(frdf="", fpath=""):
    
    rdffiles=[]
    cwd = getcwd()
    if frdf <> "":
        rdffiles.append(join(fpath, frdf))
    else:    # single file
        rdffiles = [f for f in listdir(cwd) if isfile(join(cwd, f)) and f.find('.rdf') <> -1] 
    #output_file_name = re.sub(r"\.[a-zA-Z]+",".nt",file_name)
    jarfile = "rdf2rdf-1.0.1-2.3.1.jar"
    errorfile = []
    
    for f in rdffiles:
        cmmd = "java -jar " + jarfile + " " + f + " " + f.strip(".rdf").rstrip(' -1234567890') + ".nt"
        system(cmmd)
        out = popen(cmmd).read()
        if out.find('Error') <> -1:
            errorfile.append(f)

def removeIndent(phrase):
    phrase=re.sub('\n',' ',phrase)
    phrase=re.sub('\r',' ',phrase)
    phrase=re.sub('\t',' ',phrase)
    return phrase

def removeWS(phrase):
    phrase=re.sub(' ','',phrase)
    return phrase

def removePunc(phrase):
    phrase=re.sub('&',' and ',phrase)
    phrase=re.sub(u"\"","\'", phrase)
    phrase=re.sub("\%","percent",phrase)
  #  phrase=re.sub(',','\,',phrase)
    return phrase

def removeSymbols(phrase):
    phrase=re.sub('\u2022','',phrase)
    return phrase
    
def removeTitle(phrase):
    phrase=phrase.encode('utf-8') 
    phrase=phrase.replace(u',','-')
    phrase=phrase.replace(u' ','-')
    phrase=re.sub("\%","percent",phrase)
    phrase=re.sub(u"\'","-", phrase)
    return phrase