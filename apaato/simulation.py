# simulation.py

import random
import copy
import itertools
import operator as op
import functools
import math

# Import framework
import apaato.database
from apaato.accommodation import Accommodation


def run_simulation(other_points: int,
                   accommodations: list,
                   sizes: list = [],
                   areas: list = [],
                   n: int = 1000) -> dict:
    """ Runs simulation for every combination of accommodations that is
    desired """

    def total_chance(combination: list) -> float:
        """ Returns the total chance of getting any accommodation at all from
        combination """

        return sum((accommodation[1] for accommodation in combination))

    def filter_accommodations(accommodations: list,
                              other_points: int) -> filter:
        """ Returns a filter object of all accommodations that the user wants
        to apply for """

        def inner_filter(a: Accommodation) -> bool:

            desired_size = True if sizes == [] else a.size in sizes
            desired_area = True if areas == [] else a.area in areas

            return desired_size and desired_area

        return filter(inner_filter, accommodations)

    def nck(n: int, r: int) -> int:
        """ Used to calculate how many simulations are to be run """

        r = min(r, n-r)
        numer = functools.reduce(op.mul, range(n, n-r, -1), 1)
        denom = functools.reduce(op.mul, range(1, r+1), 1)
        return numer // denom

    def run_iteration() -> bool:
        """ Tests if it's necessary to simulate current combination """

        # For every unnecessary combination
        for u_combination in u_combinations:

            # If all accommodations in an unnecessary combination is in current
            # combination then its unnecessary to run simulation
            for u_accommodation in u_combination:
                if u_accommodation not in current_combination:
                    break
            else:
                return False

        return True

    # Find all desired accommodations
    possible_accommodations = list(filter_accommodations(accommodations,
                                                         other_points))

    # Calculate the amount of accommodations that are to be applied for at a
    # time
    count = min(len(possible_accommodations), 5)

    yield possible_accommodations

    yield sum([nck(len(possible_accommodations), number)
           for number in range(1, count+1)])

    # Keeps track of all accommodations that have a 100% or 0% chance.
    # Any simulation with these accommodations in them is not necessary to run
    # because they will have the exact same chance (0%) or 100% (100%) whether
    # having that accommodation in them or not
    u_combinations = []

    for number in range(1, count+1):

        # Find all combinations of all desired accommodations
        combinations = itertools.combinations(possible_accommodations, number)

        # For every combination of accommodations
        for current_combination in combinations:

            # If it is necessary to test this combination
            if not run_iteration():
                continue

            # Make a copy as to not modify the original
            accommodations_copy = copy.deepcopy(accommodations)

            # Enter queue of every accommodation that is in current combination
            for desired_accommodation in current_combination:
                for accommodation in accommodations_copy:
                    if desired_accommodation.address == accommodation.address:
                        accommodation.insert_into_queue(other_points)
                        break

            # Run many simulations with current combination
            res = list(do_simulations(accommodations_copy, current_combination,
                                      other_points, n).items())

            chance = total_chance(res)
            if chance == 0 or math.isclose(chance, 1):
                u_combinations.append(current_combination)

            yield res


def do_simulations(accommodations: list, combination: list,
                   other_points: int, n: int) -> dict:
    """ Runs simulation of accommodations n number of times and returns a
    dictionary with {address, [(points, chance), ...]} that gives the chance
    for person with points to get the accommodation at address """

    ret = {accommodation.address: 0 for accommodation in combination}

    # Run the simulation n times
    for _ in range(n):
        result = simulate(accommodations)

        # For every person that got an accommodation
        for address, points in result:

            # Only save my chances
            if points == other_points:
                ret[address] += 1/n
                break

    return ret


def simulate(accommodations: list) -> list:
    """ Returns a list of tuples (address, points) which is a way that the
    accommodations could be distributed between every person, points
    representing the person that got the accommodation at address """

    result = []

    # Keep a list of indexes of accommodations that are still available
    occupied_accommodations = set()
    people_with_offers = set()

    # Go through every position
    for position in range(5):

        # Keep a dictionary with {points: [index, ...]} where the indexes
        # are the accommodations that the person with points could get
        potential_accommodations = {}

        # For every accommodation
        for accommodation_index, accommodation in enumerate(accommodations):

            # Get the points of the person that is at position in accommodation
            points = accommodation.queue_points_list[position]

            # If that person did not already get an offer and the accommodation
            # is available
            if points not in people_with_offers and \
               accommodation_index not in occupied_accommodations:

                # Add the accommodation to list of potential accommodations for
                # person with points
                if points in potential_accommodations:
                    potential_accommodations[points] += [accommodation_index]
                else:
                    potential_accommodations[points] = [accommodation_index]

        # For every person and the accommodations they could get
        for points, accommodation in potential_accommodations.items():

            # Choose one of the accommodations randomly
            chosen_accommodation_index = random.choice(accommodation)

            # Add accommodations to not available accommodations
            occupied_accommodations.add(chosen_accommodation_index)

            # The person cant get another accommodation
            people_with_offers.add(points)

            # Save the person together with their accommodation
            result.append((accommodations[chosen_accommodation_index].address,
                           points))

    return result
