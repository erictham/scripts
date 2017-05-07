# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 15:32:43 2016

@author: U6038155
"""

from tika import parser
from feedparser import parse
from requests import get
from subprocess import Popen, PIPE, STDOUT, call
from trit_gen import removeIndent, removePunc, removeTitle, TRITGEN_TIMEOUT
import sys, codecs
import datetime, time
from os import mkdir, path

#unicodeData.encode('ascii', 'ignore')
reload(sys)
sys.setdefaultencoding('utf8')
tot_docs_pass = 0
tot_docs_fail = 0

def main(argv):
    if len(sys.argv) > 1:
        req = sys.argv[1]
    else: req = "zawya"
    #print req
    dayperiod = datetime.datetime.now()
    am_pm = "0800"
    if dayperiod.hour > 12: am_pm = "2000"
   # pwd = getcwd()
    fname = '/home/ec2-user/trit/rss_sites.txt'
    ffile = codecs.open(fname, 'rb', encoding='utf-8')
    exkey=''
    urldict={}
    # Looping through different news agencies
    for line in ffile:
        url = line.split('#')
        if not url[0] =="#":
            url[0]=url[0].strip().replace('\n','').replace('\r', '')
            if len(url) <> 1:   # news agency
                urldict[exkey].append(url[0].strip(' '))
            else:       # this will be hit first
                exkey = url[0]
                urldict[exkey]=[]
    # unfortunately each website has a different structure that may change dynamically      
    #print urldict

    today= str(datetime.date.today()).replace("-","")
    rss_output = '/home/ec2-user/trit/rdf/'+ today + '_'+ am_pm +  '.nt'
    foutput = open(rss_output, 'wb')
    for agency, typeslist in urldict.items():   #urlreq -> no 4 types of rss feeds
        if agency == req or True : #or agency == 'cna': running through entire script
            for newsurl in typeslist:     # sub-types in news agency
                ok=0
                notok =0           
                print 'doing newsurl ' + newsurl
                rss = parse(newsurl)    
                for rss_entry in rss['entries']:  
                    try:
                    # fields to keep: url link, published, summary
                        url_link = rss_entry['link']
                        url_content = get(url_link, timeout=TRITGEN_TIMEOUT)
                    #    url_content.encoding('utf-8')
                     #   print 'Url_link is ' + url_link
                        ftemp = codecs.open('/home/ec2-user/trit/rss_temp.txt', 'wb', encoding='utf-8')
                        
                        if url_content.ok == True:
    #                            url_pub = rss_entry['published']
    #                            url_label = rss_entry['title']
    #                            print url_label
    #                            url_title = removePunc(url_label).replace(' ','')
    #                            url_summary = rss_entry['summary']
                      #      print 'Stage 1 ' + str(ok)
                            ok=ok+1                            
                            ftemp.write(url_content.content)
                            proc1=Popen(['java', '-jar', '/home/ec2-user/trit/tika-app-1.14.jar', '--text-main', 'rss_temp.txt', ], stdout= PIPE)
                          # proc2=Popen(['java', '-jar', 'tika-app-1.14.jar', '--metadata', 'rss_temp.txt', ], stdout= PIPE)
    
                           # tikadict ={}                            
    #                            for line in proc2.stdout:
    #                                ext = line.split(':')
    #                                tikadict[ext[0]] = ext[1]
                           # tikadict = {line.split(':')[0]:removePunc(line.split(':')[1])  for line in proc2.stdout}
    
                            url_pub = rss_entry['published']
                            url_label = removePunc(rss_entry['title'])
                       #     print 'Stage 2 ' 
                            url_title = removeTitle(url_label)
                            url_summary = removePunc(rss_entry['summary'])
                        #    print 'Stage 3'
                            
                            rdf1=u'<http://www.thomsonreuters.com/news/'+agency+u'/'+ url_title + u'> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://rdf.entagen.com/ns/type/document> .\n'
                            rdf2=u'<http://www.thomsonreuters.com/news/'+agency+u'/'+ url_title + u'> <http://www.w3.org/2000/01/rdf-schema#label> \"' + url_label + u'\" .\n'
                            rdf3=u'<http://www.thomsonreuters.com/news/'+agency+u'/'+ url_title + u'> <http://doc.thomsonreuters.com/pubtime> \"' + url_pub + u'\" .\n'
                            rdf4=u'<http://www.thomsonreuters.com/news/'+agency+u'/'+ url_title + u'> <http://ont.thomsonreuters.com/Summary> \"' + url_summary + u'\" .\n'
                            rdf5=u'<http://www.thomsonreuters.com/news/'+agency+u'/'+ url_title + u'> <http://doc.thomsonreuters.com/url> \"' + url_link + u'\" .\n'
                            rdf6=u'<http://www.thomsonreuters.com/news/'+agency+u'/'+ url_title + u'> <http://doc.thomsonreuters.com/RssSource> \"' + agency + u'\" .\n'
                            rdf7=u'<http://www.thomsonreuters.com/news/'+agency+u'/'+ url_title + u'> <http://rdf.entagen.com/ns/pred/document> \"'

                            rdf = rdf1+rdf2+rdf3+rdf4+rdf5+rdf6+rdf7
                         #   rdf = rdf.decode('utf-8')
                            foutput.write(rdf)
                         #   print 'Stage 4'
                            for line in proc1.stdout:
                                #fcontent=fcontent.join(removePunc(line))
                                #print type(line)
                                #foutput.write(removePunc(removeIndent(line.encode('utf-8'))))
                                foutput.write(removePunc(removeIndent(line)))
                                #print line
                            #print proc1.stdout.readlines()
                       #     print 'Stage 5'
                            foutput.write(u'\" . \n')
                       #     print 'Stage 6'
                       #     print "No " + str(ok) + " done ok"
                           #parsed = parser.from_buffer(url_content.content)
                            ftemp.close()
                        else:
                            print "url not ok:" + url_link
                    except : #ValueError:
                        print "Unexpected error:", sys.exc_info()[0]
                        print 'Error Stage for ' + url_link
                        foutput.write(u"\" . \n")
                        notok = notok+1
                print "Number passed for url " + newsurl + " : " + str(ok)
                print "Number failed for url " + newsurl + " : " + str(notok)
    foutput.close()
    
if __name__ == "__main__":
    today= str(datetime.date.today()).replace("-","")
    dayperiod = datetime.datetime.now()
    am_pm = "0800"
    if dayperiod.hour > 12: am_pm = "2000"
  #  if not path.exists('/home/ec2-user/trit/rdf/'+ today):
 #       mkdir('/home/ec2-user/trit/rdf/'+ today)
    start=time.ctime()
    print "Start datetime: " + start
    starttime = time.time()
    main(sys.argv[0])
    endtime = time.time()
    print "Total time taken in mins: " + str((endtime-starttime)/60.0)
   # call(["tar", "-zvcf", today+am_pm+".tar.gz", today+"/"])
    # create gz folder at the end
    
    # automate emails
    #fname = '/home/ec2-user/trit/rdf/'+today+am_pm+'.tar.gz'
    #ffile =open(fname, 'rb')
    #send_mail("datafusion@gmail.com", ["eric.tham@tr.com", "eric.tham@sc.com", "Peter.FreiherrVonBredow@sc.com","farzana.jabin@sc.com"], "TRIT RSS for date: "+today+" at " + am_pm + " hrs" , "This is an automated email from TR Datafusion team.", files= ffile)
    #ffile.close()