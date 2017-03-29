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
import os
import random

from termcolor import cprint
from tabulate import tabulate

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
                            add new LivingSpace object and create an empty
                                list to hold at most 4 occupants (Fellows Only)
                    '''
                    living_space = LivingSpace(room)
                    self.rooms['all_rooms'].append(living_space)
                    self.rooms["living_space"][living_space] = []
                    cprint("Living Space - {0} - successfully created".format(
                        room), "green")

    def add_person(self, person_type, firstname, lastname,
                   wants_accomodation="N"):
        """To add a person and allocate them to an available room.

        Fellow can get both office and living space(optional).
        Staff only entitled to office space alone

        """
        wants_accomodation = ("Yes" if wants_accomodation is
                              "Y" else "No")
        if person_type == "Fellow":
            new_fellow = Fellow(firstname, lastname)
            new_fellow.wants_accomodation = wants_accomodation
            self.people["fellows"].append(new_fellow)
            # allocate to office
            allocated_office = self.random_room_select("office")
            if allocated_office == "No available office space":
                self.handle_no_available_office_space(new_fellow)
                # allocate living space if available
                self.handle_living_space_accomodation(new_fellow,
                                                      wants_accomodation)
            else:
                # allocate room
                self.handle_office_allocations(new_fellow, allocated_office)
                self.handle_living_space_accomodation(new_fellow,
                                                      wants_accomodation)
        else:
            new_staff = Staff(firstname, lastname)
            new_staff.wants_accomodation = wants_accomodation
            self.people["staff"].append(new_staff)
            allocated_office = self.random_room_select("office")
            if allocated_office == "No available office space":
                self.handle_no_available_office_space(new_staff)
                # allocate living space if available
                self.handle_living_space_accomodation(new_staff,
                                                      wants_accomodation)
            else:
                # allocate room
                self.handle_office_allocations(new_staff, allocated_office)
                self.handle_living_space_accomodation(new_staff,
                                                      wants_accomodation)

    def reallocate_person(self, person_id, new_room):
        """To reallocate a person from one current room to the other."""
        # get person_object from person id
        person_object = self.get_person_object_given_person_id(person_id)
        new_room_object = (self.
                           get_room_object_from_room_name_for_available_rooms(
                               new_room))
        if person_object == "person id does not exist":
            cprint("person id does not exist.", "red")
            return "person id does not exist."
        elif new_room not in self.get_all_rooms(self.rooms['all_rooms']):
            cprint("Room does not exist.", "red")
            return 'Room does not exist.'
        elif new_room_object == "room name does not exist":
            cprint("The room {} has no space.".format(new_room), "red")
            return "The room {} has no space.".format(new_room)
        else:
            if (type(person_object) == Staff and
                    type(new_room_object) == LivingSpace):
                cprint("Cannot reallocate staff to living space.", "red")
                return "Cannot reallocate staff to living space."
            elif type(new_room_object) == Office:
                current_room = self.get_room_from_person_id(
                    person_id, "o")
                if current_room == "person id does not exist":
                    # if person has has no office
                    (cprint("{} has no current office space,hence canot "
                            "reallocate".format(
                                person_object.first_name)))
                    return "{} has no current office space, "
                    "hence canot reallocate".format(person_object.first_name)
                elif current_room == new_room_object:
                    cprint("Cannot reallocate to same room.", "red")
                    return "Cannot reallocate to same room."
                else:
                    # remove from current office
                    (self.rooms["office"][current_room].remove(
                        person_object))
                    # append to new room
                    (self.rooms["office"][new_room_object].append(
                        person_object))
                    cprint("{} {} has been reallocated from office {} to {}".
                           format(person_object.first_name,
                                  person_object.last_name, current_room.name,
                                  new_room_object.name))
                    return ("{} {} has been reallocated from office {} to {}".
                            format(person_object.first_name,
                                   person_object.last_name, current_room.name,
                                   new_room_object.name))
            elif type(new_room_object) == LivingSpace:
                current_room = self.get_room_from_person_id(person_id, "l")
                if current_room == "person id does not exist":
                    (cprint("{} has no current living space, hence cannot "
                            "reallocate".format(person_object.first_name)))
                    return ("{} has no current living space, hence cannot "
                            "reallocate".format(person_object.first_name))
                elif current_room == new_room_object:
                    cprint("Cannot reallocate to same room.", "red")
                    return "Cannot reallocate to same room."
                else:
                    # remove from current office
                    (self.rooms["living_space"][current_room].remove(
                        person_object))
                    # append to new room
                    (self.rooms["living_space"][new_room_object].
                     append(person_object))
                    cprint("{} {} has been reallocated from living space {} "
                           "to {}".format(person_object.first_name,
                                          person_object.last_name,
                                          current_room.name,
                                          new_room_object.name))
                    return ("{} {} has been reallocated from living space {}"
                            " to {}".format(person_object.first_name,
                                            person_object.last_name,
                                            current_room.name,
                                            new_room_object.name))

    def save_state(self, db_name=None):
        """To persist data to the database."""
        if not db_name:
            db_name = "amity_data.db"

        if not self.rooms["all_rooms"] or not self.people["all_people"]:
            cprint("Cannot load empty data fo db."
                   " Populate data then save state.")
            return ("Cannot load empty data fo db. Populate data then"
                    " save state.")
        db = Database(db_name)
        db.save_state(db_name, self.people, self.rooms)

    def load_people(self, text_file):
        """To fetch data from text file to and load into amity."""
        if os.path.isfile(text_file):
            with open(text_file, "r") as f:
                output = f.read()
                raw_data = output.split("\n")
                for i in raw_data:
                    row = i.split(" ")
                    if len(row) > 3:
                        self.add_person("Y", row[0], row[1],
                                        row[2].capitalize())
                    else:
                        self.add_person("N", row[0], row[1],
                                        row[2].capitalize())
            return "File found"
        else:
            cprint("File does not exist.", "red")
            return "File does not exist."

    def load_state(self, db_name):
        """To fetch data saved in the database and load them to amity."""
        # get db
        db = Database(db_name)
        collected_data = db.load_state(db_name, self.people, self.rooms)
        if (not collected_data[0] and not collected_data[1] and
                not collected_data[2] and not collected_data[3]):
                # test if is memptu
            cprint("No data in {}".format(db_name), "red")
            return "No data in {}".format(db_name)
        else:
            people = collected_data[0]
            self.populate_people(people)

            self.populate_rooms(collected_data[1])
            self.populate_allocated_people(collected_data[2])
            self.populate_unallocated_people(collected_data[3])
            return "Data load from {} success".format(db_name)

    def print_unallocated(self, text_file=None):
        """To print out a people without space."""
        unallocated_office = self.rooms["office_waiting_list"]
        unallocated_living_space = self.rooms["living_space_waiting_list"]
        if text_file:
            if not unallocated_office and not unallocated_living_space:
                cprint("There are no unallocations")
                return "There are no unallocations"
            else:
                self.dump_unallocated_to_file(text_file, unallocated_office,
                                              unallocated_living_space)
                return "Successfully dumped unallocated people to file."
        else:
            self.print_unallocated_to_office(unallocated_office)
            self.print_unallocated_to_living_space(unallocated_living_space)
            return "Successfully printed unallocated people to screen."

    def print_unallocated_to_office(self, unallocated_office):
        """To print out people unallocated to offices."""
        if unallocated_office:
            cprint("The following are people lacking space.", "red")
            cprint("---------------------------------------", "white")
            headers = ["person id", "first name", "last name",
                       "person category"]
            table = []
            for person in unallocated_office:
                table.append([person.person_id, person.first_name,
                              person.last_name, "Fellow"
                              if type(person) == Fellow else "Staff"])
            cprint(tabulate(table, headers, tablefmt="fancy_grid"), "white")
        else:
            cprint("There are no persons lacking living space.", "red")
        cprint("\n")

    def print_unallocated_to_living_space(self, unallocated_living_space):
        """To print fellows unallocated to living spaces."""
        if unallocated_living_space:
            cprint("The following are people lacking living space.", "red")
            cprint("---------------------------------------", "white")
            headers = ["person id", "first name", "last name",
                       "person category"]
            table = []
            for person in unallocated_living_space:
                table.append([person.person_id, person.first_name,
                              person.last_name, "Fellow"
                              if type(person) == Fellow else "Staff"])
            cprint(tabulate(table, headers, tablefmt="fancy_grid"), "white")
        else:
            cprint("There are no persons lacking living space.", "red")

    def print_allocations(self, text_file=None):
        """To print rooms and people allocated to them."""
        if text_file:
            list_of_offices = list(self.rooms["office"].keys())
            list_of_living_spaces = list(self.rooms["living_space"].keys())

            if not list_of_offices and not list_of_living_spaces:
                cprint("There are no allocations.")
                return "There are no allocations."
            else:
                self.dump_allocated_to_text_file(
                    text_file,
                    list_of_offices,
                    list_of_living_spaces)
                return "Successfully dumped to file."
        else:
            self.print_office_allocations()
            self.print_living_space_allocations()
            return "Allocations successfully printed to screen."

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
                       format(room_name), "white")
                cprint(", ".join([occupant.first_name for
                                  occupant in occupants]), "green")
                return "Office printed successfuly."
            else:
                cprint("The room {0} has no occupants currently".
                       format(room_name), "red")
                return ("There are no occupants in the {} currently.".format(
                    room_name))
        elif room_name in [room.name for room in living_spaces]:
            room_object = [room for room in list(
                self.rooms["living_space"].keys())
                if room.name == room_name][0]
            occupants.extend(self.rooms["living_space"][room_object])
            if len(occupants) > 0:
                cprint("The occupants of the - {0} - are".
                       format(room_name), "white")
                cprint(", ".join([occupant.first_name
                                  for occupant in occupants]), "green")
                return "Living Space printed successfuly."
            else:
                cprint("The room {0} has no occupants currently".
                       format(room_name), "red")
                return "There are no occupants in the room currently."
        elif (room_name not in [room.name for room in offices] or
              room_name in [room.name for room in living_spaces]):
            cprint("Room {0} does not exist".format(room_name), "red")
            return "Room {} does not exist.".format(room_name)

    def print_all_rooms(self):
        """To print all rooms."""
        headers = ["room id", "room name", "room type"]
        table = []
        all_rooms = self.rooms["all_rooms"]
        if all_rooms:
            for room in all_rooms:
                table.append([room.room_id, room.name,
                              ("Office" if type(room) == Office
                               else "Living Space")])
            cprint(tabulate(table, headers, tablefmt="fancy_grid"), "white")
        else:
            cprint("There are no rooms currently.", "red")
            return "There are no rooms currently."

    def print_all_people(self):
        """To print out all people."""
        all_people = self.people["all_people"]
        if all_people:
            headers = ["person id", "first name", "last name",
                       "role", "has office"]
            table = []
            for person in all_people:
                table.append([person.person_id, person.first_name,
                              person.last_name, ("Fellow" if type(person) ==
                                                 Fellow else "Staff")])
            cprint(tabulate(table, headers, tablefmt="fancy_grid"), "white")
        else:
            cprint("There are no people currently", "red")
    # Amity helper method begin here."""

    def get_all_rooms(self, rooms):
        """To return a list of room names."""
        # iterate all rooms
        room_names = []
        for room in rooms:
            room_names.append(room.name)
        return room_names

    def handle_no_available_office_space(self, person_object):
        """To handle cases of no office space."""
        # put to waiting list
        self.people["all_people"].append(person_object)
        self.rooms["office_waiting_list"].append(person_object)
        print("{0} {1} id {2} has been put to office waiting list".format(
            person_object.first_name, person_object.last_name,
            person_object.person_id))

    def handle_office_allocations(self, person_object, allocated_office):
        """To handle office allocation."""
        self.rooms["office"][allocated_office].append(person_object)
        self.people["all_people"].append(person_object)
        cprint("{} {} id {} allocated to {} (office)".format(
            person_object.first_name, person_object.last_name,
            person_object.person_id, allocated_office.name), "blue")

    def handle_living_space_accomodation(self, person_object, accomodation):
        """To handle living space allocation."""
        if accomodation == "Yes":
            if type(person_object) == Fellow:
                living_space = self.random_room_select(
                    "living_space")
                if living_space == "No available living space":
                    cprint("No available living space", "red")
                    self.rooms["living_space_waiting_list"].append(
                        person_object)
                    self.people["all_people"].append(person_object)
                    cprint("{0} {1} id {2} has been put to living space "
                           "waiting list".format(
                               person_object.first_name,
                               person_object.last_name,
                               person_object.person_id), "white")
                else:
                    # allocated living space
                    (self.rooms["living_space"][living_space].
                     append(person_object))
                    self.people["all_people"].append(person_object)

                    cprint("{} {} id {} allocated to {} (living space)".format(
                        person_object.first_name, person_object.last_name,
                        person_object.person_id, living_space.name), "blue")
            else:
                cprint("Staff not entitled to living space.", "red")

    def random_room_select(self, room_type):
        """To randomly allocate rooms."""
        if room_type == "office":
            select_office = (lambda offices:
                             random.choice(offices) if len(
                                 offices) > 0 else "No available office space"
                             )
            allocated_office = select_office(self.list_of_available_rooms("o"))
            return allocated_office
        else:
            select_living_space = (lambda living_spaces:
                                   random.choice(living_spaces) if len(
                                       living_spaces) > 0
                                   else "No available living space"
                                   )
            allocated_living_space = select_living_space(
                self.list_of_available_rooms("l"))
            return allocated_living_space

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

    def populate_people(self, people):
        """To populate people dictionary during load state database."""
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

    def populate_rooms(self, rooms):
        """To populate rooms dictionary during load state database."""
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

    def populate_allocated_people(self, allocated_people):
        """To populate people allocated to rooms."""
        for person in allocated_people:
            current_room = [room for room in self.rooms["all_rooms"]
                            if room.room_id == person[2]][0]
            person_object = self.get_person_object_given_person_id(person[1])
            if type(current_room) == Office:
                self.rooms["office"][current_room].append(person_object)
            elif type(current_room) == LivingSpace:
                self.rooms["living_space"][current_room].append(person_object)

    def populate_unallocated_people(self, unallocated_people):
        """To populate unallocated people."""
        for person in unallocated_people:
            if person[1] == "office":
                person_object = (self.get_person_object_given_person_id(
                    person[2]))
                self.rooms["office_waiting_list"].append(person_object)
            elif person[1] == "living_space":
                person_object = (self.get_person_object_given_person_id(
                    person[2]))
                self.rooms["living_space_waiting_list"].append(person_object)

    def list_of_available_rooms(self, room_type):
        """To list all available rooms slots."""
        if room_type in ["Office", "office", "O", "o"]:
            # get all office objects with space < 6
            return [room for room in list(self.rooms["office"].keys()) if
                    len(self.rooms["office"][room]) < 6]
        elif room_type in ["Living", "living", "L", "l"]:
            # get all living space objects with space < 4
            return [room for room in list(self.rooms["living_space"].keys()) if
                    len(self.rooms["living_space"][room]) < 4]

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

    def print_office_allocations(self):
        """To print out all people allocated to rooms."""
        list_of_offices = list(self.rooms["office"].keys())
        if len(list_of_offices) > 0:
            for office in list_of_offices:
                if len(self.rooms["office"][office]) > 0:
                    print("{} - (Office)".format(office.name))
                    print("---------------------------")
                    persons_in_office = []
                    for person in self.rooms["office"][office]:
                        name = person.first_name + " " + person.last_name
                        persons_in_office.append(name)
                    cprint(', '.join(persons_in_office), "red")
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
                    print("{} - (living space)".format(living_space.name))
                    print("---------------------------")
                    persons_in_living_space = []
                    for person in self.rooms["living_space"][living_space]:
                        name = person.first_name + " " + person.last_name
                        persons_in_living_space.append(name)
                    cprint(', '.join(persons_in_living_space), "red")
                else:
                    cprint("{0} - has no occupants currently\n".
                           format(living_space.name), "red")
        else:
            cprint("No living space exist", "red")

    def dump_unallocated_to_file(self, text_file, office, living_space):
        """To dump unallocated people to text file."""
        with open(text_file, 'w') as output:
            if office:
                output.write("People lacking offices\n")
                for i in office:
                    output.write("{0}\n".format(
                        i.first_name + " " + i.last_name))
            else:
                cprint("There are no office unallocations.", "white")
            if living_space:
                output.write("People lacking living spaces\n")
                for i in living_space:
                    output.write("{0}\n".format(
                        i.first_name + " " + i.last_name))
            else:
                cprint("There are no living space"
                       " unallocations.", "white")

    def list_of_persons_allocated_to_offices(self):
        """To return a list of persons allocated to office spaces."""
        persons_in_offices = []
        for key, value in self.rooms["office"].items():
            if len(value) > 0:
                persons_in_offices.extend(value)
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
            if room_name == room.name:
                result = room
        if result:
            return result
        else:
            return "room name does not exist"

    def dump_allocated_to_text_file(self, text_file, list_of_offices,
                                    list_of_living_spaces):
        """A helper method to dump allocations to text file."""
        with open(text_file, 'w') as output:
            if list_of_offices:
                output.write("People allocated to offices\n")
                for i in list_of_offices:
                    output.write("{0}\n\n".format(i.name))
                    output.write("---------------------------"
                                 "--------------\n")
                    persons_in_office = []
                    for person in self.rooms["office"][i]:
                        name = (person.first_name + " " +
                                person.last_name)
                        persons_in_office.append(name)
                    output.write("{0}\n".format(', '.join(
                        persons_in_office)))
                cprint("Office allocations successfully dumped to {}.".format(
                    text_file), "white")
            else:
                cprint("There are no office allocations.")

            if list_of_living_spaces:
                output.write("Fellows allocated to living spaces\n")
                for i in list_of_living_spaces:
                    output.write("{0}\n\n".format(i.name))
                    output.write("-------------------------"
                                 "----------------\n")
                    persons_in_living_spaces = []
                    for person in self.rooms["living_space"][i]:
                        name = (person.first_name + " "
                                + person.last_name)
                        persons_in_living_spaces.append(name)
                    output.write("{0}\n".format(', '.join(
                        persons_in_living_spaces)))
                cprint("Living space allocations successfully dumped to {}.".
                       format(text_file), "white")
            else:
                cprint("There are no living space allocations.")
