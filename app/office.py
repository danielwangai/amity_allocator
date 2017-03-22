"""This file contains the definition of office sublcass."""

from .rooms import Room


class Office(Room):
    """Class inherits from Room class."""

    room_capacity = 6

    def __init__(self, name):
        """Override the init method of Room superclass."""
        super(Office, self).__init__(name)
