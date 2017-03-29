"""This file contains the definition of Fellow class."""
from .person import Person


class Fellow(Person):
    """Class inherits from Person class."""

    wants_accomodation = "N"
    category = "Fellow"

    def __init__(self, first_name, last_name):
        """Override the init method of Person superclass."""
        super(Fellow, self).__init__(first_name, last_name)

    def __str__(self):
        pass
