# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 15:57:25 2016

@author: U6038155
"""

import os,re
from trit_gen import removeIndent, removePunc, removeTitle, TRITGEN_TIMEOUT, removeWS
from subprocess import Popen, PIPE, STDOUT

dirw = 'C:\Users\u6038155\Documents\Scripts'
os.chdir(dirw+"\\bca")
pwd = os.getcwd()

i=1
if __name__ == "__main__":
#1 Loop through folder for all documents
    frdf = open("bca_rdf.nt","wb")
    for fname in os.listdir(pwd):
        if fname.find(".doc")<>-1:
            
            proc_c=Popen(['java', '-jar', 'tika-app-1.14.jar', '--text-main', fname, ], stdout= PIPE)
            proc_m=Popen(['java', '-jar', 'tika-app-1.14.jar', '--metadata', fname, ], stdout= PIPE)
            i=i+1
            j=1
            meta={}
            for l in proc_m.stdout:
                l=removeIndent(l)
                lcontent = l.split(":")                
                meta[lcontent[0]]=removeWS(lcontent[1])
                #proc_m=
            print meta
            title = re.sub(".doc", "", meta['resourceName'])
            createdate = re.sub(".doc", "", meta['Creation-Date'])
            # Create RDF file to pump in
            out1 = "<http://doc.sc.com/"+removeTitle(title)+"> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://rdf.entagen.com/ns/type/document> .\n"
            out2 = "<http://doc.sc.com/"+removeTitle(title)+"> <http://www.w3.org/2000/01/rdf-schema#label> \""+title+"\" .\n"
            out3 = "<http://doc.sc.com/"+removeTitle(title)+"> <http://doc.thomsonreuters.com/pubtime> \""+createdate +"\" .\n" 
            out4 = "<http://doc.sc.com/"+removeTitle(title)+"> <http://rdf.entagen.com/ns/pred/document> \""
            out=out1+out2+out3+out4
            frdf.write(out)
            for line in proc_c.stdout:
                j=j+1
                frdf.write(removePunc(removeIndent(line)))
            frdf.write(u'\" . \n')
    frdf.close()

#3 Go through entity resolution
    #rline = file_output.read()


#out4 = out4 + rline
#foutput = open(foutput, 'wb')

#ffile.close()
#foutput.close()