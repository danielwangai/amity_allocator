from person import Person

class Fellow(Person):
    '''
        by default accomodation is set to N(NO)
    '''
    wants_accomodation = "N"
    category = "Fellow"
    def __init__(self, name):
        super(Fellow, self).__init__(name)
