# accommodation.py

import logging

from datetime import date
from typing import List


# ==== Setup logging ====
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] %(levelname)s:%(name)s: %(message)s')

file_handler = logging.FileHandler('apaato.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# ==== Setup logging ====


class Accommodation:
    """ Class used to store all the information about an accommodation """

    address: str
    deadline: date
    queue: List[int]

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


    # TODO: Remove this function, it is apparently not used...
    def position_in_queue(self, other_points: int) -> int:
        """ Calculates what position a person with other_points would be in the
        queue to accommodation. Returns 6 if the position is larger than or
        equal to 6 because only the top 5 queue points are visible """

        for i, points in enumerate(self.queue):
            if other_points > points:
                position = i+1
                break
        else:
            position = 6

        return position

    def insert_into_queue(self, other_points: int) -> None:
        """ Enter other_points into queue of accommodation """

        logger.debug(f"Inserting {other_points} into {self.queue}...")

        for i, points in enumerate(self.queue):
            if other_points > points:
                other_points, self.queue[i] = self.queue[i], other_points

        logger.debug(f"... which resulted in {self.queue}.")
