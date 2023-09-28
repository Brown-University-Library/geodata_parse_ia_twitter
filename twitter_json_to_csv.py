# -*- coding: utf-8 -*-
"""
Reads geocoded JSON from Internet Archive output from twitter_parse_ia_files.py
to select a subset of attributes and writes them to a CSV

https://archive.org/details/twitterstream

Frank Donnelly GIS and Data Librarian
Brown University Library
April 26, 2023 / Rev Sept 28, 2023
"""

import json, csv, os

# This is the input file - make sure it is reading the file created by
# twitter_parse_ia_files.py that's stored in the output folder

infile='20221101_all_records_with_geo.json'
input_json=os.path.join('output',infile)

# twit_data is dictionary with id key, and value of dictionary with many sub dicts
with open(input_json) as json_file:
    twit_data = json.load(json_file)

twit_list=[]

# In this block, select just the keys / values to save
for k,v in twit_data.items():
    tweet_id=k
    timestamp=v.get('created_at')
    tweet=v.get('text')
    # Source is in HTML with anchors. Separate the link and source name
    source=v.get('source') # This is in HTML
    if source !='':
        source_url=source.split('"')[1] # This gets the url
        source_name=source.strip('</a>').split('>')[-1] # This gets the name
    else:
        source_url=None
        source_name=None
    lang=v.get('lang')
    # Value for long / lat is stored in a list, must specify position
    if v['geo'] !=None:
        longitude=v.get('geo').get('coordinates')[1]
        latitude=v.get('geo').get('coordinates')[0]
    else:
        longitude=None
        latitude=None
    if v['place'] !=None:
        country=v['place'].get('country')
        ccode=v.get('place').get('country_code')
        place_sht=v.get('place').get('name')
        place_lng=v.get('place').get('full_name')
    else: # Necessary to avoid errors if there are no place elements
        country=None
        ccode=None
        place_sht=None
        place_lng=None
    user_id=v.get('user').get('id')  
    user_name=v.get('user').get('name')
    user_desc=v.get('user').get('description')
    user_loc=v.get('user').get('location')
    user_created=v.get('user').get('created_at')
    followers=v.get('user').get('followers_count')
    friends=v.get('user').get('friends_count')
    # Write most of these to a list (but not source - just get its parts)
    record=[tweet_id,timestamp,tweet,source_url,source_name,lang,longitude,latitude,country,
            ccode,place_sht,place_lng,user_id,user_name,user_desc,user_loc,
            user_created,followers,friends]
    twit_list.append(record) # Append to the main list

# Header for output CSV, must match number and order of record list
header=['tweet_id','timestamp','tweet','source_url','source_name','lang','longitude','latitude','country',
        'ccode','place_sht','place_lng','user_id','user_name','user_desc','user_loc',
        'user_create','followers','friends']
    
filestamp=infile.split('_')[0]
outfile='geotweets_'+filestamp+'.csv'
outpath=os.path.join('output',outfile)
with open(outpath, 'w', newline='',encoding='utf-8') as writefile:
    writer = csv.writer(writefile, quoting=csv.QUOTE_ALL, delimiter=',')
    writer.writerow(header)
    writer.writerows(twit_list)
print('Done!')
