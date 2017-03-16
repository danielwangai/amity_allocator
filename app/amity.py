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
        "living_space": {},
        "office_waiting_list": [],
        "living_space_waiting_list": []
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

            # select office object
            select_office = lambda offices: random.choice(offices) if len(offices) > 0 else "No available office space"
            # allocate office
            allocated_office = select_office(self.list_of_available_rooms(list(self.rooms["office"].keys()), "o"))

            if allocated_office == "No available office space":
                self.rooms["office_waiting_list"].append(new_fellow)
                return "Sorry, no available office spaces yet. You'll be set on the waiting list"
            else:
                print("{0} allocated to {1}".format(new_fellow.name, allocated_office.name))
                self.rooms["office"][allocated_office].append(new_fellow)

                if wants_accomodation in ["Y", "y"]:
                    # select living space
                    select_living_space = lambda living_spaces: random.choice(living_spaces) if len(living_spaces) > 0 else "No available living space slots"
                    # allocate living_space
                    allocated_living_space = select_living_space(self.list_of_available_rooms(list(self.rooms["living_space"].keys()), "l"))
                    if allocated_living_space == "No available living space slots":
                        self.rooms["living_space_waiting_list"].append(new_fellow)
                        return "Sorry, no available living space slots yet. You've been set on the waiting list"
                    else:
                        print("{0} allocated to {1}".format(new_fellow.name, allocated_living_space.name))
                        self.rooms["living_space"][allocated_living_space].append(new_fellow)

        elif category.lower() in ["Staff".lower(), "S".lower()]:
            new_staff = Staff(person_name)
            self.people["all_people"].append(new_staff)
            self.people["staff"].append(new_staff)

            # select office object
            select_office = lambda offices: random.choice(offices) if len(offices) > 0 else "No available office space"
            # allocate office
            allocated_office = select_office(self.list_of_available_rooms(list(self.rooms["office"].keys()), "o"))
            if allocated_office == "No available office space":
                self.rooms["office_waiting_list"].append(new_staff)
                return "Sorry, no available office spaces yet. You'll be set on the waiting list"
            else:
                print("Staff {0} allocated to {1}".format(new_staff.name, allocated_office.name))
                self.rooms["office"][allocated_office].append(new_staff)

    def reallocate_person(self, person_id):
        pass


    def get_room_from_person_id(self, person_id, room_type):
        result = None
        if room_type in ["Office", "office", "O", "o"]:
            for room in list(self.rooms["office"].keys()):
                if person_id in [person.person_id for person in self.rooms["office"][room]]:
                    result = room
        elif room_type in ["Living", "living", "L", "l"]:
            for room in list(self.rooms["living_space"].keys()):
                if person_id in [person.person_id for person in self.rooms["living_space"][room]]:
                    result = room

        if result == None:
            return "person id does not exist"
        else:
            return result

    def get_room_from_room_name(self, room_name, room_type):
        result = None
        if room_type in ["Office", "office", "O", "o"]:
            for room in list(self.rooms["office"].keys()):
                if room_name in [room.name for room in self.list_of_available_rooms(list(self.rooms["office"].keys()), "o")]:
                    result = room
        elif room_type in ["Living", "living", "L", "l"]:
            for room in list(self.rooms["living_space"].keys()):
                if room_name in [room.name for room in self.list_of_available_rooms(list(self.rooms["living_space"].keys()), "l")]:
                    result = room

        if result == None:
            return "room name does not exist"
        else:
            return result

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
            return [room for room in list_of_rooms if len(self.rooms["office"][room]) < 6]
        elif room_type in ["Living", "living", "L", "l"]:
            # if room is living space
            # get all living space objects with space < 4
            return [room for room in list_of_rooms if len(self.rooms["living_space"][room]) < 4]

    def is_allocated(self, person_object, room_type):
        """
            checks if a person is allocated to a room:-
                - checks if fellow is allocated to office and living space
                - checks if staff is allocated to office
        """
        if person_object.category in ["Fellow", "Staff"] and room_type in ["Office", "office", "O", "o"]:
            return (person_object in self.list_of_persons_allocated_to_offices())
        elif person_object.category == "Fellow" and room_type in ["Living", "living", "L", "l"]:
            return (person_object in self.list_of_fellows_allocated_to_living_spaces())

    def list_of_persons_allocated_to_offices(self):
        """
            returns a list of persons (Fellows and Staff) allocated to office spaces
        """
        persons_in_offices = []
        for i in list(self.rooms["office"].keys()):
            if len(self.rooms["office"][i]) > 0:
                persons_in_offices.extend(self.rooms["office"][i])
        return persons_in_offices

    def list_of_fellows_allocated_to_living_spaces(self):
        """
            returns a list of fellows allocated to living spaces
        """
        fellows_in_living_spaces = []
        for room in list(self.rooms["living_space"].keys()):
            if len(self.rooms["living_space"][room]) > 0:
                fellows_in_living_spaces.extend(self.rooms["living_space"][room])
        return fellows_in_living_spaces

    def get_person_object_given_person_id(self, person_id):
        # return [person for person in self.people["all_people"] if person.person_id == person_id][0]
        person_object = None
        for person in self.people["all_people"]:
            if person.person_id == person_id:
                person_object = person

        if person_object == None:
            return "person id does not exist"
        else:
            return person_object
