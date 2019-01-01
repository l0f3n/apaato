# database.py

# Import sqlite3 to store apartments in a database
import sqlite3

# Import generator for annoatations
from typing import Generator

# Import framework
from apartment import Apartment


conn = sqlite3.connect('apartments.db')
c = conn.cursor()
c.execute(""" CREATE TABLE IF NOT EXISTS apartments (
                address text,
                link text,
                size text,
                applicants integer,
                first integer,
                second integer,
                third integer,
                fourth integer,
                fifth integer) """)


def insert_apartment(app: Apartment) -> None:
    """ Inserts an Apartment object into the database """

    apartment_properties = {**app.__dict__, **(dict(zip(
                            ['first', 'second', 'third', 'fourth', 'fitfh'],
                            app.queue_points_list)))}
    with conn:
        c.execute(""" INSERT INTO apartments VALUES (:address,
                                                     :link,
                                                     :size,
                                                     :applicants,
                                                     :first,
                                                     :second,
                                                     :third,
                                                     :fourth,
                                                     :fitfh) """,
                  apartment_properties)


def all_apartments_in_database() -> Generator[Apartment, None, None]:
    """ Make search query in the database for all the elements and yields them
    as actual Apartment objects """

    with conn:
        c.execute('SELECT * FROM apartments')
        yield from map(to_apartment, c.fetchall())


def to_apartment(apartment_properties: tuple) -> Apartment:
    """ Makes a new Apartment object from tuple from sql query """

    return Apartment(**to_dict(apartment_properties))


def to_dict(apartment_properties: tuple) -> dict:
    """ Takes tuple (from database) and zips it with the kwarg names of the
    Apartment class """

    property_names = ['address', 'link', 'size', 'applicants']

    return {**dict(zip(property_names, apartment_properties[:-5])),
            'queue_points_list': list(apartment_properties[-5:])}


def wipe_database() -> None:
    """ Wipes database """

    with conn:
        c.execute('DELETE FROM apartments')
