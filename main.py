# main.py

#                main.py
#                  |
#     +------------+-----------------+
#     |            |                 |
# scraper.py   database.py   text_formatter.py
#     |            |                 |
#     +------------+-----------------+
#                  |
#             apartment.py

# Import framework
import database
import scraper
from text_formatter import TextFormatter


def load_apartments() -> None:
    """ Loads all apartments from studentbostader.se into the database """

    database.wipe_database()

    # TODO: Add proper loading animation
    for i, a in enumerate(scraper.fetch_all_apartments()):
        database.insert_apartment(a)
        print('Apartment {n} added to database.'.format(n=i+1))


def list_apartments(points: int) -> None:
    """ Function that prints out all apartments in database sorted by the
    position a person with points would be in the apartment queues """

    apartments = list(database.all_apartments_in_database())

    tf = TextFormatter(apartments, queue_points=543)
    tf.print_apartments()
