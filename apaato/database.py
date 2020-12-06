# database.py

import logging
import sqlite3
import sys

from pathlib import Path
from typing import Any, Dict, Generator, Tuple

from apaato.accommodation import Accommodation


# ==== Setup logging ====
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(u'[%(asctime)s] %(levelname)s:%(name)s: %(message)s')

file_handler = logging.FileHandler('apaato.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
# ==== Setup logging ====


DATABASE_FILE_PATH = Path(__file__).parent / "accommodations.db"


class AccommodationDatabase:

    def __init__(self, new_database: bool = False) -> None:

        if new_database:
            logger.debug("Removing old database (if there is one).")
            DATABASE_FILE_PATH.unlink(missing_ok=True)
        elif not DATABASE_FILE_PATH.is_file():
            logger.error("No database found. Exiting.")
            sys.exit()

        self.conn = sqlite3.connect(DATABASE_FILE_PATH)

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
                          floor integer,
                          first integer,
                          second integer,
                          third integer,
                          fourth integer,
                          fifth integer) """)

        # TODO: Remove this. We always delete the database if we want to create
        # a new one, so the only things this will do is wiping an already empty
        # database. 
        if new_database:
            self.wipe()

    def insert_accommodation(self, acc: Accommodation) -> None:
        """ Inserts an Accommodation object into database """

        logger.info(f"Adding '{acc.address}' to database.")

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
                                                             :floor,
                                                             :first,
                                                             :second,
                                                             :third,
                                                             :fourth,
                                                             :fifth) """,
                      acc_prop)


    def to_accommodation(self, accommodation_properties: Tuple[Any, ...]) -> Accommodation:
        """ Makes a new Accommodation object from tuple from sql query """

        return Accommodation(**self.to_dict(accommodation_properties))

    def to_dict(self, accommodation_properties: Tuple[Any, ...]) -> Dict[str, Any]:
        """ Takes tuple (from database) and zips it with the kwargs names of the
        Accommodation class """

        property_names = [
            'address', 
            'url', 
            'type', 
            'location', 
            'deadline', 
            'rent', 
            'elevator', 
            'size',
            'floor',
        ]

        return {**dict(zip(property_names, accommodation_properties[:-5])),
                'queue': list(accommodation_properties[-5:])}

    def query(self, query_text: str) -> Generator[Accommodation, None, None]:
        """ Takes a search query and yields all results as Accommodation
        objects """

        logger.info(f"Querying database.")

        with self.conn:
            self.curs.execute(query_text)
            yield from map(self.to_accommodation, self.curs.fetchall())

    def get_filtered_accommodations(self, filter_: Dict[str, Any]) -> Generator[Accommodation, None, None]:
        
        search = "SELECT * FROM accommodations WHERE "
        for key, value in filter_.items():
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

        if len(filter_) > 0:
            search = search[:-5]
        else:
            search = search[:-7]

        yield from self.query(search)

    def get_all_accommodations(self) -> Generator[Accommodation, None, None]:

        search = "SELECT * FROM accommodations"
        yield from self.query(search)

    def wipe(self) -> None:

        logger.info(f"Wiping database.")

        with self.conn:
            self.curs.execute('DELETE FROM accommodations')

