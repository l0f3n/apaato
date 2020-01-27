# text_formatter.py

# Import Generator for annotations
from typing import Generator

# Import framework
from apaato.accommodation import Accommodation


class AccommodationListing:
    """ Class that handles the printing of the accommodations """

    def __init__(self,
                 accommodations: list,
                 show_link: bool = False,
                 show_type: bool = False,
                 show_location: bool = False, ):

        self.show_link     = show_link
        self.show_type     = show_type
        self.show_location = show_location

        self.accommodations = sorted(accommodations, key=lambda x: x.address[0])

        self.address_length  = 0
        self.type_length     = 0
        self.location_length = 0

        self.calculate_padding()

    def calculate_padding(self) -> None:
        """ Calculates the correct amount of padding for the accommodation
        address and size """

        self.address_length  = max(len(a.address)  for a in self.accommodations) + 1
        self.type_length     = max(len(a.type)     for a in self.accommodations) + 1
        self.location_length = max(len(a.location) for a in self.accommodations) + 1

    def print_accommodation(self,
                            index: int,
                            accommodation: Accommodation) -> None:
        """ Prints a single accommodation given its index """

        # index
        f_index = f"{index+1:>{len(str(len(self.accommodations)))}}: "

        # accommodation
        f_address = f"{accommodation.address:<{self.address_length}}"

        f_size = f"{accommodation.type:<{self.type_length}}"         if self.show_type     else ""
        f_area = f"{accommodation.location:<{self.location_length}}" if self.show_location else ""
        f_link = f"{accommodation.url}"                              if self.show_link     else ""

        f_accommodation = f_index + f_address + f_size + f_area + f_link

        print(f_accommodation)

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

        print('Estimated probabilities of getting an accommodation:')

        for index, combination in enumerate(self.combinations):
            self.print_combination(index, combination)


def print_progress_bar(progress: float, max_length: int = 40):
    """ Simple progress bar. Progress is how far along it should be [0, 1] and
    max_length is the maximum length the progress bar will reach. """
    l = int(progress*max_length)
    print(f"\r[{l*'#'+(max_length-l)*'.'}] {progress:.2%} Completed", end='',
        flush=True)
