#apartment.py

class Apartment:
    """ Class used to store all the information about an apartment """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def position_in_queue(self, other_points: int) -> int:
        """ Calculates what position a person with other_points would be in the
        queue to apartment. Returns 6 if the position is larger than or equal
        to 6 because only the top 5 queue points are visible """

        for i, queue_points in enumerate(self.queue_points_list):
            if other_points > queue_points:
                position = i+1
                break
        else:
            position = 6

        return position
