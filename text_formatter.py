# text_formatter.py

# Import Generator for annotations
from typing import Generator

# Import framework
from apartment import Apartment


class ApartmentListing:
    """ Class that handles the printing of the apartments """

    def __init__(self, apartments: list, queue_points: int):
        self.apartments = sorted(apartments, key=lambda x:
                                 (x.position_in_queue(queue_points),
                                  x.applicants))

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

    def print(self):
        """ Prints all the apartments """

        for index, apartment in enumerate(self.apartments):
            self.print_apartment(index, apartment)


class CombintationListing:

    def __init__(self, combinations):
        self.combinations = sorted(combinations,
                                   key=lambda x: self.total_probability(x),
                                   reverse=True)

        self.total_probability_length = 0
        self.address_length = [0 for _ in range(5)]
        self.probability_length = [0 for _ in range(5)]

        self.calculate_padding()

    def calculate_padding(self) -> None:
        """ Calculates the correct amount of padding for the probability and
        address """

        for comb in self.combinations:

            # Total probability
            prob_length = self.probability_len(self.total_probability(comb))
            if prob_length > self.total_probability_length:
                self.total_probability_length = prob_length

            # Aparments and probability
            for index, apartment in enumerate(comb):

                address, prob = apartment

                apartment_length = len(address)
                if apartment_length > self.address_length[index]:
                    self.address_length[index] = apartment_length

                probability_length = self.probability_len(prob)
                if probability_length > self.probability_length[index]:
                    self.probability_length[index] = probability_length

    def probability_len(self, prob):
        """ Calculate the length of a formatted probability """

        f_probability = "{probability:.1%}".format(
            probability=prob)

        return len(f_probability)

    def total_probability(self, combination):
        """ Returns the chance of getting any apartment from combination """

        return sum((apartment[1] for apartment in combination))

    def print_combination(self, index, combination):
        """ Prints a formatted combination given index and combination """

        def formatted_index() -> str:
            f_index = "{index:>{length}}".format(
                index=str(index+1) + ':',
                length=len(str(len(self.combinations)))+1)

            return f_index

        def formatted_probability() -> str:
            f_probability = "{probability:>{length}.1%} |".format(
                probability=self.total_probability(combination),
                length=self.total_probability_length)

            return f_probability

        def formatted_apartment(index, apartment):
            f_a = "{probability:>{p_len}.1%} {address:<{a_len}}".format(
                p_len=self.probability_length[index],
                a_len=self.address_length[index]+1,
                address=apartment[0],
                probability=apartment[1])

            return f_a

        def formatted_apartments() -> str:

            f_apartments = ''.join([formatted_apartment(index, apartment)
                                    for index, apartment in
                                    enumerate(sorted(combination,
                                    key=lambda x: x[1], reverse=True))])

            return f_apartments

        def all_fields() -> Generator[str, None, None]:
            yield formatted_index()
            yield formatted_probability()
            yield formatted_apartments()

        print(' '.join(list(all_fields())))

    def print(self):
        """ Prints all combinations and their probabilites """

        for index, combination in enumerate(self.combinations):
            self.print_combination(index, combination)
