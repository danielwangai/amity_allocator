from person import Person

class Staff(Person):
    wants_accomodation = "N"
    category = "Staff"
    def __init__(self, name):
        super(Staff, self).__init__(name)
