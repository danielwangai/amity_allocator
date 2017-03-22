"""Amity.

Has the following capabilities.
can:-
    create room
    add people
    allocate people to rooms
    reallocate people to rooms
    save state - persist data to database
    load state - fetch saved data from database

"""
import random
import sqlite3
import os

from termcolor import cprint

from .fellow import Fellow
from .staff import Staff
from .office import Office
from .living_space import LivingSpace
from .database import Database


class Amity(object):
    """People is a dictionary contains the following keys.

    all_people - for fellows who opt for no accomodation:
        - a list of objects of all people
    fellows - For Fellows ONLY:
        - a list of objects of fellows

    staff - a dictionary with:
        - a list of objects of all staff

    rooms is a dictionary contains the following keys:-
        all_rooms - a list of room objects
        office - a dictionary with:
            key - room object
            value - list of person objects (Fellows & Staff) whose length
            cannot exceed 6

        living_space - a dictionary with:
            key - room object
            value - list of objects of occupants (Fellows ONLY) whose
            length cannot exceed 4
    """

    people = {
        # stores all people -> fellows + staff
        "all_people": [],
        "fellows": [],
        "staff": []
    }

    rooms = {
        "all_rooms": [],
        "office": {},
        "living_space": {},
        "office_waiting_list": [],
        "living_space_waiting_list": []
    }

    def create_room(self, room_type, list_of_rooms):
        """To accept a list as an argument containing a list of rooms."""
        for room in list_of_rooms:
            if room_type == "office":
                if room in self.get_all_rooms(self.rooms['all_rooms']):
                    # reject adding an already existing room
                    cprint(
                        "Cannot create room named {0} since a room with the"
                        " same name exists.".format(room), "red")
                else:
                    '''
                        if room is an office:-
                            add new Office object and create an empty list to \
                                hold at most 6 occupants (Fellows and/or Staff)
                    '''
                    office = Office(room)
                    self.rooms['all_rooms'].append(office)
                    self.rooms['office'][office] = []
                    cprint("Office - {0} - successfully created".format(room),
                           "green")
            elif room_type == "living_space":
                if room in self.get_all_rooms(self.rooms['all_rooms']):
                    # reject adding an already existing room
                    cprint(
                        "Cannot create room named {0} since a room with the"
                        "same name exists.".format(room), "red")
                else:
                    '''
                        if room is an living_space:-
                            add new LivingSpace object and create an empty \
                                list to hold at most 4 occupants (Fellows Only)
                    '''
                    living_space = LivingSpace(room)
                    self.rooms['all_rooms'].append(living_space)
                    self.rooms["living_space"][living_space] = []
                    cprint("Living Space - {0} - successfully created".format(
                        room), "green")

    def get_all_rooms(self, rooms):
        """To return a list of room names."""
        # iterate all rooms
        room_names = []
        for room in rooms:
            room_names.append(room.name)
        return room_names

    def add_person(self, person_type, firstname, lastname, wants_accomodation):
        """To add a person and allocate them to an available room.

        Fellow can get both office and living space(optional).
        Staff only entitled to office space alone

        """
        if person_type == "Fellow":
            new_fellow = Fellow(firstname, lastname)
            new_fellow.wants_accomodation = wants_accomodation
            self.people["all_people"].append(new_fellow)
            self.people["fellows"].append(new_fellow)

            # select office object
            select_office = (lambda offices:
                             random.choice(offices) if len(
                                 offices) > 0 else "No available office space"
                             )
            # allocate office
            allocated_office = select_office(self.list_of_available_rooms("o"))

            if allocated_office == "No available office space":
                cprint("{0}\n".format(allocated_office), "red")
                cprint("{0} {1} has been put in waiting list\n".format(
                    new_fellow.first_name, new_fellow.last_name), "green")
                self.rooms["office_waiting_list"].append(new_fellow)

                if wants_accomodation is "Y":
                    # select living space
                    select_living_space = (lambda living_spaces:
                                           random.choice(living_spaces) if len(
                                               living_spaces) > 0 else
                                           "No available living space slots"
                                           )
                    # allocate living_space
                    allocated_living_space = select_living_space(
                        self.list_of_available_rooms("l"))

                    cprint(allocated_living_space, "green")
                    # if there are no available living spaces
                    if (allocated_living_space ==
                            "No available living space slots"):
                        # add person to living space waiting list
                        (self.rooms["living_space_waiting_list"].
                         append(new_fellow))

                        return ("Sorry, no available living space slots yet.\
                         You've been set on the waiting list")
                    else:
                        cprint("{0} {1} id - {2}".format(new_fellow.first_name,
                                                         new_fellow.last_name,
                                                         new_fellow.person_id),
                               "green")
                        cprint("{0} {1} allocated to {2} (living space)".format
                               (new_fellow.first_name,
                                new_fellow.last_name,
                                allocated_living_space.name),
                               "green")

                        (self.rooms["living_space"][allocated_living_space].
                            append(new_fellow))
            else:
                # if office space is available, allocate fellow to both
                # an office and a living space
                cprint("{0} {1} id - {2}"
                       .format(new_fellow.first_name,
                               new_fellow.last_name,
                               new_fellow.person_id), "green")
                cprint("{0} {1} allocated to {2} (office)".
                       format(new_fellow.first_name,
                              new_fellow.last_name,
                              allocated_office.name), "green")
                # add person to a slot in the allocated office
                self.rooms["office"][allocated_office].append(new_fellow)

                if wants_accomodation == "Yes":
                    # select living space
                    select_living_space = (lambda living_spaces:
                                           random.choice(living_spaces) if len(
                                               living_spaces) > 0 else
                                           "No available living space slots")
                    # allocate living_space
                    allocated_living_space = select_living_space(
                        self.list_of_available_rooms("l"))
                    if allocated_living_space == "No available \
                    living space slots":
                        (self.rooms["living_space_waiting_list"].
                         append(new_fellow))
                        return "Sorry, no available living space slots yet.\
                         You've been set on the waiting list"
                    else:
                        cprint("{0} {1} id - {2}".format(new_fellow.first_name,
                                                         new_fellow.last_name,
                                                         new_fellow.person_id),
                               "green")
                        cprint("{0} {1} allocated to {2} (living space)".
                               format(new_fellow.first_name,
                                      new_fellow.last_name,
                                      allocated_living_space.name),
                               "green")
                        (self.rooms["living_space"][allocated_living_space]
                         .append(new_fellow))

        elif person_type == "Staff":
            new_staff = Staff(firstname, lastname)
            self.people["all_people"].append(new_staff)
            self.people["staff"].append(new_staff)

            # select office object
            select_office = (lambda offices:
                             random.choice(offices) if len(
                                 offices) > 0 else
                             "No available office space"
                             )
            # allocate office
            allocated_office = select_office(self.list_of_available_rooms("o"))
            if allocated_office == "No available office space":
                # add to waiting list if office not available
                cprint("{0}\n".format(allocated_office), "red")
                cprint("{0} {1} has been put in waiting list\n".format(
                    new_staff.first_name, new_staff.last_name), "green")
                self.rooms["office_waiting_list"].append(new_staff)

                return ("Sorry, no available office spaces yet."
                        "You'll be set on the waiting list")
            else:
                if wants_accomodation == "Yes":
                    cprint("Staff cannot get living space\n", "red")
                # if office is availabl, allocate staff.
                cprint("{0} {1} id - {2}".format(new_staff.first_name,
                                                 new_staff.last_name,
                                                 new_staff.person_id), "green")
                cprint("Staff {0} {1} allocated to {2} (office)".format(
                    new_staff.first_name,
                    new_staff.last_name, allocated_office.name), "green")

                self.rooms["office"][allocated_office].append(new_staff)

    def reallocate_person(self, person_id, room_type, new_room):
        """To reallocate a person from one current room to the other."""
        if (room_type in ["Office", "office", "O", "o"] and
                self.get_person_object_given_person_id(person_id)
                != "person id does not exist"):
            # get current room
            # get_person_object_given_person_id
            person_object = self.get_person_object_given_person_id(person_id)
            current_room = self.get_room_from_person_id(person_id, "o")
            if (self.get_room_object_from_room_name(new_room)
                    != "room name does not exist"):
                new_room_object = self.get_room_object_from_room_name(new_room)
                # remove person from current_room
                self.rooms["office"][current_room].remove(person_object)
                # add person to new_room_object
                self.rooms["office"][new_room_object].append(person_object)
                print("Reallocated {0} {1} from {2} to {3}\n".format
                      (person_object.first_name, person_object.last_name,
                       current_room.name, new_room_object.name))
            else:
                print("Room {0} does not exist\n".format(new_room))
        elif (room_type in ["Living", "living", "L", "l"] and
              self.get_person_object_given_person_id(person_id) !=
              "person id does not exist"):
            # get current room
            # get_person_object_given_person_id
            person_object = self.get_person_object_given_person_id(person_id)
            current_room = self.get_room_from_person_id(person_id, "l")
            if (self.get_room_object_from_room_name(new_room) !=
                    "room name does not exist"):
                new_room_object = self.get_room_object_from_room_name(new_room)
                # remove person from current_room
                self.rooms["living_space"][current_room].remove(person_object)
                # add person to new_room_object
                (self.rooms["living_space"]
                 [new_room_object].append(person_object))
                print("Reallocated {0} {1} from {2} to {3}\n".format(
                    person_object.first_name, person_object.last_name,
                    current_room.name, new_room_object.name))
            else:
                print("Room {0} does not exist\n".format(new_room))
        else:
            print("person with id {0} does not exist\n".format(person_id))

    def get_room_from_person_id(self, person_id, room_type):
        """To return current room of a person given a valid person id."""
        result = None
        if room_type in ["Office", "office", "O", "o"]:
            for room in list(self.rooms["office"].keys()):
                if (person_id in [person.person_id
                                  for person in self.rooms["office"][room]]):
                    result = room
        elif room_type in ["Living", "living", "L", "l"]:
            for room in list(self.rooms["living_space"].keys()):
                if (person_id in [person.person_id for
                                  person in self.rooms["living_space"][room]]):
                    result = room

        if result:
            return result
        else:
            return "person id does not exist"

    def get_room_object_from_room_name_for_all_rooms(self, room_name):
        """To return room object given valid room name."""
        result = None
        all_rooms = []
        all_rooms.extend(list(self.rooms["office"].keys()))
        all_rooms.extend(list(self.rooms["living_space"].keys()))

        for room in all_rooms:
            if (room_name in [room.name for room in all_rooms if
                              room.name == room_name]):
                result = room
        if result:
            return result
        else:
            return "room name does not exist"

    def print_unallocated_to_office(self):
        """To print out persons allocated to offices."""
        # get all person objects from the waiting list
        unallocations = self.rooms["office_waiting_list"]
        if len(unallocations) > 0:
            print("The following is a list of\
             persons with no office allocations\n")
            for person in unallocations:
                cprint("{0}, {1} - {2}".format(person.first_name,
                                               person.last_name,
                                               person.category), "green")
        else:
            cprint("The are no unallocated people.", "red")

    def save_state(self, db_name=None):
        """To persist data to the database."""
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
        cprint('Saving...', "red")
        for key, value in self.people.items():
            if key == "fellows":
                for i in value:
                    try:
                        cursor.execute("INSERT INTO person VALUES \
                                        (?, ?, ?, ?);",
                                       (i.person_id, i.first_name,
                                        i.last_name, i.category))
                    except sqlite3.IntegrityError:
                        continue
            if key == "staff":
                for i in value:
                    try:
                        cursor.execute("INSERT INTO person VALUES \
                        (?, ?, ?, ?);",
                                       (i.person_id, i.first_name,
                                        i.last_name, i.category))
                    except sqlite3.IntegrityError:
                        continue

        # save office data
        cprint('Saving office...', "red")
        for room in list(self.rooms["office"].keys()):
            try:
                cursor.execute("INSERT INTO room VALUES (?, ?, ?);",
                               (room.room_id, room.name, 'office'))
            except sqlite3.IntegrityError:
                continue

        # save living_space data
        cprint('Saving Living Space...', "red")
        for room in list(self.rooms["living_space"].keys()):
            try:
                cursor.execute("INSERT INTO room VALUES (?, ?, ?);",
                               (room.room_id, room.name, 'living_space'))
            except sqlite3.IntegrityError:
                continue
        # save allcations - offices
        cprint("Saving office allocations", "red")
        for room in list(self.rooms["office"].keys()):
            for person in self.rooms["office"][room]:
                try:
                    cursor.execute("INSERT INTO allocations(person_id, room_id)\
                     VALUES(?, ?);",
                                   (person.person_id, room.room_id))
                except sqlite3.IntegrityError:
                    continue

        # save allcations - living spaces
        cprint("Saving living space allocations", "red")
        for room in list(self.rooms["living_space"].keys()):
            for person in self.rooms["living_space"][room]:
                try:
                    cursor.execute("INSERT INTO allocations(person_id, room_id)\
                     VALUES(?, ?);",
                                   (person.person_id, room.room_id))
                except sqlite3.IntegrityError:
                    continue

        # save unallocated people to office waiting lists
        cprint("Saving people unallocated to offices", "red")
        for person in self.rooms["office_waiting_list"]:

            try:
                # print(type(person.person_id))
                cursor.execute("INSERT INTO unallocated (person_id,\
                 missing_room) VALUES(?, ?)",
                               (person.person_id, "s", ))
            except sqlite3.IntegrityError:
                continue

        # save unallocated people to office waiting lists
        cprint("Saving people unallocated to living spaces", "red")
        for person in self.rooms["living_space_waiting_list"]:

            try:
                # print(type(person.person_id))
                cursor.execute("INSERT INTO unallocated (person_id,\
                 missing_room) VALUES(?, ?)",
                               (person.person_id, "living_space", ))
            except sqlite3.IntegrityError:
                continue

        db.commit()

    def load_state(self, db_name):
        """To fetch data saved in the database and load them to amity."""
        # get db
        db = Database(db_name)
        db.create_tables()
        cursor = db.cursor()

        # fetch people
        cprint('Loading people', "red")
        cursor.execute("SELECT * from person")
        people = cursor.fetchall()
        # print(people)
        for person in people:
            # populate db
            if person[3] == 'Fellow':
                fellow = Fellow(person[1], person[2])
                fellow.person_id = person[0]
                # add to data structures
                self.people["all_people"].append(fellow)
                self.people["fellows"].append(fellow)

            elif person[3] == 'Staff':
                staff = Staff(person[1], person[2])
                staff.person_id = person[0]
                self.people["all_people"].append(staff)
                self.people["staff"].append(staff)
        # load rooms
        cursor.execute("SELECT * FROM room")
        rooms = cursor.fetchall()
        for room in rooms:
            if room[2] == "office":
                office = Office(room[1])
                office.room_id = room[0]
                # save offices to data structures
                self.rooms["all_rooms"].append(office)
                self.rooms["office"][office] = []
            elif room[2] == "living_space":
                living_space = LivingSpace(room[1])
                living_space.room_id = room[0]
                # save living_spaces to data structures
                self.rooms["all_rooms"].append(living_space)
                self.rooms["living_space"][living_space] = []
        # get allocated
        cursor.execute("SELECT * FROM allocations")
        allocated_people = cursor.fetchall()
        for person in allocated_people:
            current_room = [room for room in self.rooms["all_rooms"]
                            if room.room_id == person[2]][0]
            person_object = self.get_person_object_given_person_id(person[1])
            # print(person_object)
            if type(current_room) == Office:
                self.rooms["office"][current_room].append(person_object)
            elif type(current_room) == LivingSpace:
                self.rooms["living_space"][current_room].append(person_object)
        # print("All allocated people loaded successfully")

        # get unallocated
        cursor.execute("SELECT * FROM unallocated")
        allocated_people = cursor.fetchall()
        for person in allocated_people:
            if person[1] == "office":
                person_object = (self.get_person_object_given_person_id(
                    person[2]))
                self.rooms["office_waiting_list"].append(person_object)
            elif person[1] == "living_space":
                person_object = (self.get_person_object_given_person_id(
                    person[1]))
                self.rooms["living_space_waiting_list"].append(person_object)
        # print(self.rooms["office_waiting_list"])

        os.remove(db_name)

    def list_of_available_rooms(self, room_type):
        """To list all available rooms slots."""
        if room_type in ["Office", "office", "O", "o"]:
            # if room is office
            # get all office objects with space < 6
            return ([room for room in list(self.rooms["office"].keys())
                     if len(self.rooms["office"][room]) < 6])
        elif room_type in ["Living", "living", "L", "l"]:
            # if room is living space
            # get all living space objects with space < 4
            return ([room for room in list(self.rooms["living_space"].keys())
                     if len(self.rooms["living_space"][room]) < 4])

    def is_allocated(self, person_object, room_type):
        """To check if a person is allocated to a room."""
        if (person_object.category in ["Fellow", "Staff"]
                and room_type in ["Office", "office", "O", "o"]):
            return (person_object in
                    self.list_of_persons_allocated_to_offices())
        elif (person_object.category == "Fellow"
              and room_type in ["Living", "living", "L", "l"]):
            return (person_object in
                    self.list_of_fellows_allocated_to_living_spaces())

    def print_fellows_unallocated_to_living_space(self):
        """To print out a list of fellows lacking accomodation."""
        unallocations = self.rooms["living_space_waiting_list"]
        cprint("The following is a list of \
        fellows unallocated to living spaces", "red")
        for person in unallocations:
            cprint("{0}, {1} - {2}".format(person.first_name, person.last_name,
                                           person.category), "red")

    def print_office_allocations(self):
        """To print out all people allocated to rooms."""
        list_of_offices = list(self.rooms["office"].keys())
        if len(list_of_offices) > 0:

            for office in list_of_offices:
                if len(self.rooms["office"][office]) > 0:
                    print(office.name)
                    print("---------------------------")
                    persons_in_office = []
                    for person in self.rooms["office"][office]:
                        name = person.first_name + " " + person.last_name
                        persons_in_office.append(name)
                    cprint(', '.join(persons_in_office), "red")
                    print("\n")
                else:
                    print("{0} - has no occupants currently".
                          format(office.name))
        else:
            cprint("No office spaces exist", "red")

    def print_living_space_allocations(self):
        """To print living spaces and people allocated to them."""
        list_of_living_spaces = list(self.rooms["living_space"].keys())
        if len(list_of_living_spaces) > 0:

            for living_space in list_of_living_spaces:
                if len(self.rooms["living_space"][living_space]) > 0:
                    print(living_space.name)
                    print("---------------------------")
                    persons_in_living_space = []
                    for person in self.rooms["living_space"][living_space]:
                        name = person.first_name + " " + person.last_name
                        persons_in_living_space.append(name)
                    cprint(', '.join(persons_in_living_space), "red")
                    print("\n")
                else:
                    cprint("{0} - has no occupants currently\n".
                           format(living_space.name), "red")
        else:
            cprint("No living space exist", "red")

    def print_room(self, room_name):
        """To return a list of room occupants."""
        occupants = []
        offices = list(self.rooms["office"].keys())
        living_spaces = list(self.rooms["living_space"].keys())

        if room_name in [room.name for room in offices]:
            room_object = [room for room in list(
                self.rooms["office"].keys()) if room.name == room_name][0]
            occupants.extend(self.rooms["office"][room_object])
            if len(occupants) > 0:
                cprint("The occupants of the - {0} - are".
                       format(room_name), "red")
                cprint(", ".join([occupant.first_name for
                                  occupant in occupants]), "red")
            else:
                cprint("The room {0} has no occupants currently".
                       format(room_name), "red")
        elif room_name in [room.name for room in living_spaces]:
            room_object = [room for room in list(
                self.rooms["living_space"].keys())
                if room.name == room_name][0]
            occupants.extend(self.rooms["living_space"][room_object])
            if len(occupants) > 0:
                cprint("The occupants of the - {0} - are".
                       format(room_name), "red")
                cprint(", ".join([occupant.first_name
                                  for occupant in occupants]), "red")
            else:
                cprint("The room {0} has no occupants currently".
                       format(room_name), "red")
        elif (room_name not in [room.name for room in offices] or
              room_name in [room.name for room in living_spaces]):
            '''
                if room name does not exist
            '''
            cprint("Room {0} does not exist".format(room_name), "red")

    def list_of_persons_allocated_to_offices(self):
        """To return a list of persons allocated to office spaces."""
        persons_in_offices = []
        for i in list(self.rooms["office"].keys()):
            if len(self.rooms["office"][i]) > 0:
                persons_in_offices.extend(self.rooms["office"][i])
        return persons_in_offices

    def list_of_fellows_allocated_to_living_spaces(self):
        """To return a list of fellows allocated to living spaces."""
        fellows_in_living_spaces = []
        for room in list(self.rooms["living_space"].keys()):
            if len(self.rooms["living_space"][room]) > 0:
                fellows_in_living_spaces.extend(
                    self.rooms["living_space"][room])
        return fellows_in_living_spaces

    def get_person_object_given_person_id(self, person_id):
        """To return object of a person given valid person id."""
        person_object = None
        for person in self.people["all_people"]:
            if person.person_id == person_id:
                person_object = person

        if person_object:
            return person_object
        else:
            return "person id does not exist"

    def get_room_object_from_room_name_for_available_rooms(self, room_name):
        """To return room object given valid room name."""
        result = None
        all_available_rooms = (self.list_of_available_rooms("o"))
        all_available_rooms.extend(self.list_of_available_rooms("l"))
        for room in all_available_rooms:
            if room_name in [room.name for room in all_available_rooms]:
                result = room
        if result:
            return result
        else:
            return "room name does not exist"
