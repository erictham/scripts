# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 15:33:57 2016

@author: U6038155
"""

from trit_gen import convert_nt, CALAIS_URL, SCB_URL, ACCESS_TOKEN
import requests, re
from os import listdir, chdir, getcwd, makedirs
from os.path import isfile, join, exists, basename

access_token="D9SMlZ7K9fPDzsmduzzhVDDdcnVAbDK3"

def toTRIT(input_dirfile, token=""):
    # input_dirfile: either a file or directory input
    # output_dir : folder to save into; if empty will be saved into the same folders
    # 'outputformat': 'xml/rdf', 'application/json', 'text/n3'
    # 'Content-Type': 'text/xml', 'text/raw', 'text/html', 'application/pdf'
    # 'x-calais-contentClass': 'new', 'research'
    # 'omitOutputtingOriginalText': 'true', 'false' (by default)
    # 'x-calais-language': 'English', 'French', 'Spanish'
    # 'x-calais-selectiveTags': 

    is_file = isfile(input_dirfile)
    if is_file == True:
        toTRIT_SendFile(input_dirfile, headers, output_dir)
    else:
        for fname in listdir(input_dirfile):
            if isfile(input_dirfile+"\\"+fname) and fname.find(".txt") <> -1 :
                toTRIT_SendFile(input_dirfile+"\\"+fname, headers, output_dir)

def toTRIT_SendFile(calais_url, file_name, headers="", token="", output_dir=""):
    if token<>"":
        headers = {'Content-Type' : 'text/raw', 'outputformat' : 'xml/rdf'}
    filen = {'file': open(file_name, 'rb')}
    response = requests.post(calais_url, files=filen, headers=headers, timeout=80)
    print 'status code: %s' % response.status_code
    content = response.text
    print 'TRIT send file results received: %s' % content
    if response.status_code == 200:
        if output_dir<>"":
            toTRIT_SaveFile(file_name, content, output_dir)
        else:
            toTRIT_SaveFile(file_name, content, output_dir)
            
def toTRIT_SaveFile(file_name, content, output_dir):
    output_file_name = basename(file_name) + '.rdf'
    output_file = open(join(output_dir, output_file_name), 'wb')
    output_file.write(content.encode('utf-8'))
    output_file.close()
    
    # convert to nt file regardless
    output_file = open(join(output_dir, output_file_name), 'rb')
    convert_nt(output_file_name)
    output_file.close()
   
if __name__ == "__main__":
# Use either 
# i.  toTRIT to send whole directory
# ii. toTRIT_SendFile to send individual file
    pwd=getcwd()
    fname = pwd+"\\scb_bca.txt"
    output_folder = pwd+"\\nt"
    url =SCB_URL
    token=ACCESS_TOKEN
    headers={'X-AG-Access-Token' : token, 'Content-Type' : 'text/raw', 'outputformat' : 'xml/rdf'}

    inputfolder=""
    #toTRIT("dir_name")
    toTRIT_SendFile(url, fname, headers)
# Output files are in RDF format in the same directory and convertible to nt format
    
    
    
    