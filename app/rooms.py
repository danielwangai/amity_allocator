"""This file contains the definition of Room super class."""


class Room(object):
    """Class defines the structure of a room."""

    room_capacity = None

    def __init__(self, name):
        """To define the attributes of a room."""
        self.room_id = id(self)
        self.name = name
