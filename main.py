#                main.py
#                   |
#           +-------+-------+
#           |               |
#       scraper.py      database.py
#           |               |
#           +-------+-------+
#                   |
#              apartment.py

# Import framework
import database
import scraper
import apartment


def load_apartments() -> None:
    """ Loads all apartments from studentbostader.se into the database """

    database.wipe_database()

    # TODO: Add proper loading animation
    for i, a in enumerate(scraper.fetch_all_apartments()):
        database.insert_apartment(a)
        print('Apartment {n} added to database.'.format(n=i+1))


def sort_apartments(points: int) -> None:
    """ Function that prints out all apartments in database sorted by the
    position a person with points would be in the apartment queues """

    apartments = list(database.all_apartments_in_database())
    sorted_apartments = sorted(apartments, key=lambda x:
                               (x.position_in_queue(points), x.applicants))

    six_found = False
    apartment.setup_name_formatting(sorted_apartments)
    for i, a in enumerate(sorted_apartments):

        if a.position_in_queue(points) == 6 and not six_found:
            print('-'*len(apartment_text))
            six_found = True

        apartment_text = '{index:>{length}} {position} | {apartment}'.format(
                index=str(i+1) + ':',
                position=a.position_in_queue(points),
                apartment=a,
                length=len(str(len(sorted_apartments))) + 1)
        print(apartment_text)
