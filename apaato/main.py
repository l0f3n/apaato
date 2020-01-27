# main.py

#               command_line_interface.py
#                          |
#                        main.py
#                          |
#     +------------+-------+---------+----------------+
#     |            |                 |                |
# scraper.py   database.py   text_formatter.py   simulation.py
#     |            |                 |                |
#     +------------+-------+---------+----------------+
#                          |
#                     accommodation.py


import os
import sys
import time
from datetime import datetime

# Import framework
import apaato.database as database
import apaato.scraper as scraper
import apaato.simulation as simulation
import apaato.text_formatter as text_formatter

def load_accommodations() -> None:
    """ Loads all accommodations from studentbostader.se into the database """

    print('Loading studentbostader.se... ', end = '', flush=True)

    start_time = time.time()

    acc_database = database.AccommodationDatabase(new_database=True)

    accommodations_gen = scraper.fetch_all_accommodations()
    total = next(accommodations_gen)

    print(f'found {total} accommodations.')

    print('Fetching data about each accommodation... ')

    for current, accommodation in enumerate(accommodations_gen, start=1):
        acc_database.insert_accommodation(accommodation)

        text_formatter.print_progress_bar(current/total)

    print(f'\nFinished in {time.time() - start_time:.3f} seconds')


def list_accommodations(show_link: bool = False,
                        show_type: bool = False,
                        show_location: bool = False,) -> None:
    """ Prints out all accommodations in database sorted by the position a
    person with queue_points would be in the accommodation queues """

    acc_database = database.AccommodationDatabase()

    deadlines = sorted(set(accommodation.deadline for accommodation in acc_database.get_all_accommodations()))

    for deadline in deadlines:
        print(f"Deadline: {deadline}")
        tf = text_formatter.AccommodationListing(acc_database.get_accommodations_with_deadline(deadline),
                                                 show_link,
                                                 show_type,
                                                 show_location,)
        tf.print()


def simulate(other_points: int,
             types: list = [],
             locations: list = [], ) -> None:
    """ Runs simulation with other points and saves result in a database """

    acc_database = database.AccommodationDatabase()

    # Make a set of all the different points that are in the queues
    unique_queue_points = set()
    for accommodation in list(acc_database.get_all_accommodations()):
        unique_queue_points.update(accommodation.queue)

    # Check that the queue_points are unique
    if other_points in unique_queue_points:
        print(f"Unable to simulate with {other_points} points. Points must be unique.")
        sys.exit(-1)

    # Finds the earliest latest application acceptance date
    earliest_deadline = min(accommodation.deadline for accommodation in acc_database.get_all_accommodations())

    # Only simulate with the apartments that have the earliest latest
    # application acceptance date
    accommodations = list(acc_database.get_accommodations_with_deadline(earliest_deadline))

    simulation_gen = simulation.run_simulation(other_points,
                                               accommodations,
                                               types,
                                               locations, )

    desired_accommodations = next(simulation_gen)

    if len(desired_accommodations) == 0:
        print("No accommodation matched the specified critera.")
        sys.exit(-1)

    print(f'Running simulation with {len(desired_accommodations)} accommodations...')

    total_combinations = next(simulation_gen)

    # Store all results from simulation
    combinations = []

    start_time = time.time()

    for current, result in enumerate(simulation_gen, start=1):
        combinations.append(result)

        text_formatter.print_progress_bar(current/total_combinations)

    text_formatter.print_progress_bar(1)

    print(f'\nFinished in {time.time() - start_time:.3} seconds')

    return combinations


def list_probabilites(combinations):
    """ Print all combinations sorted by the chance of getting any of the
    accommodations in that combination """

    tf = text_formatter.CombintationListing(combinations)
    tf.print()
