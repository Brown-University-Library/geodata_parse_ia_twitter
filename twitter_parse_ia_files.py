# -*- coding: utf-8 -*-
"""
Reads JSONL Twitter archive files from Internet Archive for a
single day and exports geocoded records to a new JSON file

https://archive.org/details/twitterstream

Frank Donnelly GIS and Data Librarian
Brown University Library
April 26, 2023 / Rev Sept 28, 2023
"""
import os,json

#json_dir is the directory that contains a day's worth of files
#Make sure you unzipped them first! This directory should be below the
#directory where this script is stored:

json_dir='20221101'

outfolder='output'
if not os.path.exists(outfolder):
    os.makedirs(outfolder)

json_list=[] # list of lists, each sublist has 1 string element = 1 line

for path, dirs, files in os.walk(json_dir):
    for f in files:
        if f.endswith('.json'):
            json_file=os.path.join(path,f)
            with open(json_file,'r',encoding='utf-8') as jf:
                jfile_list = list(jf) # create list with one element, a line saved as a string 
                json_list.extend(jfile_list)
                print('Processed file',f,'...')

print("Finished reading",len(json_list),'records into list')
print('Converting geocoded JSONL records to dictionary now...')

# This block creates parsed dicts and only pulls records that have a geo
# element. You can change geo to another element to generate different extracts
# Takes awhile to run...

geo_dict={} # dictionary of dicts, each dict has line parsed into keys / values
i=0   
for json_str in json_list:
    result = json.loads(json_str) # convert line / string to dict
    if result.get('geo')!=None: # only take records that were geocoded
        geo_dict[result['id']]=result 
    i=i+1
    if i%100000==0:
        print('Processed',i,'records...')
    
print('Finished pocessing',i,'records.')    
print('Created dictionary with',len(geo_dict),'geocoded records...')

outfile=json_dir+'_all_records_with_geo.json'
outpath=os.path.join(outfolder,outfile)
print('Writing output for all geo records...')
with open(outpath,'w',encoding='utf-8') as outf:
    json.dump(geo_dict, outf)
    
print('Wrote output file - Done!')
    

