# database.py

import os
from pathlib import Path
import sqlite3
import sys
from typing import Generator

# Import framework
from apaato.accommodation import Accommodation

dir_name = os.path.expanduser('~/Documents/apaato')
file_name = "/accommodations_db.sqlite"

class AccommodationDatabase:

    def __init__(self, new_database: bool = False):

        if new_database:
            if Path(dir_name + file_name).is_file():
                os.remove(dir_name + file_name)
            elif not Path(dir_name).is_dir():
                os.mkdir(dir_name)
        else:
            if not Path(dir_name + file_name).is_file():
                print("No database found. Please run 'apaato load'.")
                sys.exit()

        self.conn = sqlite3.connect(dir_name + file_name)

        self.curs = self.conn.cursor()
        self.curs.execute(""" CREATE TABLE IF NOT EXISTS accommodations (
                          address text,
                          url text,
                          type text,
                          location text,
                          deadline text,
                          rent integer,
                          elevator text,
                          size integer,
                          first integer,
                          second integer,
                          third integer,
                          fourth integer,
                          fifth integer) """)
        if new_database:
            self.wipe()

    def insert_accommodation(self, acc: Accommodation) -> None:
        """ Inserts an Accommodation object into database """

        acc_prop = {**acc.__dict__,
                    **(dict(zip(
                    ['first', 'second', 'third', 'fourth', 'fifth'],
                    acc.queue)))}

        with self.conn:
            self.curs.execute(""" INSERT INTO accommodations VALUES (:address,
                                                             :url,
                                                             :type,
                                                             :location,
                                                             :deadline,
                                                             :rent,
                                                             :elevator,
                                                             :size,
                                                             :first,
                                                             :second,
                                                             :third,
                                                             :fourth,
                                                             :fifth) """,
                      acc_prop)


    def to_accommodation(self, accommodation_properties: tuple) -> Accommodation:
        """ Makes a new Accommodation object from tuple from sql query """

        return Accommodation(**self.to_dict(accommodation_properties))

    def to_dict(self, accommodation_properties: tuple) -> dict:
        """ Takes tuple (from database) and zips it with the kwargs names of the
        Accommodation class """

        property_names = ['address', 'url', 'type', 'location', 'deadline', 'rent', 'elevator']

        return {**dict(zip(property_names, accommodation_properties[:-5])),
                'queue': list(accommodation_properties[-5:])}

    def query(self, query_text: str) -> Generator[Accommodation, None, None]:
        """ Takes a search query and yields all results as Accommodation
        objects """

        with self.conn:
            self.curs.execute(query_text)
            yield from map(self.to_accommodation, self.curs.fetchall())

    def get_filtered_accommodations(self, **kwargs):
        search = "SELECT * FROM accommodations WHERE "
        for key, value in kwargs.items():
            if isinstance(value, list):
                search += "("
                for val in value:
                    search += f"{key} = '{val}' OR "
                search = search[:-4] + ") AND "
            elif value is not None:
                if key == 'rent':
                    search += f"{key} <= '{value}' AND "
                elif key == 'size':
                    search += f"{key} >= '{value}' AND "
                else:
                    search += f"{key} = '{value}' AND "

        if len(kwargs) > 0:
            search = search[:-5]
        else:
            search = search[:-7]

        yield from self.query(search)

    def get_all_accommodations(self):
        search = "SELECT * FROM accommodations"
        yield from self.query(search)

    def wipe(self) -> None:
        """ Wipes database """

        with self.conn:
            self.curs.execute('DELETE FROM accommodations')

