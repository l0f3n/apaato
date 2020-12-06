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


import logging
import sys

from typing import Any, Dict, List, Tuple

import apaato.database  as database
import apaato.scraper   as scraper
import apaato.simulator as simulator
import apaato.printer   as printer

# ==== Setup logging ====
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] %(levelname)s:%(name)s: %(message)s')

file_handler = logging.FileHandler('apaato.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
# ==== Setup logging ====


@printer.timer(prefix='\nFinished in ')
def load_accommodations() -> None:
    """ Loads all accommodations from studentbostader.se into the database """

    logger.info("Loading studentbostader.se.")
    print('Loading studentbostader.se... ', end = '', flush=True)

    accommodations = scraper.AccommodationsFetcher()
    accommodations_len = len(accommodations)

    print(f'found {accommodations_len} accommodations.')

    print('Fetching properties of each accommodation... ')

    acc_database = database.AccommodationDatabase(new_database=True)

    for current, accommodation in enumerate(accommodations, start=1):
        acc_database.insert_accommodation(accommodation)

        printer.print_progress_bar(current/accommodations_len)


def list_accommodations(
        display: Dict[str, bool], 
        filter_: Dict[str, Any]) -> None:
    """ Prints out all accommodations in database sorted by the position a
    person with queue_points would be in the accommodation queues """

    acc_database = database.AccommodationDatabase()

    deadlines = sorted(set(accommodation.deadline for accommodation in acc_database.get_all_accommodations()))

    logger.debug("Found deadlines: " + ', '.join([deadline if deadline != '9999-99-99' else 'Accommodation Direct' for deadline in deadlines]))

    for deadline in deadlines:
        filter_['deadline'] = deadline
        accommodations = list(acc_database.get_filtered_accommodations(filter_))
        logger.info(f"Found {len(accommodations)} accommodations with deadline {deadline}.")
        
        if len(accommodations) > 0:
            print(f"[Deadline: {deadline if deadline != '9999-99-99' else 'Accommodation Direct'}]")
            printer.print_accommodations(accommodations, display)

@printer.timer(prefix='\nFinished in ')
def simulate(
        other_points: int, 
        filter_: Dict[str, Any]) -> List[Tuple[str, float]]:
    """ Runs simulation with other points and saves result in a database """

    acc_database = database.AccommodationDatabase()

    # Make a set of all the different points that are in the queues
    unique_queue_points = set()
    for accommodation in list(acc_database.get_all_accommodations()):
        unique_queue_points.update(accommodation.queue)

    # Check that the queue_points are unique
    if other_points in unique_queue_points:
        logger.error(f"Unable to calculate probabilities with non-unique {other_points} queue points. Exiting.")
        sys.exit(-1)

    # Finds the earliest latest application acceptance date
    deadline = min(accommodation.deadline for accommodation in acc_database.get_all_accommodations())
    deadline_filter = {'deadline' : deadline}

    logger.info(f"Earliest deadline is {deadline}.")

    # Use only the apartments that have the earliest deadline
    accommodations = list(acc_database.get_filtered_accommodations(deadline_filter))

    logger.info(f"Found {len(accommodations)} accommodations with deadline {deadline}.")

    # Only apply for accommodations that match the user specified filter
    filter_.update(deadline_filter)
    accommodations_to_apply_for = list(acc_database.get_filtered_accommodations(filter_))

    if len(accommodations_to_apply_for) == 0:
        logger.error("No accommodation matched the critera. Exiting.")
        sys.exit(-1)

    accommodations_simulator = simulator.Simulator(
                                    other_points,
                                    accommodations,
                                    accommodations_to_apply_for,
                                )

    logger.info(f'There are {len(accommodations_to_apply_for)} accommodations that matches the desired criteria.')
    print(f'{len(accommodations_to_apply_for)} accommodations matched the criteria.')

    desired_accommodations_count = len(accommodations_simulator)

    # Store probabilities of getting an apartment
    probabilities: List[Tuple[str, float]] = []

    for current, result in enumerate(accommodations_simulator, start=1):
        probabilities.append(result)
        printer.print_progress_bar(current/desired_accommodations_count)

    return probabilities


def list_probabilites(probabilities: List[Tuple[str, float]]):
    """ Print probabilities of getting an accommodation """

    print("These are the estimated probabilities of getting an accommodation:")
    printer.print_probabilities(probabilities)
