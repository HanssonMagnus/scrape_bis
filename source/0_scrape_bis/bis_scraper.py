# Import packages
import os
import logging
import string
import io
import requests
from bs4 import BeautifulSoup as bs

# Import scripts
import constants

def bis_scraper(wd, institutions, date_list):
    '''
    Args:
        wd: string
        intitutions: list of strings
        date_list: list of dates in format 210101
    '''
    # Create list of the alphabet
    letters = list(string.ascii_lowercase)

    # Define url from where to get text data
    url = "https://www.bis.org/review/r"
    end_pdf = ".pdf"
    end_htm = ".htm"

    for date in date_list:
        for inc in letters:

            response = requests.get(url + date + inc + end_htm)

            if response.status_code == 200:
                try:
                    # Creating a Beautiful Soup object with appropriate parser.
                    soup = bs(response.content, 'html.parser')

                    # Retrieve author data
                    extratitle = soup.find(id='extratitle-div')

                    # Create a string with meta data
                    meta = extratitle.text
                    meta = meta.strip()# remove white space

                    # Match institution with meta data
                    inst = []
                    for item in institutions:
                        if item.lower() in meta.lower(): # case insensitive
                            inst.append(item.lower()) # append all matching inst.

                    # If one institution was in the list proceed further
                    if len(inst) == 1:
                        inst = inst[0]

                    # If multiple institutions were in the extra title, choose
                    # the one that comes first in the meta information
                    elif len(inst) > 1:
                        index_list = []
                        for i in inst:
                            index_list.append(meta.lower().find(i))
                        min_value = min(index_list)
                        inst = inst[index_list.index(min_value)]

                    # Correct some institution names, because they are written
                    # wrong on the BIS website for some (all lower case here)
                    # us
                    if inst in constants.inst_us:
                        inst = constants.inst_us[0]
                    # norway
                    if inst == "norges bank":
                        inst = "central bank of norway"
                    # france
                    if inst == "banque de france":
                        inst = "bank of france"
                    # sweden
                    if inst in constants.inst_swe:
                        inst = "sveriges riksbank"
                    # netherlands
                    if inst == "nederlandsche bank":
                        inst = "netherlands bank"
                    # austria
                    if inst in constants.inst_austria:
                        inst = "central bank of the republic of austria"
                    # south africa
                    if inst == "bank of south africa":
                        inst = "south african reserve bank"
                    # hong kong
                    if inst == "hong kong monetary":
                        inst = "hong kong monetary authority"
                    # india
                    if inst == "bank of india":
                        inst = "reserve bank of india"
                    # macedonia
                    if inst == "national bank of the republic of macedonia" or inst == "national bank of the republic of north macedonia":
                        inst = "national bank of north macedonia"
                    # european cental bank
                    if inst == "ecb":
                        inst = "european central bank"
                    # ireland
                    if inst == "authority of ireland":
                        inst = "central bank of ireland"
                    # turkey
                    if inst == "bank of turkey":
                        inst = "central bank of the republic of turkey"
                    # china
                    if inst == "bank of china":
                        inst = "people's bank of china"
                    # austrailia
                    if inst == "australian reserve bank" or inst == "bank of australia":
                        inst = "reserve bank of australia"

                    file_meta = os.path.join(wd, inst, inst + "_meta.txt")

                    if not os.path.exists(os.path.dirname(file_meta)):
                        os.makedirs(os.path.dirname(file_meta))

                    # use "a" instaed of "w" to append
                    with io.open(file_meta, "a", encoding="utf-8") as f:
                        f.write(inc + date + ": " + meta + "\n")

                    response_pdf = requests.get(url + date + inc + end_pdf)

                    file_speech = os.path.join(wd, inst, inc + date + "_speech.pdf")

                    # Create list of institutions.
                    with open(file_speech, "wb") as f:
                            f.write(response_pdf.content)

                except:
                    print("Error scraping: " + url + date + inc + end_htm)
                    logging.error("Error scraping: " + url + date + inc + end_htm)

            # Break inner loop if no more speeches for that day
            elif response.status_code == 404:
                break

