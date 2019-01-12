# main.py

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
import time

# Import framework
import database
import scraper
import simulation
import text_formatter


def load_accommodations() -> None:
    """ Loads all accommodations from studentbostader.se into the database """

    database.wipe_database()

    accommodations_gen = scraper.fetch_all_accommodations()
    total = next(accommodations_gen)

    start_time = time.time()

    for current, accommodation in enumerate(accommodations_gen):
        database.insert_accommodation(accommodation)

        os.system('clear')
        print('{current} / {total}'.format(
            current=current+1,
            total=total))

    print('Finished in {time:.3f} seconds'.format(
        time=time.time() - start_time))


def list_accommodations(queue_points: int) -> None:
    """ Prints out all accommodations in database sorted by the position a
    person with queue_points would be in the accommodation queues """

    accommodations = list(database.all_accommodations_in_database())

    tf = text_formatter.AccommodationListing(accommodations,
                                             queue_points=queue_points)
    tf.print()


def simulate(other_points: int) -> None:
    """ Runs simulation with other points and saves result in database """

    unique = set()
    for accommodation in list(database.all_accommodations_in_database()):
        unique.update(accommodation.queue_points_list)

    if other_points in unique:
        print("Unable to simulate with '" + str(other_points) + "' points.")
        print("Points must be unique.")
        return

    simulation_gen = simulation.run_simulation(other_points)
    total = next(simulation_gen)

    global combintations
    combintations = []

    start_time = time.time()

    for current, result in simulation_gen:
        combintations.append(result)

        os.system('clear')
        print('{current} / {total}'.format(
            current=current,
            total=total))

    print('Finished in {time:.3f} seconds'.format(
        time=time.time() - start_time))


def list_probabilites():
    """ Print all combinations sorted by the chance of getting any of the
    accommodations in that combination """

    try:
        tf = text_formatter.CombintationListing(combintations)
        tf.print()
    except NameError:
        print("Please run 'simulate()' first.")
