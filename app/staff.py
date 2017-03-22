"""This file contains the definition of Person class."""
from .person import Person


class Staff(Person):
    """Class inherits from Person class."""

    wants_accomodation = "N"
    category = "Staff"

    def __init__(self, first_name, last_name):
        """Override the init method of Person superclass."""
        super(Staff, self).__init__(first_name, last_name)
