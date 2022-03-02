#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 07:44:55 2020
@author: magnus

Converting a folder structure of .pdf to a structure of .txt. This takes the
given structure that the scraper yielded and returns the same structure but
with .txt files.
"""

# import packages
import time
start = time.time()
import logging
import os
import glob
import textract
import datetime as dt

# Paths
path_data = '../../data/'
path_log = '../../logs/'
path_scrape = path_data + '0_raw'

# Working directory to load files
wd_in = path_data + '0_raw'

# Working directory to save files
wd_out = path_data + '1_raw_txt'
if not os.path.exists(wd_out):
    os.makedirs(wd_out)

# Creating a log file
logging.basicConfig(filename=path_log+'logging_pdf_to_txt.log',
        level=logging.ERROR)

folders = os.listdir(wd_in)

for folder in folders:
    path_folder = os.path.join(wd_in, folder)
    files = [file for file in glob.glob(path_folder + "/*.pdf")]
    for file in files:

        try:
            # Extract text from pdf
            text = textract.process(file) # type bytes
            text = text.decode('utf-8') # decode to type str

            # Create new file name
            file_name = os.path.basename(file)
            file_name = file_name.replace("_speech.pdf", "")
            order = file_name[0]
            date = file_name[1:] # in format "%y%m%d"
            date = dt.datetime.strptime(date, "%y%m%d") # datetime object
            date = dt.datetime.strftime(date, "%Y-%m-%d") # convert to "%Y-%m-%d"

            # Save list of strings to file
            path_file_out = os.path.join(wd_out, folder, date + "_" + order + ".txt")

            if not os.path.exists(os.path.dirname(path_file_out)):
                os.makedirs(os.path.dirname(path_file_out))

            with open(path_file_out, 'w') as f:
                f.write(text)

            f.close()

        except Exception as e:
            print("Error converting file: " + file)
            print(e.args)
            logging.error("Error converting file: " + file, exc_info=True)

logging.shutdown()

# Print elapsed time
end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("Elapsed time: " + "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),
    int(minutes), seconds))
