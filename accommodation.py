# accommodation.py


class Accommodation:
    """ Class used to store all the information about an accommodation """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def position_in_queue(self, other_points: int) -> int:
        """ Calculates what position a person with other_points would be in the
        queue to accommodation. Returns 6 if the position is larger than or
        equal to 6 because only the top 5 queue points are visible """

        for i, queue_points in enumerate(self.queue_points_list):
            if other_points > queue_points:
                position = i+1
                break
        else:
            position = 6

        return position

    def insert_into_queue(self, other_points: int) -> None:
        """ Enter other_points into queue of accommodation """

        for i, points in enumerate(self.queue_points_list):
            if other_points > points:
                other_points, self.queue_points_list[i] = \
                    self.queue_points_list[i], other_points
