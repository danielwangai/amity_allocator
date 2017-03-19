from .person import Person

class Staff(Person):
    wants_accomodation = "N"
    category = "Staff"
    def __init__(self, first_name, last_name):
        super(Staff, self).__init__(first_name, last_name)
