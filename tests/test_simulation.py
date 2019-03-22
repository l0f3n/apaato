# test_simulation.py

import unittest

import random
import math

# Insert parent directory to PATH in order to import accommodation
import sys
sys.path.insert(0, './apaato/')

import simulation
from accommodation import Accommodation


class TestSimulation(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """ Setup random seed """

        random.seed(420)

    def setUp(self):
        """ Set up some accommodations to use """

        self.accommodation1 = Accommodation(address=1,
                           queue_points_list=[500, 400, 300, 200, 100])
        self.accommodation2 = Accommodation(address=2,
                           queue_points_list=[600, 500, 400, 300, 200])
        self.accommodation3 = Accommodation(address=3,
                           queue_points_list=[700, 600, 500, 400, 300])
        self.accommodation4 = Accommodation(address=4,
                           queue_points_list=[800, 700, 600, 500, 400])
        self.accommodation5 = Accommodation(address=5,
                           queue_points_list=[500, 400, 300, 200, 100])
        self.accommodation6 = Accommodation(address=6,
                           queue_points_list=[0, 0, 0, 0, 0])

    def test_simulate(self):
        """ Tests simulation() function of simulation module """

        # The first person in every queue should get the accommodation
        accommodations = [self.accommodation1, self.accommodation2,
                          self.accommodation3, self.accommodation4]

        test_result = simulation.simulate(accommodations)

        correct_result = [(accommodations[0].address, 500),
                          (accommodations[1].address, 600),
                          (accommodations[2].address, 700),
                          (accommodations[3].address, 800)]

        self.assertEqual(test_result, correct_result)

        # The same person (500 points) is now first in two queues and should
        # get one of them at random (not with a set seed though).
        accommodations.append(self.accommodation5)

        test_result = simulation.simulate(accommodations)

        correct_result = [(accommodations[0].address, 500),
                          (accommodations[1].address, 600),
                          (accommodations[2].address, 700),
                          (accommodations[3].address, 800),
                          (accommodations[4].address, 400)]

        self.assertEqual(test_result, correct_result)

        # If we add an accommodation that no one gets it should not change the
        # result.
        accommodations.append(self.accommodation6)

        self.assertEqual(test_result, correct_result)

    def test_do_simulation(self):
        accommodations = [self.accommodation1, self.accommodation2,
                          self.accommodation3, self.accommodation4]

        for accommodation in accommodations:
            accommodation.insert_into_queue(750)

        combination = [self.accommodation1, self.accommodation2,
                       self.accommodation3]

        test_prob = simulation.do_simulations(accommodations, combination, 750)

        correct_prob = {1: 0.338, 2: 0.354, 3: 308}

        for test, correct in zip(test_prob, correct_prob):
            self.assertTrue(math.isclose(test, correct))


if __name__ == '__main__':
    unittest.main()
