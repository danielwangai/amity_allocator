from fellow import Fellow
from staff import Staff
from office import Office
from living_space import LivingSpace


class Amity(object):

    '''
        people is a dictionary contains the following keys:-
            all_people - for fellows who opt for no accomodation:
                - a list of objects of all people
            fellows - For Fellows ONLY:
                - a list of objects of fellows

            staff - a dictionary with:
                - a list of objects of all staff
    '''
    people = {
        # stores all people -> fellows + staff
        "all_people": [],
        "fellows":[],
        "staff": []
    }

    '''
        rooms is a dictionary contains the following keys:-
            all_rooms - a list of room objects
            office - a dictionary with:
                key - room object
                value - list of person objects (Fellows & Staff) whose length cannot exceed 6

            living_space - a dictionary with:
                key - room object
                value - list of objects of occupants (Fellows ONLY) whose length cannot exceed 4
    '''
    rooms = {
        "all_rooms": [],
        "office": {},
        "living_space": {}
    }

    def create_room(self, list_of_rooms, room_type):
        '''
            accepts a list as an argument containing a list of rooms
            when list validates correctly returns a string confirming
            successful addition.
        '''
        pass

    def get_all_rooms(self, rooms):
        """
            Returns a list of all room names
        """
        room_names = []
        for room in rooms:
            room_names.append(room.name)
        return room_names

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
