# Parse Internet Archive's Twitter Stream Grab

Python scripts for parsing geolocated data downloaded from the *Internet Archive's Twitter Stream Grab* at https://archive.org/details/twitterstream (but can be modified to parse other elements and values as desired). The Internet Archive captured a sample or "sprtizer" of global tweets every day, and provides these in monthly collections. Most of the Twitter APIs ceased functioning in early 2023, so many of the projects and countless web examples that use these APIs to scrape Twitter no longer work. Many of these projects also relied on third party modules with lots of dependencies. The scripts in this repo are designed to operate on one daily file downloaded locally, and use no third party modules.

This script was tested using the daily file from [November 1, 2022](https://archive.org/details/archiveteam-twitter-stream-2022-11). The TAR file contained over 4 million tweets, of which about 1100 were geolocated. The input data is not included in this repo, but the output data is.

# Steps

1. Download this repo, or clone it

2. Download a single, daily file from https://archive.org/details/twitterstream and place it in the same folder as the scripts. The archive file format has differed over time, but is usually a ZIP or TAR file.

3. Unzip the ZIP / TAR file, which creates a subfolder for that date, which contains additional, individual archive files. Again, these archive formats vary and could include tar, zip, gz, bz2, or 7z.

4. Unzip all of the individual archived files, to reveal many individual json files. NOTE: not all of the Internet Archive files are organized in the same way. In this example, the zipped (gz) JSON files are stored directly in the top folder. In other cases, these files may be separated and nested in several subfolders. As long as the top folder is stored in the same folder as the scripts, and all of the JSON files have been unzipped, the script will function properly. There are many programs (7-zip for example) that can be used for unzipping multiple files at once.
   
   ![!Folder with scripts and data subfolder](files_1.png)
   
   ![Subfolder with unzipped data](files_2.png)

5. Open *twitter_parse_ia_files.py* and change the name of the json directory at the top, to match the name of the date subfolder  Run the script. The data is stored in a JSONL format; the script iterates through the JSON files and reads each JSONL record in as a string, which it appends to a list, and then iterates through the list to parse each string to a dictionary. Any dictionary that has geolocated information is saved to a new dictionary, which is output as a regular JSON file.
   
   Note: reading the JSON files into the program happens quickly, but parsing the strings to dictionaries takes a bit longer. You can modify the parsing section to grab tweets based on elements other than the geo element, but be aware this will increase processing time. When I attempted to parse and save all 4 million tweets, memory became an issue and the program ground to a halt after 750,000 records. You will have to apply some filters. As very few records are geolocated, the process ran smoothly.

6. Open *twitter_parse_ia_files.py* and change the name of the input file so it matches the JSON file output by the previous script. This script reads the JSON file, pulls out specific elements and values, and writes these to a list structure that is output to a CSV. Values that include longitude and latitude were captured, so the tweets can be plotted in GIS. 

If you want to modify what's extracted in step 6, you can look at some of the output from step 5, or in the sample data folder which contains a sample of 77,000 tweets (geo and non-geolocated), and a pretty printed version of a few geolocated json records.

![Sample Tweets from Internet Archive Nov 1, 2022](tweet_map_nov_1_2022.png)
