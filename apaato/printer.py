# printer.py

import time

from typing import Dict, List, Tuple

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


def print_probabilities(probabilities: List[Tuple[str, float]]):
    
    # Constructs the output for printing like this:
    # 100%: Rydsvägen 230 B.17
    #  87%: Rydsvägen 230 B.18
    #         .
    #         .
    output = '\n'.join([f"{percent:>4.0%}: {address}" 
                for address, percent in sorted(probabilities, 
                                               key=lambda x: x[1], 
                                               reverse=True)])

    print(output)


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