# scraper.py

import json
import re
import requests

from typing import Dict, Generator

from apaato.accommodation import Accommodation


ALL_ACCOMMODATIONS_URL = 'https://marknad.studentbostader.se/widgets/?pagination=0&paginationantal=1000&callback=jQuery17109732211216157454_1492970171534&widgets%5B%5D=koerochprenumerationer%40STD&widgets%5B%5D=objektfilter%40lagenheter&widgets%5B%5D=objektsortering%40lagenheter&widgets%5B%5D=objektlista%40lagenheter&widgets%5B%5D=pagineringgonew%40lagenheter&widgets%5B%5D=pagineringlista%40lagenheter&widgets%5B%5D=pagineringgoold%40lagenheter&_=1492970171907'
SINGLE_ACCOMMODATION_URL = 'https://marknad.studentbostader.se/widgets/?refid={}&callback=&widgets[]=koerochprenumerationer@STD&widgets[]=objektinformation@lagenheter&widgets[]=objektforegaende&widgets[]=objektnasta&widgets[]=objektbilder&widgets[]=objektfritext&widgets[]=objektinformation@lagenheter&widgets[]=objektegenskaper&widgets[]=objektdokument&widgets[]=alert&widgets[]=objektintresse&widgets[]=objektintressestatus&widgets[]=objektkarta&_=1545230378811'


class AccommodationsFetcher:

    def __init__(self) -> None:
        response = requests.get(ALL_ACCOMMODATIONS_URL)
        self._accommodations_data = json.loads(response.text[response.text.find('{'):-2])["data"]["objektlista@lagenheter"]

        self._len = len(self._accommodations_data)

    def __len__(self) -> int:
        return self._len

    def __iter__(self) -> Generator[Accommodation, None, None]:
        for accommodation_data in self._accommodations_data:
            yield self.fetch_accommodation(accommodation_data)

    def fetch_accommodation(
            self, 
            accommodation_data: Dict[str, str]) -> Accommodation:
        """ Gathers information about a single accommodation """

        accommodation_properties = {
            "address": accommodation_data["adress"],
            "url": accommodation_data["detaljUrl"],
            "type": accommodation_data["typ"],
            "location": accommodation_data["omrade"],
            "rent": int(''.join(accommodation_data["hyra"].split())),
            "elevator": accommodation_data["hiss"],
            "size": float(accommodation_data["yta"]),
        }

        try:
            accommodation_properties["floor"] = int(accommodation_data["vaning"])
        except ValueError:
            floor_pattern = re.compile(r"\.\d")
            floor = floor_pattern.search(accommodation_properties["address"]).group()[1:]  # type: ignore
            accommodation_properties["floor"] = floor

        response = requests.get(SINGLE_ACCOMMODATION_URL.format(accommodation_data["detaljUrl"][-64:]))
        accommodation_detailed_data = json.loads(response.text[1:-2])["html"]

        top_five_queue_points_text = accommodation_detailed_data["objektintressestatus"]
        queue_points_pattern = re.compile(r' ([\d ]+)')
        matches = queue_points_pattern.findall(top_five_queue_points_text)
        num_visible_queue_points = max(len(matches) - 1, 0)

        # Convert queue_points to integers, right pad the list with zeros 
        # to make it length 5. First match is # of applicants so i -> i+1.
        queue = [int(''.join(matches[i+1].split())) if i < num_visible_queue_points else 0 for i in range(5)]
        accommodation_properties['queue'] = queue

        deadline_text = accommodation_detailed_data["objektintresse"]
        deadline_pattern = re.compile(r'\d\d\d\d-\d\d-\d\d')

        try:
            deadline = deadline_pattern.search(deadline_text).group()  # type: ignore
        except AttributeError:  # Accommodation Direct has no deadline
            deadline = "9999-99-99"  # Placeholder for Accommodation Direct

        accommodation_properties["deadline"] = deadline

        return Accommodation(**accommodation_properties)
