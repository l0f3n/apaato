# simulation.py

import copy
import random

# Import framework
import apaato.database
from apaato.accommodation import Accommodation


NUM_SIMULATIONS = 1000

class Simulator:

    def __init__(
            self,
            other_points: int,
            accommodations: list,
            accommodations_to_apply_for: list):
    
        self.other_points = other_points
        self.accommodations = accommodations
        self.accommodations_to_apply_for = accommodations_to_apply_for

    def __len__(self): 
        return len(self.accommodations_to_apply_for)
        
    def __iter__(self):
        for desired_accommodation in self.accommodations_to_apply_for:

            # Make a copy as to not modify the original
            accommodations_copy = copy.deepcopy(self.accommodations)

            # Store current address
            current_address = desired_accommodation.address

            # Enter queue of the current desired accommodation 
            for accommodation in accommodations_copy:
                if current_address == accommodation.address:
                    accommodation.insert_into_queue(self.other_points)
                    break

            result = do_many_simulations(accommodations_copy)

            # Tuple containing address and probability of getting it 
            #   ('Rydsvägen 248 A.36': 1)
            yield (current_address, 
                result[self.other_points][current_address] if self.other_points in result else 0)


def do_many_simulations(accommodations: list) -> dict:
    """ Do many simulations of who would get the given accommodations """

    #ret = {accommodation.address: 0 for accommodation in combination}

    # Dictionary with points mapping to probabilities of gettings apartments
    # {
    #   '1000': { 'Rydsvägen 252 C.17': 0.1, 'Alsättersgatan 9 B.25': 0.5, ... }
    #                               .
    #                               .
    # }
    result = {}

    for _ in range(NUM_SIMULATIONS):
        one_result = do_one_simulation(accommodations)

        for address, points in one_result:
            
            # TODO: Use defaultdict instead for the two following snippets
            if points not in result:
                result[points] = {}

            if address not in result[points]:
                result[points][address] = 0

            result[points][address] += 1/NUM_SIMULATIONS

    return result


def do_one_simulation(accommodations: list) -> list:
    """ Uses the accommodations to simulate who would get them. """

    # Keeps track of the result in the format address, points (who got the accommodation)
    # [
    #   (Rydsvägen 262 A.12, 1050)
    #               .
    #               .
    # ]
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
            points = accommodation.queue[position]

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
