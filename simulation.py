# simulation.py

# Maybe simulate what happens if every person has a one percent chance of
# declining an offer

import random
import copy
import itertools
import operator as op
import functools

# Import framework
import database
from apartment import Apartment


def run_simulation(other_points: int) -> dict:
    """ Runs simulation for every combination of apartments that is desired """

    def total_chance(combination):
        """ Returns the total chance of getting any apartment at all from
        combination """

        return sum((apartment[1] for apartment in combination))

    def desired_apartments(apartments: list, other_points: int) -> filter:
        """ Returns a filter object of all apartments that the user wants to
        apply for """

        def apartment_filter(a: Apartment) -> bool:

            pos = a.position_in_queue(other_points)
            return pos not in [6]  # and a.size == '1 rum'

        return filter(apartment_filter, apartments)

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

            # If all apartments in an unnecessary combination is in current
            # combination then its unnecessary to run simulation
            for u_apartment in u_combination:
                if not u_apartment in current_combination:
                    break
                else:
                    return False

        return True

    # Load every apartment from database
    apartments = list(database.all_apartments_in_database())

    # Find all desired apartments
    possible_apartments = list(desired_apartments(apartments, other_points))

    # Calculate the amount of apartments that are to be applied for at a time
    count = min(len(possible_apartments), 5)

    # Calculates the total number of combinations
    yield sum([nck(len(possible_apartments), number)
               for number in range(1, count+1)])

    # Keeps track of all apartments that have a 100% or 0% chance.
    # Any simulation with these apartments in them is not necessary to run
    # because they will have the exact same chance (0%) or 100% (100%) whether
    # having that apartment in them or not
    u_combinations = []

    # Keeps track of which simulation is running
    current = 0

    for number in range(1, count+1):

        # Find all combinations of all desired apartments
        combinations = itertools.combinations(possible_apartments, number)

        # For every combination of apartments
        for current_combination in combinations:
            current += 1

            # If it is necessary to test this combination
            if not run_iteration():
                continue

            # Make a copy as to not modify the original
            apartments_copy = copy.deepcopy(apartments)

            # Enter queue of every apartment that is in current combination
            for desired_apartment in current_combination:
                for apartment in apartments_copy:
                    if desired_apartment.address == apartment.address:
                        apartment.insert_into_queue(other_points)
                        break

            # Run many simulations with current combination
            res = do_simulations(apartments_copy, current_combination,
                                 other_points)
            res = list(res.items())

            chance = total_chance(res)
            if chance == 0 or chance >= 1:
                u_combinations.append(current_combination)

            yield current, res


def do_simulations(apartments: list, combination: list,
                   other_points: int, n: int = 1000) -> dict:
    """ Runs simulation of apartments n number of times and returns a
    dictionary with {address, [(points, chance), ...]} that gives the chance
    for person with points to get the apartment at address """

    ret = {apartment.address: 0 for apartment in combination}

    # Run the simulation n times
    for _ in range(n):
        result = simulate(apartments)

        # For every person that got an apartment
        for address, points in result:

            # Only save my chances
            if points == other_points:
                ret[address] += 1/n
                break

    return ret


def simulate(apartments: list) -> list:
    """ Returns a list of tuples (address, points) which is a way that the
    apartments could be distributed between every person, points representing
    the person that got the apartment at address """

    result = []

    # Keep a list of indexes of apartments that are still available
    occupied_apartments = set()
    people_with_offers = set()

    # Go through every position
    for position in range(5):

        # Keep a dictionary with {points: [index, ...]} where the indexes
        # are the apartments that the person with points could get
        potential_apartments = {}

        # For every apartment
        for apartment_index, apartment in enumerate(apartments):

            # Get the points of the person that is at position in apartment
            points = apartment.queue_points_list[position]

            # If that person did not already get an offer and the apartment is
            # available
            if points not in people_with_offers and \
               apartment_index not in occupied_apartments:

                # Add the apartment to list of potential apartments for person
                # with points
                if points in potential_apartments:
                    potential_apartments[points] += [apartment_index]
                else:
                    potential_apartments[points] = [apartment_index]

        # For every person and the apartments they could get
        for points, potential_apartment in potential_apartments.items():

            # Choose one of the apartments randomly
            chosen_apartment_index = random.choice(potential_apartment)

            # Add apartments to not available apartments
            occupied_apartments.add(chosen_apartment_index)

            # The person cant get another apartment
            people_with_offers.add(points)

            # Save the person together with their apartment
            result.append((apartments[chosen_apartment_index].address, points))

    return result
