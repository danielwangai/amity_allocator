import random

from .fellow import Fellow
from .staff import Staff
from .office import Office
from .living_space import LivingSpace
from .database import Database


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

    def create_room(self, args):
        '''
            accepts a list as an argument containing a list of rooms
            when list validates correctly returns a string confirming
            successful addition.

            args contain - list of room names
                         - room type - Fellow/Staff
        '''
        for room in args["<name>"]:
            if args["office"]:
                if room in self.get_all_rooms(self.rooms['all_rooms']):
                    # reject adding an already existing room
                    print("Cannot create room named {0} since a room with the same name exists.".format(room))
                else:
                    '''
                        if room is an office:-
                            add new Office object and create an empty list to hold at most 6 occupants (Fellows and/or Staff)
                    '''
                    office = Office(room)
                    self.rooms['all_rooms'].append(office)
                    self.rooms['office'][office] = []
                    print("Office - {0} - successfully created".format(room))
            elif args["living_space"]:
                if room in self.get_all_rooms(self.rooms['all_rooms']):
                    # reject adding an already existing room
                    print("Cannot create room named {0} since a room with the same name exists.".format(room))
                else:
                    '''
                        if room is an living_space:-
                            add new LivingSpace object and create an empty list to hold at most 4 occupants (Fellows Only)
                    '''
                    living_space = LivingSpace(room)
                    self.rooms['all_rooms'].append(living_space)
                    self.rooms["living_space"][living_space] = []
                    print("Living Space - {0} - successfully created".format(room))

    def get_all_rooms(self, rooms):
        # iterate all rooms
        room_names = []
        for room in rooms:
            room_names.append(room.name)
        return room_names

    def add_person(self, args):
        wants_accomodation = "Yes" if args.get("<wants_accomodation>") is "Y" else "No"
        '''
            accepts 3 parameters:-
                - person_name - name of person
                - category - FELLOW/STAFF
            returns string confirming successful addition of person if inputs validate correctly
        '''
        if args["Fellow"]:
            new_fellow = Fellow(args["<first_name>"], args["<last_name>"])
            new_fellow.wants_accomodation = wants_accomodation
            self.people["all_people"].append(new_fellow)
            self.people["fellows"].append(new_fellow)

            # select office object
            select_office = lambda offices: random.choice(offices) if len(offices) > 0 else "No available office space"
            # allocate office)
            allocated_office = select_office(self.list_of_available_rooms(list(self.rooms["office"].keys()), "o"))

            if allocated_office == "No available office space":
                self.rooms["office_waiting_list"].append(new_fellow)
                # return "Sorry, no available office spaces yet. You'll be set on the waiting list"
                if args.get("<wants_accomodation>") is "Y":
                    # select living space
                    select_living_space = lambda living_spaces: random.choice(living_spaces) if len(living_spaces) > 0 else "No available living space slots"
                    # allocate living_space
                    allocated_living_space = select_living_space(self.list_of_available_rooms(list(self.rooms["living_space"].keys()), "l"))

                    print(allocated_living_space)
                    if allocated_living_space == "No available living space slots":
                        self.rooms["living_space_waiting_list"].append(new_fellow)
                        return "Sorry, no available living space slots yet. You've been set on the waiting list"
                    else:
                        print("{0} {1} id - {2}".format(new_fellow.first_name, new_fellow.last_name, new_fellow.person_id))
                        print("{0} {1} allocated to {2}".format(new_fellow.first_name, new_fellow.last_name, allocated_living_space.name))
                        self.rooms["living_space"][allocated_living_space].append(new_fellow)
            else:
                print("{0} {1} id - {2}".format(new_fellow.first_name, new_fellow.last_name, new_fellow.person_id))
                print("{0} {1} allocated to {2}".format(new_fellow.first_name, new_fellow.last_name, allocated_office.name))
                self.rooms["office"][allocated_office].append(new_fellow)

                if args.get("<wants_accomodation>") is "Y":
                    # select living space
                    select_living_space = lambda living_spaces: random.choice(living_spaces) if len(living_spaces) > 0 else "No available living space slots"
                    # allocate living_space
                    allocated_living_space = select_living_space(self.list_of_available_rooms(list(self.rooms["living_space"].keys()), "l"))
                    if allocated_living_space == "No available living space slots":
                        self.rooms["living_space_waiting_list"].append(new_fellow)
                        return "Sorry, no available living space slots yet. You've been set on the waiting list"
                    else:
                        print("{0} {1} id - {2}".format(new_fellow.first_name, new_fellow.last_name, new_fellow.person_id))
                        print("{0} {1} allocated to {2}".format(new_fellow.first_name, new_fellow.last_name, allocated_living_space.name))
                        self.rooms["living_space"][allocated_living_space].append(new_fellow)

        elif args["Staff"]:
            new_staff = Staff(args["<first_name>"], args["<last_name>"])
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
                print("{0} {1} id - {2}".format(new_staff.first_name, new_staff.last_name, new_staff.person_id))
                print("Staff {0} {1} allocated to {2}".format(new_staff.first_name, new_staff.last_name, allocated_office.name))
                self.rooms["office"][allocated_office].append(new_staff)

    def reallocate_person(self, person_id, room_type, new_room):
        if room_type in ["Office", "office", "O", "o"] and self.get_person_object_given_person_id(person_id) != "person id does not exist":
            # get current room
            # get_person_object_given_person_id
            person_object = self.get_person_object_given_person_id(person_id)
            current_room = self.get_room_from_person_id(person_id, "o")
            if self.get_room_from_room_name(new_room, "o") != "room name does not exist":
                new_room_object = self.get_room_from_room_name(new_room, "o")
                # remove person from current_room
                self.rooms["office"][current_room].remove(person_object)
                # add person to new_room_object
                self.rooms["office"][new_room_object].append(person_object)
                print("Reallocated {0} {1} from {2} to {3}\n".format(person_object.first_name, person_object.last_name,
                    current_room.name, new_room_object.name))
            else:
                print("Room {0} does not exist\n".format(new_room))
        elif room_type in ["Living", "living", "L", "l"] and self.get_person_object_given_person_id(person_id) != "person id does not exist":
            # get current room
            # get_person_object_given_person_id
            person_object = self.get_person_object_given_person_id(person_id)
            current_room = self.get_room_from_person_id(person_id, "l")
            if self.get_room_from_room_name(new_room, "l") != "room name does not exist":
                new_room_object = self.get_room_from_room_name(new_room, "l")
                # remove person from current_room
                self.rooms["living_space"][current_room].remove(person_object)
                # add person to new_room_object
                self.rooms["living_space"][new_room_object].append(person_object)
                print("Reallocated {0} {1} from {2} to {3}\n".format(person_object.first_name, person_object.last_name,
                    current_room.name, new_room_object.name))
            else:
                print("Room {0} does not exist\n".format(new_room))
        else:
            print("person with id {0} does not exist\n".format(person_id))


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

    def print_unallocated_to_office(self):
        '''
            prints out all people - Fellows and Staff - that have not been allocated
            an office
        '''
        # get all person objects from the waiting list
        unallocations = self.rooms["office_waiting_list"]
        if len(unallocations) > 0:
            print("The following is a list of persons with no office allocations\n")
            for person in unallocations:
                print("{0}, {1} - {2}".format(person.first_name, person.last_name, person.category))
        else:
            print("The are no unallocated people.")

    def print_unallocated(self):
        pass

    def print_allocations(self):
        pass


    def save_state(self, db_name=None):
        # save people data
        if db_name is not None:
            db_name = db_name + '.db'
        else:
            db_name = 'amity.db'

        # try:
        db = Database(db_name)
        db.create_tables()
        cursor = db.cursor()

        # Save all people
        print('Saving...')
        for key, value in self.people.items():
            if key == "fellows":
                for i in value:
                    try:
                        cursor.execute("INSERT INTO person VALUES (?, ?, ?, ?);",
                                   (i.person_id, i.first_name, i.last_name, i.category))
                    except sqlite3.IntegrityError:
                        continue
            if key == "staff":
                for i in value:
                    try:
                        cursor.execute("INSERT INTO person VALUES (?, ?, ?, ?);",
                                   (i.person_id, i.first_name, i.last_name, i.category))
                    except sqlite3.IntegrityError:
                        continue


        # save office data
        print('Saving office...')
        for room in list(self.rooms["office"].keys()):
            try:
                cursor.execute("INSERT INTO room VALUES (?, ?, ?);",
                           (room.room_id, room.name, 'office'))
            except sqlite3.IntegrityError:
                continue

        # save living_space data
        print('Saving Living Space...')
        for room in list(self.rooms["living_space"].keys()):
            try:
                cursor.execute("INSERT INTO room VALUES (?, ?, ?);",
                           (room.room_id, room.name, 'living_space'))
            except sqlite3.IntegrityError:
                continue
        db.commit()

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

    def print_fellows_unallocated_to_living_space(self):
        '''
            prints out a list of fellows lacking accomodation who are in the waiting list
        '''
        unallocations = self.rooms["living_space_waiting_list"]
        print("The following is a list of fellows unallocated to living spaces")
        for person in unallocations:
            print("{0}, {1} - {2}".format(person.first_name, person.last_name, person.category))

    def print_office_allocations(self):
        '''
            Prints out all people allocated to rooms
        '''
        list_of_offices = list(self.rooms["office"].keys())
        for office in list_of_offices:
            if len(self.rooms["office"][office]) > 0:
                print(office.name)
                print("---------------------------")
                persons_in_office = []
                for person in self.rooms["office"][office]:
                    name = person.first_name+ " "+ person.last_name
                    persons_in_office.append(name)
                print(', '.join(persons_in_office))
                print("\n")
            else:
                print("{0} - has no occupants currently".format(office.name))

    def print_living_space_allocations(self):
        '''
            Prints living spaces and people allocated to them
        '''
        list_of_living_spaces = list(self.rooms["living_space"].keys())
        for living_space in list_of_living_spaces:
            if len(self.rooms["living_space"][living_space]) > 0:
                print(living_space.name)
                print("---------------------------")
                persons_in_living_space = []
                for person in self.rooms["living_space"][living_space]:
                    name = person.first_name+ " "+ person.last_name
                    persons_in_living_space.append(name)
                print(', '.join(persons_in_living_space))
                print("\n")
            else:
                print("{0} - has no occupants currently\n".format(living_space.name))

    def print_room(self, args):
        '''
            takes room name as argument and if exists returns list of occupants
        '''
        room_name = args["<room_name>"]
        occupants = []
        offices = list(self.rooms["office"].keys())
        living_spaces = list(self.rooms["living_space"].keys())

        if room_name in [room.name for room in offices]:
            room_object = [room for room in list(self.rooms["office"].keys()) if room.name == room_name][0]
            occupants.extend(self.rooms["office"][room_object])
        elif room_name in [room.name for room in living_spaces]:
            room_object = [room for room in list(self.rooms["living_space"].keys()) if room.name == room_name][0]
            occupants.extend(self.rooms["living_space"][room_object])
        elif room_name not in [room.name for room in offices] or room_name in [room.name for room in living_spaces]:
            '''
                if room name does not exist
            '''
            print("Room {0} does not exist".format(room_name))
        if len(occupants) > 0:
            print("The occupants of the - {0} - are".format(room_name))
            print(", ".join([occupant.first_name for occupant in occupants]))
        else:
            print("The room {0} has no occupants currently".format(room_name))

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

    def get_room_from_room_name_update_all_rooms(self, room_name):
        result = None
        all_available_rooms = self.list_of_available_rooms(list(self.rooms["office"].keys()), "o")
        all_available_rooms.extend(self.list_of_available_rooms(list(self.rooms["living_space"].keys()), "l"))
        for room in all_available_rooms:
            if room_name in [room.name for room in all_available_rooms]:
                result = room
        if result == None:
            return "room name does not exist"
        else:
            return result
