# main.py

import os
import time
from datetime import datetime

# Import framework
import apaato.database as database
import apaato.scraper as scraper
import apaato.simulation as simulation
import apaato.text_formatter as text_formatter

acc_database = database.AccommodationDatabase()

def load_accommodations() -> None:
    """ Loads all accommodations from studentbostader.se into the database """

    acc_database.wipe()

    accommodations_gen = scraper.fetch_all_accommodations()
    total = next(accommodations_gen)

    start_time = time.time()

    for current, accommodation in enumerate(accommodations_gen):
        acc_database.insert_accommodation(accommodation)

        os.system('cls' if os.name == 'nt' else 'clear') # Windows / Unix
        print('{current} / {total}'.format(
            current=current+1,
            total=total))

    print('Finished in {time:.3f} seconds'.format(
        time=time.time() - start_time))


def list_accommodations(queue_points: int, show_link: bool = False) -> None:
    """ Prints out all accommodations in database sorted by the position a
    person with queue_points would be in the accommodation queues """

    # Finds the earliest latest application acceptance date
    earliest_date = min(datetime.strptime(accommodation.date, '%Y-%m-%d')
                        for accommodation
                        in acc_database.get_all_accommodations())

    # Only list the relevant accommodations
    date = earliest_date.strftime('%Y-%m-%d')
    accommodations = list(acc_database.get_accommodations_with_date(date))

    tf = text_formatter.AccommodationListing(accommodations, queue_points,
                                             show_link)
    tf.print()


def simulate(other_points: int, filter_: list = ['1 rum']) -> None:
    """ Runs simulation with other points and saves result in a database """

    # Make a set of all the different points that are in the queues
    unique_queue_points = set()
    for accommodation in list(acc_database.get_all_accommodations()):
        unique_queue_points.update(accommodation.queue_points_list)

    # Check that the queue_points are unique
    if other_points in unique_queue_points:
        print("Unable to simulate with '" + str(other_points) + "' points. " +
              "Points must be unique.")
        return

    # Finds the earliest latest application acceptance date
    earliest_date = min(datetime.strptime(accommodation.date, '%Y-%m-%d')
                        for accommodation
                        in acc_database.get_all_accommodations())

    # Only simulate with the apartments that have the earliest latest
    # application acceptance date
    date = earliest_date.strftime('%Y-%m-%d')
    accommodations = list(acc_database.get_accommodations_with_date(date))

    simulation_gen = simulation.run_simulation(other_points, accommodations,
                                               filter_)
    total = next(simulation_gen)

    # Store all results from simulation
    combinations = []

    start_time = time.time()

    for current, result in enumerate(simulation_gen):
        combinations.append(result)

        os.system('cls' if os.name == 'nt' else 'clear') # Windows / Unix
        print('{current} / {total}'.format(
            current=current+1,
            total=total))

    print('Finished in {time:.3f} seconds'.format(
        time=time.time() - start_time))

    return combinations


def list_probabilites(combinations):
    """ Print all combinations sorted by the chance of getting any of the
    accommodations in that combination """

    tf = text_formatter.CombintationListing(combinations)
    tf.print()

