"""This file contains the definition of Person super class."""


class Person(object):
    """Class defines the structure of a person."""

    def __init__(self, first_name, last_name):
        """To define the attributes of a person."""
        self.person_id = id(self)
        self.first_name = first_name
        self.last_name = last_name
