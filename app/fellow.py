from person import Person

class Fellow(Person):
    '''
        by default accomodation is set to N(NO)
    '''
    wants_accomodation = "N"
    category = "Fellow"
    def __init__(self, first_name, last_name):
        super(Fellow, self).__init__(first_name, last_name)
