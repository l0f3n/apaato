# printer.py

import time

from typing import Dict, Generator, List

from apaato.accommodation import Accommodation


def print_accommodations(
        accommodations: List[Accommodation], 
        display: Dict[str, bool],
        heading: bool = True) -> None:

    accommodations = sorted(accommodations, key=lambda a: a.address)

    # Calculates length of the longest value in each column.
    # {
    #   'address' : 18,
    #   'type' : 5,
    #   'location' : 8,
    #         .
    #         .
    # }
    lengths = {key: max(
        [len(str(getattr(a, key))) for a in accommodations]
        + [len(key) if heading else 0]
        )
        for key in display}

    # Creates a list with all headers. Each string is right-padded
    # according to maximum property length in each column.
    # ['Address', 'Type', 'Location', ...]
    header = [
        f"{name:<{lengths[name]}}".capitalize()
        for name, value in display.items()
        if value
        ] if heading else []

    # Creates a list of lists containing all accommodations. Each string is
    # right-padded according to maximum property length in each column.
    # [
    #   ['Rydsvägen 252 C.17', '1 rum', 'Ryd', ...]
    #                     .
    #                     .
    # ]
    accommodation_list = [
            [
            f"{str(getattr(accommodation, name)):<{lengths[name]}}"
            for name, value in display.items()
            if value
            ] for accommodation in accommodations
        ]

    output = '\n'.join(
        [' '.join(header)]
        + [' '.join(accommodation) for accommodation in accommodation_list]
        ) + '\n'

    print(output)


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
    """
    Print a progress bar.

    :param float progress: The current progress [0, 1]
    :param int max_length: Length of progress bar in characters
    """
    l = int(progress*max_length)
    print(f"\r[{l*'#'+(max_length-l)*'.'}] {progress:.2%} Completed", end='', flush=True)


def timer(prefix='Finished in ', suffix=' seconds.'):
    """
    Decorator used to print execution time of a function.

    :param str prefix: Text before time
    :param str suffix: Text after time
    """
    def inner_timer(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            ret = func(*args, **kwargs)
            print(f'{prefix}{time.time() - start_time:.1f}{suffix}')
            return ret
        return wrapper
    return inner_timer