#text_formatter.py

# Import Generator for annotations
from typing import Generator

# Import framework
from apartment import Apartment


class TextFormatter:
    """ Class that handles the printing of the apartments """

    def __init__(self, apartments: list, *, queue_points: int):
        self.apartments = sorted(apartments, key=lambda x:
                            (x.position_in_queue(queue_points), x.applicants))

        self.queue_points = queue_points
        self.address_length = 0
        self.size_length = 0

        self.calculate_padding()

    def calculate_padding(self) -> None:
        """ Calculates the correct amount of padding for the apartment address
        and size """

        for a in self.apartments:

            # Address
            address_length = len(a.address)
            if address_length > self.address_length:
                self.address_length = address_length

            # Size
            size_length = len(a.size)
            if size_length > self.size_length:
                self.size_length = size_length

    def print_apartment(self, index: int, apartment: Apartment) -> None:
        """ Prints a single apartment given its index """

        def formatted_index() -> str:
            f_index = "{index:>{length}}".format(
                index=str(index+1) + ':',
                length=len(str(len(self.apartments)))+1)

            return f_index

        def formatted_position() -> str:
            f_position = "{position}".format(
                position=apartment.position_in_queue(self.queue_points))

            return f_position

        def formatted_apartment() -> str:
            f_address = "{apartment.address:<{address_length}}".format(
                apartment=apartment,
                address_length=self.address_length)

            f_size = "{apartment.size:<{size_length}}".format(
                apartment=apartment,
                size_length=self.size_length)

            f_link = "{apartment.link}".format(
                apartment=apartment)

            return ' '.join([f_address, f_size, f_link])

        def all_fields() -> Generator[str, None, None]:
            yield formatted_index()
            yield formatted_position()
            yield formatted_apartment()

        print(' '.join(list(all_fields())))

    def print_apartments(self):
        """ Prints all the apartments """

        for index, apartment in enumerate(self.apartments):
            self.print_apartment(index, apartment)
