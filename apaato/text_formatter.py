# text_formatter.py

# Import Generator for annotations
from typing import Generator

# Import framework
from apaato.accommodation import Accommodation


class AccommodationListing:
    """ Class that handles the printing of the accommodations """

    def __init__(self, accommodations: list, queue_points: int,
                 show_link: bool):

        self.accommodations = sorted(accommodations, key=lambda x:
                                     (x.position_in_queue(queue_points),
                                      x.queue_points_list[-1]))

        self.queue_points = queue_points
        self.address_length = 0
        self.size_length = 0

        self.show_link = show_link

        self.calculate_padding()

    def calculate_padding(self) -> None:
        """ Calculates the correct amount of padding for the accommodation
        address and size """

        for a in self.accommodations:

            # Address
            address_length = len(a.address)
            if address_length > self.address_length:
                self.address_length = address_length

            # Size
            size_length = len(a.size)
            if size_length > self.size_length:
                self.size_length = size_length

    def print_accommodation(self, index: int,
                            accommodation: Accommodation) -> None:
        """ Prints a single accommodation given its index """

        def formatted_index() -> str:
            f_index = "{index:>{length}}".format(
                index=str(index+1) + ':',
                length=len(str(len(self.accommodations)))+1)

            return f_index

        def formatted_position() -> str:
            f_position = "{position}".format(
                position=accommodation.position_in_queue(self.queue_points))

            return f_position

        def formatted_accommodation() -> str:
            f_address = "{accommodation.address:<{address_length}}".format(
                accommodation=accommodation,
                address_length=self.address_length)

            f_size = "{accommodation.size:<{size_length}}".format(
                accommodation=accommodation,
                size_length=self.size_length)

            base_link = ("https://www.studentbostader.se/en/find-apartments/"
                         "ledig-bostad?refid=")
            f_link = "{base_link}{accommodation.refid}".format(
                accommodation=accommodation,
                base_link=base_link) if self.show_link else ""

            return ' '.join([f_address, f_size, f_link])

        def all_fields() -> Generator[str, None, None]:
            yield formatted_index()
            yield formatted_position()
            yield formatted_accommodation()

        print(' '.join(list(all_fields())))

    def print(self):
        """ Prints all the accommodations """

        for index, accommodation in enumerate(self.accommodations):
            self.print_accommodation(index, accommodation)


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

            # accommodations and probability
            for index, accommodation in enumerate(comb):

                address, prob = accommodation

                accommodation_length = len(address)
                if accommodation_length > self.address_length[index]:
                    self.address_length[index] = accommodation_length

                probability_length = self.probability_len(prob)
                if probability_length > self.probability_length[index]:
                    self.probability_length[index] = probability_length

    def probability_len(self, prob):
        """ Calculate the length of a formatted probability """

        f_probability = "{probability:.1%}".format(
            probability=prob)

        return len(f_probability)

    def total_probability(self, combination):
        """ Returns the chance of getting any accommodation from
        combination """

        return sum((accommodation[1] for accommodation in combination))

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

        def formatted_accommodation(index, accommodation):
            f_a = " {probability:>{p_len}.1%} {address:<{a_len}}".format(
                p_len=self.probability_length[index],
                a_len=self.address_length[index]+1,
                address=accommodation[0],
                probability=accommodation[1])

            return f_a

        def formatted_accommodations() -> str:

            f_accommodations = ''.join([formatted_accommodation(index,
                                                                accommodation)
                                        for index, accommodation in
                                        enumerate(sorted(combination,
                                        key=lambda x: x[1], reverse=True))])

            return f_accommodations

        def all_fields() -> Generator[str, None, None]:
            yield formatted_index()
            yield formatted_probability()
            yield formatted_accommodations()

        print(' '.join(list(all_fields())))

    def print(self):
        """ Prints all combinations and their probabilities """

        for index, combination in enumerate(self.combinations):
            self.print_combination(index, combination)
