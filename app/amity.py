import random

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
        for room in list_of_rooms:
            if room in self.get_all_rooms(self.rooms['all_rooms']):
                return "Cannot create room since a room with the same naem exists."
            if room_type in ["Office", "office", "O", "o"]:
                office = Office(room)
                self.rooms['all_rooms'].append(office)
                self.rooms['office'][office] = []
            elif room_type in ["Living", "living", "L", "l"]:
                living_space = LivingSpace(room)
                self.rooms['all_rooms'].append(living_space)
                self.rooms["living_space"][living_space] = []

    def get_all_rooms(self, rooms):
        # iterate all rooms
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
        if category.lower() in ["Fellow".lower(), "F".lower()]:
            new_fellow = Fellow(person_name)
            new_fellow.wants_accomodation = wants_accomodation
            self.people["all_people"].append(new_fellow)
            self.people["fellows"].append(new_fellow)

        elif category.lower() in ["Staff".lower(), "S".lower()]:
            new_staff = Staff(person_name)
            self.people["all_people"].append(new_staff)
            self.people["staff"].append(new_staff)

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

    def list_of_available_rooms(self, list_of_rooms, room_type):
        if room_type in ["Office", "office", "O", "o"]:
            # if room is office
            # get all office objects with space < 6
            return [room for room in list_of_rooms if len(list_of_rooms[room]) < 6]
        elif room_type in ["Living", "living", "L", "l"]:
            # if room is living space
            # get all living space objects with space < 4
            return [room for room in list_of_rooms if len(list_of_rooms[room]) < 4]
