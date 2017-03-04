class Amity(object):

    '''
        people is a dictionary contains the following keys:-
            fellows - contains the following keys:
                no_accomodation - for fellows who opt for no accomodation:
                    key - person_id of fellow
                    value - name of fellow
                wants_accomodation - For Fellows ONLY:
                    key - person_id of fellow
                    value - name of fellow

            staff - a dictionary with:
                key - as person_id
                value - name of staff member
    '''
    people = {
        "fellows": {
            "no_accomodation": {},
            "wants_accomodation": {},
        },
        "staff": {}
    }

    '''
        rooms is a dictionary contains the following keys:-
            office - a dictionary with:
                key - as room name
                value - list of ids of occupants (Fellows & Staff) whose length cannot exceed 6

            living_space - a dictionary with:
                key - as room name
                value - list of ids of occupants (Fellows ONLY) whose length cannot exceed 4
    '''
    rooms = {
        "office": {},
        "living_space": {}
    }
