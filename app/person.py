"""This file contains the definition of Person super class."""
from abc import ABCMeta, abstractmethod


class Person(metaclass=ABCMeta):
    """Class defines the structure of a person."""

    def __init__(self, first_name, last_name):
        """To define the attributes of a person."""
        self.person_id = id(self)
        self.first_name = first_name
        self.last_name = last_name

    @abstractmethod
    def __str__(self):
        pass
