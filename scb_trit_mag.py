# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 13:33:36 2017

@author: U6038155
"""


import os,re
from tika import parser
from trit_gen import removeIndent, removePunc, removeTitle, removeWS
from subprocess import Popen, PIPE, STDOUT

dirw = 'C:\Users\u6038155\Documents\Scripts'
os.chdir(dirw+"\\mag")
pwd = os.getcwd()

i=1
if __name__ == "__main__":
#1 Loop through folder for all documents
    frdf = open("mag_rdf.nt","wb")
    for fname in os.listdir(pwd):
        if fname.find(".pdf")<>-1:

            # for metadata
            proc_m=Popen(['java', '-jar', 'tika-app-1.14.jar', '--metadata', fname, ], stdout= PIPE)
            
            i=i+1
            ffile=open(fname, "rb")
            parsed=parser.from_buffer(ffile)
            
            meta=parsed['metadata']
            title=re.sub(".pdf", "", fname)
            title=removeTitle(title)
            createdate = re.sub(".doc", "", meta['Creation-Date'])
            
            
            content=removeIndent(parsed['content'])
            
            nlen=5000
            ncount=int(len(content)/nlen)
            for i in range(ncount-1):
                title_s=title+"_"+str(i)
                out1 = "<http://doc.sc.com/mag/"+title_s+"> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://rdf.entagen.com/ns/type/document> .\n"
                out2 = "<http://doc.sc.com/mag/"+title_s+"> <http://www.w3.org/2000/01/rdf-schema#label> \""+title_s+"\" .\n"
                out3 = "<http://doc.sc.com/mag/"+title_s+"> <http://doc.thomsonreuters.com/pubtime> \""+createdate +"\" .\n" 
                

                tempcontent=removePunc(content[i*nlen:(i+1)*nlen])
                out4 = "<http://doc.sc.com/mag/"+title_s+"> <http://rdf.entagen.com/ns/pred/document> \""+tempcontent+"\" .\n"
                out=out1+out2+out3+out4
                frdf.write(out)
                #frdf.write(u'\" . \n')
                    
                    
#                pattern=re.compile("{*}")
#                res=re.search(r'({.+})', content)
                # Content to add in:
                # Look for first { *** }
                # { CORPORATE FINANCIAL MANAGEMENT }, { ... }
                # Add in content to the next { ... }
                # 
#                no1=content.count('{')
#                no2=content.count('}')
#              #  patt1= re.compile(r'{.*',re.DOTALL)
#                patt2= re.compile(r'({.*})(.*)',re.DOTALL)
#                patt3= re.compile(r'({.*})(.*)?',re.DOTALL)
#                patt4= re.compile(r'({.*})(.*)?',re.DOTALL)
              

                
    frdf.close()
    ffile.close()

#3 Go through entity resolution
    #rline = file_output.read()


#out4 = out4 + rline
#foutput = open(foutput, 'wb')

#ffile.close()
#foutput.close()