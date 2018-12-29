
ADDRESS_LENGTH = 0
SIZE_LENGTH = 0


class Apartment:
    """ Class used to store all the information about an apartment """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        # TODO: make this a clickable link
        return ("{self.address:<{address_length}} " +
                "{self.size:<{size_length}} {self.link}").format(
                    self=self,
                    address_length=ADDRESS_LENGTH,
                    size_length=SIZE_LENGTH)

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


def setup_name_formatting(apartments: list) -> None:
    """ Functions that calculates the right amount of padding for each field
    in the apartment.__str__ method. Call this before printing any apartments
    """

    global ADDRESS_LENGTH, SIZE_LENGTH
    for a in apartments:

        # Address
        length = len(a.address)
        if length > ADDRESS_LENGTH:
            ADDRESS_LENGTH = length

        # Size
        length = len(a.size)
        if length > SIZE_LENGTH:
            SIZE_LENGTH = length
