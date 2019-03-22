# test_accommodation.py

import unittest

from apaato.accommodation import Accommodation


class TestAccommodation(unittest.TestCase):
    """ Tests for the accommodation module """

    def setUp(self):
        """ Creates accommodation """

        self.accommodation = Accommodation(queue_points_list=[2000, 1000, 200, 20, 2])

    def test_position_in_queue(self):
        """ Tests the position_in_queue() function of accommodation"""

        # First in queue
        self.assertEqual(self.accommodation.position_in_queue(2001), 1)

        # Last in queue
        self.assertEqual(self.accommodation.position_in_queue(3), 5)

        # Further than last in queue
        self.assertEqual(self.accommodation.position_in_queue(1), 6)

    def test_insert_into_queue(self):
        """ Tests the insert_into_queue() function of accommodation"""

        # First in queue
        self.accommodation.insert_into_queue(2001)

        # Last in queue
        self.accommodation.insert_into_queue(21)

        # Further than last in queue
        self.accommodation.insert_into_queue(20)

        self.assertEqual(self.accommodation.queue_points_list,
                         [2001, 2000, 1000, 200, 21])

if __name__ == '__main__':
    unittest.main()
