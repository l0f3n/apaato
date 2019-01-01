# main.py

#                        main.py
#                          |
#     +------------+-------+---------+----------------+
#     |            |                 |                |
# scraper.py   database.py   text_formatter.py   simulation.py
#     |            |                 |                |
#     +------------+-------+---------+----------------+
#                          |
#                     apartment.py

import os
import time

# Import framework
import database
import scraper
import simulation
import text_formatter


def load_apartments() -> None:
    """ Loads all apartments from studentbostader.se into the database """

    database.wipe_database()

    apartments_gen = scraper.fetch_all_apartments()
    total = next(apartments_gen)

    start_time = time.time()

    for current, apartment in enumerate(apartments_gen):
        database.insert_apartment(apartment)

        os.system('clear')
        print('{current} / {total}'.format(
            current=current+1,
            total=total))

    print('Finished in {time:.3f} seconds'.format(
        time=time.time() - start_time))


def list_apartments(queue_points: int) -> None:
    """ Prints out all apartments in database sorted by the position a person
    with queue_points would be in the apartment queues """

    apartments = list(database.all_apartments_in_database())

    tf = text_formatter.ApartmentListing(apartments, queue_points=queue_points)
    tf.print()


def simulate(other_points: int) -> None:
    """ Runs simulation with other points and saves result in database """

    unique = set()
    for apartment in list(database.all_apartments_in_database()):
        unique.update(apartment.queue_points_list)

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
    apartments in that combination """

    try:
        tf = text_formatter.CombintationListing(combintations)
        tf.print()
    except NameError:
        print("Please run 'simulate()' first.")
