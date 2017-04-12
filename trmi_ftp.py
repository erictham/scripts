# -*- coding: utf-8 -*-
"""
"""

import ftplib
from pandas import read_csv, DataFrame
from os import chdir
import zipfile as zf
import datetime

    
def download_data(path, localpath):
   
    ftp = ftplib.FTP("mrn-ftp.thomsonreuters.com") 
    ftp.login("loginID", "password") 
    ftp.cwd(path)     # cd to the directory
    fnames = ftp.nlst()      # list of fnames in remote directory to extract from
    
    df= DataFrame()
    for f in fnames:
        if f.find("2014") <> -1:        # this is just to filter out txt files of 2016
            fhandle = open(localpath+"\\"+f, 'wb')
            rmthandle   = path+"/"+f
            ftp.retrbinary('RETR %s' % rmthandle, fhandle.write)
            fhandle.close()
            # open a zip file that is saved by fhandle
            zfile = zf.ZipFile(localpath+"\\"+f, "r") 
            fname = f.replace(".zip",".txt")
            # read the contents of the text file in the zipfile
            zdata = zfile.extract(fname)
            temp = read_csv(localpath+"\\"+fname, sep="\t")
            
            df = df.append(temp)
            zfile.close()


    ftp.quit()
    return df

if __name__ == "__main__":
   # path is the ftp folder to download all the zip files
   # localpath is a temporary folder in the local drive
    path = '/TRMI_TRIAL/CMPNY/5YR/DAI/JP/IND'
    localpath = "C:\\Users\\u6038155\\Documents\\Products\\TRMI"
    chdir(localpath)
    
    df = download_data(path, localpath)
    df['date'] = df['id'].apply( lambda x : x[3:13])
    df['date'] = df['date'].apply( lambda x : datetime.datetime.strptime(x, "%Y-%m-%d"))
    df = df.drop([ u'id', u'systemVersion'], axis =1)
    df = df.sort(["date" ])
    
    
    df_filter = df[df["date"]>datetime.date(2014,6,1)]
    df_filter = df_filter.sort([u'windowTimestamp', "date" ])
    #df_filter.to_csv("test.txt", sep = ",")
    
    #df_cc3 = df_filter[df_filter['ticker']=="CC3"]
    #dfgrp = df.groupby(by = ["ticker"])
    
    