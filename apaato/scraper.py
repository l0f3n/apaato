# scraper.py

import json
import re
import requests

# Import framework
from apaato.accommodation import Accommodation

ALL_ACCOMMODATIONS_URL = 'https://marknad.studentbostader.se/widgets/?pagination=0&paginationantal=100&callback=jQuery17109732211216157454_1492970171534&widgets%5B%5D=koerochprenumerationer%40STD&widgets%5B%5D=objektfilter%40lagenheter&widgets%5B%5D=objektsortering%40lagenheter&widgets%5B%5D=objektlista%40lagenheter&widgets%5B%5D=pagineringgonew%40lagenheter&widgets%5B%5D=pagineringlista%40lagenheter&widgets%5B%5D=pagineringgoold%40lagenheter&_=1492970171907'
SINGLE_ACCOMMODATION_URL = 'https://marknad.studentbostader.se/widgets/?refid={}&callback=&widgets[]=koerochprenumerationer@STD&widgets[]=objektinformation@lagenheter&widgets[]=objektforegaende&widgets[]=objektnasta&widgets[]=objektbilder&widgets[]=objektfritext&widgets[]=objektinformation@lagenheter&widgets[]=objektegenskaper&widgets[]=objektdokument&widgets[]=alert&widgets[]=objektintresse&widgets[]=objektintressestatus&widgets[]=objektkarta&_=1545230378811'


def fetch_all_accommodations():
    """ Yields all an accommodation object for every accommodation currently 
    available """

    response = requests.get(ALL_ACCOMMODATIONS_URL)
    accommodations_data = json.loads(response.text[response.text.find('{'):-2])["data"]["objektlista@lagenheter"]

    yield len(accommodations_data)

    for accommodation_data in accommodations_data:
        yield fetch_accommodation(accommodation_data)


def fetch_accommodation(accommodation_data: dict) -> dict:
    """ Gathers information about a single accommodation """

    # Store information about a single accommodation
    accommodation_properties = {
        "address": accommodation_data["adress"],
        "url": accommodation_data["detaljUrl"],
        "type": accommodation_data["typ"],
        "location": accommodation_data["omrade"],
        "rent": int(''.join(accommodation_data["hyra"].split())),
        "elevator": accommodation_data["hiss"],
        "size": float(accommodation_data["yta"]),
    }

    # Get text that has information about the queue
    response = requests.get(SINGLE_ACCOMMODATION_URL.format(accommodation_data["detaljUrl"][-64:]))
    accommodation_detailed_data = json.loads(response.text[1:-2])["html"]

    ##### QUEUE #####

    # Get text that contains all applicant queue points
    top_five_queue_points_text = accommodation_detailed_data["objektintressestatus"]

    # Create a RE that matches the numbers beginning with space
    queue_points_pattern = re.compile(r' ([\d ]+)')

    # Create a list of all the matches without leading space
    matches = queue_points_pattern.findall(top_five_queue_points_text)

    # The first match is the number of applicants
    number_of_applicants = int(matches.pop(0)) if len(matches) > 0 else 0

    # Remove whitespace and convert all matches to ints, right pad the list
    # with zeros to make it length 5.
    queue = [int(''.join(matches[i].split())) if i < number_of_applicants else 0 for i in range(5)]
    accommodation_properties['queue'] = queue

    ##### DEADLINE #####

    # Get text that has deadline
    deadline_text = accommodation_detailed_data["objektintresse"]

    # Create RE that matches date yyyy-mm-dd
    deadline_pattern = re.compile(r'\d\d\d\d-\d\d-\d\d')

    # Find deadline in text and add it accommodations_properties
    try:
        deadline = deadline_pattern.search(deadline_text).group()
    except AttributeError:
        # If date wasn't found, it means that it was an Accommodation Direct
        deadline = "9999-99-99"
    accommodation_properties["deadline"] = deadline

    return Accommodation(**accommodation_properties)
