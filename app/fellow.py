from person import Person

class Fellow(Person):
    '''
        by default accomodation is set to N(NO)
    '''
    wants_accomodation = "N"
    def __init__(self, person_id, name):
        super(Fellow, self).__init__(person_id, name)
