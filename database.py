# database.py

# Import sqlite3 to store accommodations in a database
import sqlite3

# Import generator for annotations
from typing import Generator

# Import framework
from accommodation import Accommodation


conn = sqlite3.connect('accommodations.db')
c = conn.cursor()
c.execute(""" CREATE TABLE IF NOT EXISTS accommodations (
                address text,
                link text,
                size text,
                date text,
                applicants integer,
                first integer,
                second integer,
                third integer,
                fourth integer,
                fifth integer) """)


def insert_accommodation(app: Accommodation) -> None:
    """ Inserts an Accommodation object into the database """

    accommodation_properties = {**app.__dict__, **(dict(zip(
                            ['first', 'second', 'third', 'fourth', 'fifth'],
                            app.queue_points_list)))}
    with conn:
        c.execute(""" INSERT INTO accommodations VALUES (:address,
                                                     :link,
                                                     :size,
                                                     :date,
                                                     :applicants,
                                                     :first,
                                                     :second,
                                                     :third,
                                                     :fourth,
                                                     :fifth) """,
                  accommodation_properties)


def all_accommodations() -> Generator[Accommodation, None, None]:
    """ Make search query in the database for all the elements and yields them
    as Accommodation objects """

    yield from query('SELECT * FROM accommodations')


def to_accommodation(accommodation_properties: tuple) -> Accommodation:
    """ Makes a new Accommodation object from tuple from sql query """

    return Accommodation(**to_dict(accommodation_properties))


def to_dict(accommodation_properties: tuple) -> dict:
    """ Takes tuple (from database) and zips it with the kwargs names of the
    Accommodation class """

    property_names = ['address', 'link', 'size', 'date', 'applicants']

    return {**dict(zip(property_names, accommodation_properties[:-5])),
            'queue_points_list': list(accommodation_properties[-5:])}


def query(query_text: str) -> Generator[Accommodation, None, None]:
    """ Takes a search query and yields all results as Accommodation objects """

    with conn:
        c.execute(query_text)
        yield from map(to_accommodation, c.fetchall())


def wipe() -> None:
    """ Wipes database """

    with conn:
        c.execute('DELETE FROM accommodations')
