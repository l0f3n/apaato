# scraper.py

# Import selenium to gather the refids for the accommodations
from selenium import webdriver

# Import requests to use studentbostaders API
import requests

# Import json to parse response from studentbostaders API
import json

# Import bs4 to parse html from studentbostaders API
from bs4 import BeautifulSoup as bs

# Import Generator for annotations
from typing import Generator

# Import re to find number of applcaints and queue points
import re

import os

# Import framework
from apaato.accommodation import Accommodation


API = 'https://marknad.studentbostader.se/widgets/?refid={}&callback=&widgets[]=koerochprenumerationer@STD&widgets[]=objektinformation@lagenheter&widgets[]=objektforegaende&widgets[]=objektnasta&widgets[]=objektbilder&widgets[]=objektfritext&widgets[]=objektinformation@lagenheter&widgets[]=objektegenskaper&widgets[]=objektdokument&widgets[]=alert&widgets[]=objektintresse&widgets[]=objektintressestatus&widgets[]=objektkarta&_=1545230378811'


# TODO: make this asynchronous
def fetch_all_accommodations():
    """ Goes to studentbostader.se and gathers the information about all the
    currently listed apartments """

    # Initialize headless driver
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(firefox_options=options,
            log_path=os.path.expanduser('~/Documents/apaato/geckodriver.log'),
            executable_path=os.path.expanduser('~/Documents/apaato/geckodriver'),)
    # Go to page with all apartments
    start_page = "https://www.studentbostader.se/en/find-apartments/search-apartments?pagination=0&paginationantal=10000"
    driver.get(start_page)

    # Find refids to all accommodations
    accommodations = driver.find_elements_by_class_name('noLinkcolor')[1:]
    accommodation_links = (a.get_attribute('href') for a in accommodations)
    refids = [link[link.index('=')+1:] for link in accommodation_links]

    # Yield total amount of accommodations
    yield len(refids)

    # Get information about every accommodation
    for refid in refids:
        yield fetch_accommodation(refid)

    driver.quit()


def fetch_accommodation(refid: str) -> dict:
    """ Gathers all information about an accommodation using its refid """

    # Store information about a single accommodation
    accommodation_properties = {}
    accommodation_properties['refid'] = refid

    # Use their API to get information about accommodation
    r = requests.get(API.format(refid))

    # Create dictionary
    dict_ = json.loads(r.text[1:-2])['html']


    #######################################
    ##### Queue points and applicants #####
    #######################################

    # Access text about queue points and number of applicants
    interest_status_text = dict_['objektintressestatus']

    # Pattern will match a dot followed by one or more spaces or digits
    # example: 1 230, 233, 73, 27
    queue_points_pattern = re.compile(r' ([\d ]+)')

    # Create a list of all the matches without leading space
    matches = queue_points_pattern.findall(interest_status_text)

    # The first match is the number of applicants
    number_of_applicants = matches.pop(0)
    accommodation_properties['applicants'] = number_of_applicants

    # Remove whitespace and convert all matches to ints, right pad the list
    # with zeros to make it length 5.
    queue_points_list = [int(matches[i].replace(' ', ''))
                         if i < len(matches) else 0 for i in range(5)]
    accommodation_properties['queue_points_list'] = queue_points_list


    ##############################################
    ##### Latest application acceptance date #####
    ##############################################

    # Access text about latest application acceptance date
    interest_text = dict_['objektintresse']

    # Create BeautifulSoup object
    soup = bs(interest_text, 'lxml')

    # Find latest application acceptance date
    date = soup.find('div', class_='IntresseMeddelande').text[25:35]
    accommodation_properties['date'] = date


    ############################
    ##### Address and size #####
    ############################

    # Access text about address, size, rent, etc.
    object_text = dict_['objektinformation@lagenheter']

    # Create BeautifulSoup object
    soup = bs(object_text, 'lxml')

    # Find address
    address = soup.find('dd', class_='ObjektAdress').text
    accommodation_properties['address'] = address

    # Find size
    size = soup.find('dd', class_='ObjektTyp').text
    accommodation_properties['size'] = size

    return Accommodation(**accommodation_properties)
