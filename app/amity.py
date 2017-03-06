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
        # stores all people -> fellows + staff
        "all_people": [],
        "fellows": {
            "no_accomodation": [],
            "wants_accomodation": [],
        },
        "staff": []
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
        "all_rooms": [],
        "office": [],
        "living_space": []
    }

    def create_room(self, list_of_rooms, room_type):
        '''
            accepts a list as an argument containing a list of rooms
            when list validates correctly returns a string confirming
            successful addition.
        '''
        pass
    def add_person(self, person_name, category, wants_accomodation='N'):
        '''
            accepts 3 parameters:-
                - person_name - name of person
                - category - FELLOW/STAFF
                - wants_accomodation - with default value N
            returns string confirming successful addition of person if inputs validate correctly
        '''
        pass

    def reallocate_person(self, person_id):
        pass


    def load_people(self, file_path):
        '''
            Takes path to file as argument and populates people in specific lists
        '''
        pass

    def print_unallocated(self):
        pass

    def print_allocations(self):
        pass

    def print_room(self, room_name):
        '''
            takes room name as argument and if exists returns list of occupants
        '''
        pass

    def save_state(self):
        pass

    def load_state(self):
        pass
