# test_database.py

import unittest

import os
import sqlite3

# Insert parent directory to PATH in order to import accommodation
import sys
sys.path.insert(0, './apaato/')

import database
from accommodation import Accommodation


class TestDatabase(unittest.TestCase):
    """ Tests for the database module """

    @classmethod
    def setUpClass(cls):
        """ Creates the database """

        database.conn = sqlite3.connect(':memory:')
        database.c = database.conn.cursor()
        database.c.execute(""" CREATE TABLE IF NOT EXISTS accommodations (
                           address text,
                           refid text,
                           size text,
                           date text,
                           applicants integer,
                           first integer,
                           second integer,
                           third integer,
                           fourth integer,
                           fifth integer) """)


    def setUp(self):
        """ Setup a correct tuple and dict for comparison """

        self.correct_tuple = ('Testvägen', '4312431243214312', '1 rum',
                              '2019-01-21', 52, 530, 490, 241, 123, 43)

        self.correct_dict = {'address': 'Testvägen',
                             'refid': '4312431243214312',
                             'size': '1 rum',
                             'date': '2019-01-21',
                             'applicants': 52,
                             'queue_points_list': [530, 490, 241, 123, 43]}

    def test_wipe(self):
        """ Tests wipe() function in database module """

        database.wipe()

        with database.conn:
            database.c.execute('SELECT * FROM accommodations')

            # Database should be empty
            self.assertEqual(0, sum(1 for _ in database.c.fetchall()))

    def test_to_dict(self):
        """ Tests to_dict() function in database module """

        test_dict = database.to_dict(self.correct_tuple)
        self.assertEqual(test_dict, self.correct_dict)

    def test_to_accommodation(self):
        """ Tests to_accommodation() function in database module """

        test_accommodation = database.to_accommodation(self.correct_tuple)
        correct_accommodation = Accommodation(**self.correct_dict)

        # Creating an accommodation normally should result in the same
        # accommodation as creating one using data.to_accommodation.
        for key in test_accommodation.__dict__:
            self.assertEqual(test_accommodation.__dict__[key],
                             correct_accommodation.__dict__[key])

    def test_insert_accommodation(self):
        """ Tests insert_accommodation() function in database module """

        # Create an accommodation and insert into database
        accommodation = Accommodation(**self.correct_dict)
        database.insert_accommodation(accommodation)

        # Get newly created accommodation from database
        with database.conn:
            database.c.execute('SELECT * FROM accommodations')
            accommodations = [a for a in database.c.fetchall()]

        # Should only be one accommodation in the database
        self.assertEqual(len(accommodations), 1)

        # The result should be the same values we inserted earlier
        test_tuple = accommodations[0]
        self.assertEqual(test_tuple, self.correct_tuple)


if __name__ == '__main__':
    unittest.main()
