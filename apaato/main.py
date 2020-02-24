# main.py

#               command_line_interface.py
#                          |
#                        main.py
#                          |
#     +------------+-------+---------+----------------+
#     |            |                 |                |
# scraper.py   database.py       printer.py      simulator.py
#     |            |                 |                |
#     +------------+-------+---------+----------------+
#                          |
#                     accommodation.py


import os
import sys
import time
from datetime import datetime
from typing import List, Tuple

# Import framework
import apaato.database as database
import apaato.scraper as scraper
import apaato.simulator as simulator
import apaato.printer as printer

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
        acc_database.insert_accommodation(accommodation) # type: ignore

        printer.print_progress_bar(current/total) # type: ignore

    print(f'\nFinished in {time.time() - start_time:.1f} seconds')


def list_accommodations(**kwargs) -> None:
    """ Prints out all accommodations in database sorted by the position a
    person with queue_points would be in the accommodation queues """

    acc_database = database.AccommodationDatabase()

    deadlines = sorted(set(accommodation.deadline for accommodation in acc_database.get_all_accommodations()))

    for deadline in deadlines:
        print(f"[Deadline: {deadline if deadline != '9999-99-99' else 'Accommodation Direct'}]")
        accommodations = acc_database.get_filtered_accommodations(deadline=deadline)
        printer.print_accommodations(accommodations, address=True, **kwargs)


def simulate(other_points: int, **kwargs) -> List[Tuple[str, float]]:
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
    deadline = min(accommodation.deadline for accommodation in acc_database.get_all_accommodations())

    # Only simulate with the apartments that have the earliest deadline
    accommodations = list(acc_database.get_filtered_accommodations(deadline=deadline))

    accommodations_to_apply_for = list(acc_database.get_filtered_accommodations(deadline=deadline, **kwargs))

    if len(accommodations_to_apply_for) == 0:
        print("No accommodation matched the critera.")
        sys.exit(-1)

    simulation_gen = simulator.run_simulation(other_points,
                                               accommodations,
                                               accommodations_to_apply_for,
                                            )

    print(f'{len(accommodations_to_apply_for)} accommodations matched the criteria...')

    total_combinations = next(simulation_gen)  # type: ignore

    # Store all results from simulation
    combinations = []

    start_time = time.time()

    for current, result in enumerate(simulation_gen, start=1):
        combinations.append(result)

        printer.print_progress_bar(current/total_combinations)

    printer.print_progress_bar(1)

    print(f'\nFinished in {time.time() - start_time:.1} seconds')

    return combinations


def list_probabilites(combinations):
    """ Print all combinations sorted by the chance of getting any of the
    accommodations in that combination """

    tf = printer.CombintationListing(combinations)
    tf.print()
