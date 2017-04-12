# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 12:44:26 2016

@author: U6038155
Remove commas in Name
"""

import sys
import requests
import os
import json

match_url = 'https://api.thomsonreuters.com/permid/match/file'
access_token = 'D9SMlZ7K9fPDzsmduzzhVDDdcnVAbDK3'
input_file = 'C:\\Users\\u6038155\\Documents\\Clients\\SCB\\permid_upload.csv'# change this
output_dir = 'C:\\Users\\u6038155\\Documents\\Clients\\SCB' #sys.argv[2]

def main():
    try:
        if len(sys.argv) < 0:       # not using this option
            print '2 params are required: 1.input file full path and 2.output directory'
            sys.exit(-1)
        else:
            input_file = 'C:\\Users\\u6038155\\Documents\\Clients\\SCB\\permid_upload.csv'
            output_dir = 'C:\\Users\\u6038155\\Documents\\Clients\\SCB' #sys.argv[2]

            if not os.path.exists(input_file):
                print 'The file [%s] does not exist' % input_file
                return
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

        headers = {'X-AG-Access-Token' : access_token, 'x-openmatch-numberOfMatchesPerRecord' : '10', 'x-openmatch-dataType' : 'Organization'}
        sendFiles(input_file, headers, output_dir)
    except Exception ,e:
        print 'Error in connect ' , e

def sendFiles(files, headers, output_dir):
    is_file = os.path.isfile(files)
    if is_file == True:
        sendFile(files, headers, output_dir)
    else:
        for file_name in os.listdir(files):
            if os.path.isfile(file_name):
                sendFile(file_name, headers, output_dir)
            else:
                sendFiles(file_name, headers, output_dir)

def sendFile(file_name, headers, output_dir):
    files = {'file': open(file_name, 'rb')}
    response = requests.post(match_url, files=files, headers=headers, timeout=80)
    print 'status code: %s' % response.status_code
    content = response.text
    print 'Results received: %s' % content
    if response.status_code == 200:
        saveFile(file_name, output_dir, content)

def saveFile(file_name, output_dir, content):
    output_file_name = os.path.basename(file_name) + '.xml'
    output_file = open(os.path.join(output_dir, output_file_name), 'wb')
    output_file.write(content.encode('utf-8'))
    output_file.close()

if __name__ == "__main__":
# Loop through the large file; need to parse file 1000 by 1000 and monitor progress in case failure
# Step 1: Match PermIDs through website
   main()
   # ingest output json file
   os.chdir(output_dir)
   json_data = open(input_file+'.xml', 'rb').read()
   
   data = json.loads(json_data)     # output is in json format; data is in dict
# Step 2: Segregate matches to 2 categories     # one with permid and one without. 

# Step 3: Create rdf file to input into DataFusion

# Repeat process