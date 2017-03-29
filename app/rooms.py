"""This file contains the definition of Room super class."""
from abc import ABCMeta, abstractmethod


class Room(metaclass=ABCMeta):
    """Class defines the structure of a room."""

    room_capacity = None

    def __init__(self, name):
        """To define the attributes of a room."""
        self.room_id = id(self)
        self.name = name

    @abstractmethod
    def __str__(self):
        pass
