#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import packages
import time
start = time.time()
import os
from bs4 import BeautifulSoup as bs
import logging

# Import scripts
import constants
import bis_scraper
import utils

# Working directory to save files and log path
path_data = '../../data/'
path_log = '../../logs/'
path_scrape = path_data + '0_raw'

# Create directories if doesn't exist
if not os.path.exists(path_data):
    os.makedirs(path_data)

if not os.path.exists(path_log):
    os.makedirs(path_log)

if not os.path.exists(path_scrape):
    os.makedirs(path_scrape)

# Creating a log file
logging.basicConfig(filename=path_log+'logging_bis_scraper.log',
        level=logging.ERROR)

# Create datelist
date_list = utils.date_list()

# Create list of institutions.
institutions = constants.institutions

# Call scrape_bis
bis_scraper.bis_scraper(path_scrape, institutions, date_list)

# Shut down logging so that logging files close etc.
logging.shutdown()

# Print elapsed time
end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("Elapsed time: " + "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),
    int(minutes), seconds))
