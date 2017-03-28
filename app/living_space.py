"""This file contains the definition of living space sublcass."""

from .rooms import Room


class LivingSpace(Room):
    """Class inherits from Room class."""

    room_capacity = 6

    def __init__(self, name):
        """Override the init method of Ro superclass."""
        super(LivingSpace, self).__init__(name)

    def __str__(self):
        pass
