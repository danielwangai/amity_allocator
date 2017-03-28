"""Tests for amity."""
import os.path
import unittest

from .amity import Amity


class TestAmity(unittest.TestCase):
    """Tests for amity.

    To tests amity methods.
    """

    def setUp(self):
        """To set up test variables."""
        self.amity = Amity()

    def test_create_room_adds_offices_successfully(self):
        """To test if create_room adds office(s) successfully."""
        self.free_variables()
        # list of new room to be added
        new_office = "Hogwarts"
        # assert that new room is not is list of all rooms
        self.assertNotIn(new_office, self.amity.get_all_rooms(
            self.amity.rooms["all_rooms"]))
        # print(self.amity.get_all_rooms(self.amity.rooms["all_rooms"]))
        # add room
        self.amity.create_room("office", [new_office])
        # assert that new room was added
        (self.assertIn(new_office,
                       self.amity.get_all_rooms(
                           self.amity.rooms["all_rooms"])))

    def test_create_room_adds_living_space_successfully(self):
        """To test if create_room adds living space(s) successfully."""
        self.free_variables()
        # list of new room to be added
        new_living_space = "PHP"
        # assert that new room is not is list of all rooms
        self.assertNotIn(new_living_space, self.amity.get_all_rooms(
            self.amity.rooms["all_rooms"]))
        # print(self.amity.get_all_rooms(self.amity.rooms["all_rooms"]))
        # add room
        self.amity.create_room("living_space", [new_living_space])
        # assert that new room was added
        self.assertIn(new_living_space, self.amity.get_all_rooms(
            self.amity.rooms["all_rooms"]))

    def test_create_room_does_not_create_duplicate_rooms(self):
        """To test if create_room adds rejects room duplication."""
        self.free_variables()
        # new room to be created
        new_office = "Valhalla"
        # assert that new room is not is list of all rooms
        self.assertNotIn(new_office, self.amity.get_all_rooms(
            self.amity.rooms["all_rooms"]))
        # # add room
        self.amity.create_room("office", [new_office])
        original_number_of_rooms = len(self.amity.rooms["all_rooms"])
        # assert that new room was added
        self.assertIn(new_office, self.amity.get_all_rooms(
            self.amity.rooms["all_rooms"]))
        # # try adding the same room again
        self.amity.create_room("office", [new_office])
        number_of_rooms_after_duplication_attempt = len(
            self.amity.rooms["all_rooms"])

        self.assertEqual(original_number_of_rooms,
                         number_of_rooms_after_duplication_attempt)

    def test_create_room_office_and_living_space_with_same_name(self):
        """To test room duplication.

        create_room rejects office and living spaces with same name.
        """
        self.free_variables()
        # new room to create
        new_office = "Oculus"
        # # assert that new room is not is list of all rooms
        self.assertFalse(new_office in [i.name for i in list(
            self.amity.rooms["office"].keys())])
        # add room
        self.amity.create_room("office", [new_office])
        # assert that new room was added
        self.assertIn(new_office, self.amity.get_all_rooms(
            self.amity.rooms["all_rooms"]))
        # assert new room not is living space list
        new_living_space = "Oculus"
        # assert that new room is not is list of all rooms
        self.assertFalse(new_living_space in [i.name for i in list(
            self.amity.rooms["living_space"].keys())])
        # attempt add
        self.amity.create_room("living_space", [new_office])
        # confirm that oculus was is not in the list of living spaces
        self.assertNotIn(new_living_space, [i.name for i in list(
            self.amity.rooms["living_space"].keys())])

    def test_add_person_creates_fellow_successfully(self):
        """To test if add_person adds fellow successfully."""
        # get initial number of people
        initial_number_of_fellows = len(self.amity.people["fellows"])
        # create a person
        self.amity.add_person("Fellow", "Daniel", "Maina", "Y")
        # get the new number of people
        new_number_of_fellows = len(self.amity.people["fellows"])
        # test that person is added
        self.assertEqual((initial_number_of_fellows + 1),
                         new_number_of_fellows)

    def test_add_person_creates_staff_successfully(self):
        """To test if add_person adds staff successfully."""
        # get initial number of people
        initial_number_of_fellows = len(self.amity.people["staff"])
        # create a person
        self.amity.add_person("Staff", "David", "Ngugi", "N")
        # get the new number of people
        new_number_of_fellows = len(self.amity.people["staff"])
        # test that person is added
        self.assertEqual((initial_number_of_fellows + 1),
                         new_number_of_fellows)

    def test_add_person_allocates_fellow_to_office(self):
        """To test if add_person allocates fellow to office."""
        # add fellow
        self.amity.create_room("office", "Tent")
        self.amity.add_person("Fellow", "Daniel", "Maina")
        all_people = self.amity.people["all_people"]
        # get object of added fellow
        new_fellow_object = all_people[-1]
        # assert that the fellow object is allocated an office
        self.assertIn(new_fellow_object,
                      self.amity.list_of_persons_allocated_to_offices())

    def test_add_person_allocates_staff_to_office(self):
        """To test if add_person allocates staff to office."""
        all_people = self.amity.people["all_people"]
        # add staff
        self.amity.create_room("office", "another-room")
        self.amity.add_person("Staff", "Daniel", "Maina", "N")
        # get object of added staff
        new_fellow_object = all_people[-1]
        # assert that the staff object is allocated an office
        self.assertIn(new_fellow_object,
                      self.amity.list_of_persons_allocated_to_offices())

    def test_add_person_allocates_fellow_to_living_space(self):
        """To test if add_person allocates fellow to living_space."""
        all_people = self.amity.people["all_people"]
        # add fellow
        self.amity.add_person("Fellow", "Daniel", "Maina", "Y")
        # get object of added fellow
        new_fellow_object = all_people[-1]
        # assert that the fellow object is allocated an office
        self.assertIn(new_fellow_object,
                      self.amity.list_of_fellows_allocated_to_living_spaces())

    def test_add_person_adds_people_to_waiting_list_if_office_is_full(self):
        """To test if add_person caters for excess people.

        Adds fellow/staff to office waiting list when offices are full.
        """
        # get office
        office = list(self.amity.rooms["office"].keys())[0]
        list_of_persons = [
            ["Fellow", "Daniel", "Maina", "N"],
            ["Fellow", "Dan", "Wachira", "N"],
            ["Fellow", "Larry", "W", "N"],
            ["Staff", "Fellow", "David", "White", "N"],
            ["Staff", "Xie", "Yuen", "N"],
            ["Staff", "Stella", "Storl", "N"]
        ]
        for person in list_of_persons:
            self.amity.add_person(person[0], person[1], person[2], person[3])
        self.amity.add_person("Fellow", "Dan", "K", "N")
        # get last person to be added
        last_person = self.amity.people["all_people"][-1]
        # confirm that new person has not been added to office
        self.assertNotIn(last_person, self.amity.rooms["office"][office])
        # check that the last person is in office waiting list
        self.assertIn(last_person, self.amity.rooms["office_waiting_list"])

    def test_add_person_set_fellow_to_waiting_list_if_living_spaces_full(self):
        """To test if add_person caters for excess people.

        Adds fellow to living space waiting list when offices are full.
        """
        # get living space
        living_space = list(self.amity.rooms["living_space"].keys())[0]
        list_of_fellows = [
            ["Fellow", "Daniel", "Maina", "Y"],
            ["Fellow", "Dan", "Wachira", "Y"],
            ["Fellow", "Larry", "W", "Y"],
            ["Fellow", "Fellow", "David", "White", "Y"],
            ["Fellow", "Xie", "Yuen", "Y"],
            ["Fellow", "Stella", "Storl", "Y"]
        ]
        for person in list_of_fellows:
            self.amity.add_person(person[0], person[1], person[2], person[3])
        # attempt to add another fellow
        self.amity.add_person("Fellow", "Dan", "K", "Y")
        last_person = self.amity.people["all_people"][-1]
        # confirm that new person has not been added to office
        self.assertNotIn(last_person,
                         self.amity.rooms["living_space"][living_space])
        # check that the last person
        self.assertIn(last_person,
                      self.amity.rooms["living_space_waiting_list"])

    def test_add_person_allocate_fellow_to_livingspace_when_office_full(self):
        """To allocate fellow to living space even when offices are full."""
        self.free_variables()
        self.amity.create_room("office", ["Oculus"])
        # get office
        office = list(self.amity.rooms["office"].keys())[-1]

        list_of_fellows = [
            ["Fellow", "Daniel", "Maina", "N"],
            ["Fellow", "Dan", "Wachira", "N"],
            ["Fellow", "Larry", "W", "N"],
            ["Fellow", "Fellow", "David", "White", "N"],
            ["Fellow", "Xie", "Yuen", "N"],
            ["Fellow", "Stella", "Storl", "N"]
        ]
        # add people to offices
        for person in list_of_fellows:
            self.amity.add_person(person[0], person[1], person[2], person[3])
        self.amity.create_room("living_space", ["Python"])
        # get living_space
        living_space = list(self.amity.rooms["living_space"].keys())[0]
        # add another person - expected to miss office slot
        self.amity.add_person("Fellow", "Dan", "K", "Y")
        last_person = self.amity.people["all_people"][-1]
        # confirm that new person has not been added to office
        self.assertNotIn(last_person, self.amity.rooms["office"][office])
        # confirm that new person has not been added to office
        self.assertIn(last_person,
                      self.amity.rooms["living_space"][living_space])

    def test_load_people_file_does_not_exist(self):
        """To test that method rejects loading people if file doesnt exist."""
        self.free_variables()
        file_path = '/path/to/no where'
        self.assertEqual(self.amity.load_people(file_path),
                         'File does not exist.')

    def test_load_people_loads_people_successfully(self):
        """To test that loads people successfully."""
        #     # assign file path
        self.free_variables()
        file_path = 'text.txt'
        people_before = len(self.amity.people["all_people"])
        # load people from file
        self.amity.load_people(file_path)
        # get count after loading people
        people_after = len(self.amity.people["all_people"])
        # assert for increment
        self.assertTrue(people_before < people_after)

    def test_reallocate_person_reallocates_to_office_successfully(self):
        """To test that method reallocates person successfuly."""
        self.free_variables()
        # get initial number of people
        length = len(self.amity.people["fellows"])
        self.amity.create_room("office", ["Python"])
        # create a person
        self.amity.add_person("Fellow", "Daniel", "Maina", "N")
        # get the new number of people
        new_length = len(self.amity.people["fellows"])
        # test that person is added
        self.assertEqual((length + 1), new_length)
        # get person_id
        person_object = self.amity.people["all_people"][0]
        # get current_room
        current_room = list(self.amity.rooms["office"].keys())[0]
        # assert that person is in room
        self.assertIn(person_object, self.amity.rooms["office"][current_room])
        # get new_room
        self.amity.create_room("office", ["Camelot"])
        new_room_object = (self.amity.
                           get_room_object_from_room_name_for_available_rooms(
                               "Camelot"))
        self.amity.reallocate_person(person_object.person_id, "Camelot")
        self.assertNotIn(person_object,
                         self.amity.rooms["office"][current_room])
        self.assertIn(person_object,
                      self.amity.rooms["office"][new_room_object])

    def test_reallocate_person_reallocates_to_living_space_successfully(self):
        """To test that method reallocates to living space successfuly."""
        self.free_variables()
        # create person
        # get initial number of people
        length = len(self.amity.people["fellows"])
        self.amity.create_room("living_space", ["Python"])
        # create a person
        self.amity.add_person("Fellow", "David", "Ngugi", "Y")
        # get the new number of people
        new_length = len(self.amity.people["fellows"])
        # test that person is added
        self.assertEqual((length + 1), new_length)
        # get person_id
        person_object = self.amity.people["all_people"][0]
        # get current_room
        current_room = list(self.amity.rooms["living_space"].keys())[0]
        # assert that person is in room
        self.assertIn(person_object,
                      self.amity.rooms["living_space"][current_room])
        # get new_room
        self.amity.create_room("living_space", ["Ruby"])
        new_room_object = (self.amity.
                           get_room_object_from_room_name_for_available_rooms(
                               "Ruby"))
        self.amity.reallocate_person(person_object.person_id, "Ruby")
        self.assertNotIn(person_object,
                         self.amity.rooms["living_space"][current_room])
        self.assertIn(person_object,
                      self.amity.rooms["living_space"][new_room_object])

    def test_reallocate_person_reject_move_to_office_with_wrong_personid(self):
        """To test that method rejects move to office given wrong person id."""
        self.free_variables()
        person_id = 312312312
        self.amity.create_room("office", ["Hogwarts"])
        new_room = list(self.amity.rooms["office"].keys())[0]
        self.assertEqual(self.amity.reallocate_person(
            person_id, new_room.name), "person id does not exist.")

    def test_reallocate_person_reject_move_to_living_with_wrong_personid(self):
        """To test that method rejects reallocation to living space.

        given wrong person id.
        """
        self.free_variables()
        person_id = 312312312
        self.amity.create_room("living_space", ["Pythons"])
        new_room = list(self.amity.rooms["living_space"].keys())[0]
        self.assertEqual(self.amity.reallocate_person(person_id,
                                                      new_room.name),
                         "person id does not exist.")

    def test_reallocate_person_reject_move_to_office_given_bad_roomname(self):
        """To test that method rejects reallocation given bad new room name."""
        self.free_variables()
        new_room_name = "I do not exist"
        self.amity.create_room("office", ["Hogwarts"])
        self.amity.add_person("Fellow", "Daniel", "Maina", "N")
        # get person_id
        person_object = self.amity.people["all_people"][-1]

        self.assertEqual(self.amity.reallocate_person
                         (person_object.person_id, new_room_name),
                         "Room does not exist.")

    def test_reallocate_person_reject_move_to_living_given_bad_roomname(self):
        """To test that method rejects move to living space.

        given wrong room name.
        """
        self.free_variables()
        new_room_name = "I do not exist"
        self.amity.create_room("office", ["Hogwarts"])
        self.amity.add_person("Fellow", "Daniel", "Maina", "Y")
        # get person_id
        person_object = self.amity.people["all_people"][-1]

        self.assertEqual(self.amity.reallocate_person(
            person_object.person_id, new_room_name),
            "room name does not exist.")

    def test_reallocate_person_does_not_reallocate_staff_to_living_space(self):
        """To test that method does not reallocate staff to living space."""
        self.free_variables()
        self.amity.add_person("Staff", "David", "Ngugi", "Y")
        person_object = self.amity.people["all_people"][-1]
        # reallocate to living space
        self.amity.create_room("living_space", ["Django"])
        self.assertEqual(self.amity.reallocate_person(
            person_object.person_id, "Django"),
            "Cannot reallocate staff to living space.")

    def test_reallocate_person_does_not_reallocate_staff_to_same_office(self):
        """To test that method does not reallocate staff to same office."""
        self.free_variables()
        self.amity.create_room("office", ["Cafeteria"])
        self.amity.add_person("Staff", "David", "Ngugi", "Y")
        person_object = self.amity.people["all_people"][-1]
        # reallocate to living space
        self.assertEqual(self.amity.reallocate_person(
            person_object.person_id, "Cafeteria"),
            "Cannot reallocate to same room.")

    def test_reallocate_person_does_not_reallocate_fellow_to_same_office(self):
        """To test that method does not reallocate fellow to same office."""
        self.free_variables()
        self.amity.create_room("office", ["Cafeteria"])
        self.amity.add_person("Fellow", "David", "Ngugi", "Y")
        person_object = self.amity.people["all_people"][-1]
        # reallocate to living space
        self.assertEqual(self.amity.reallocate_person(
            person_object.person_id, "Cafeteria"),
            "Cannot reallocate to same room.")

    def test_reallocate_person_wont_realocate_fellow_to_same_livingspace(self):
        """To test that method wont reallocate fellow to same livingspace."""
        self.free_variables()
        self.amity.create_room("living_space", ["living1"])
        self.amity.add_person("Fellow", "David", "Ngugi", "Y")
        person_object = self.amity.people["all_people"][-1]
        # reallocate to living space
        self.assertEqual(self.amity.reallocate_person(
            person_object.person_id, "living1"),
            "Cannot reallocate to same room.")

    def test_print_room_does_not_print_inexistent_room(self):
        """To test if method prints rooms and occupants successfully."""
        self.free_variables()
        room_name = "I don't exist!!!"
        self.assertEqual(self.amity.print_room(room_name),
                         "Room {0} does not exist.".format(room_name))

    def test_print_room_does_not_print_when_given_wrong_name(self):
        """To test if method prints invalid message given wrong name."""
        self.free_variables()
        # get room
        room = "I do not exist"
        self.assertEqual(self.amity.print_room(room),
                         "Room {0} does not exist.".format(room))

    def test_print_room_prints_error_for_office_with_no_occupants(self):
        """To test if method prints error message for empty office."""
        self.free_variables()
        self.amity.create_room("office", ["Narnia"])
        (self.assertEqual(self.amity.print_room("Narnia"),
                          "There are no occupants in the {} currently.".format(
            "Narnia")))

    def test_print_room_prints_error_for_livingspace_with_no_occupants(self):
        """To test if method prints error message for empty living space."""
        self.free_variables()
        self.amity.create_room("living_space", ["Django"])
        (self.assertEqual(self.amity.print_room("Django"),
                          "There are no occupants in the room currently."))

    def test_print_room_prints_existing_occupants_in_office(self):
        """To test if method prints office occupants."""
        self.free_variables()
        self.amity.create_room("office", ["Narnia"])
        self.amity.add_person("Fellow", "Daniel", "Maina", "N")
        (self.assertEqual(self.amity.print_room("Narnia"),
                          "Office printed successfuly."))

    def test_print_room_prints_existing_occupants_in_living_space(self):
        """To test if method prints office occupants."""
        self.free_variables()
        self.amity.create_room("living_space", ["Python"])
        self.amity.add_person("Fellow", "Daniel", "Maina", "Y")
        (self.assertEqual(self.amity.print_room("Python"),
                          "Living Space printed successfuly."))

    def test_print_allocations_prints_successfully_to_screen(self):
        """To test if method prints allocations to screen."""
        self.free_variables()
        self.amity.create_room("office", ["Narnia"])
        self.amity.create_room("living_space", ["Python"])
        # create people
        self.amity.add_person("Fellow", "Daniel", "Maina1", "Y")
        self.amity.add_person("Fellow", "Daniel", "Maina2", "Y")
        self.amity.add_person("Fellow", "Daniel", "Maina3", "Y")

        self.assertEqual(self.amity.print_allocations(),
                         "Allocations successfully printed to screen.")

    def test_print_allocations_prints_successfully_dumps_to_file(self):
        """To test if method prints allocations to screen."""
        self.free_variables()
        self.amity.create_room("office", ["Narnia"])
        self.amity.create_room("living_space", ["Python"])
        # create people
        self.assertEqual(self.amity.print_allocations("test_file.txt"),
                         "Successfully dumped to file.")

    def test_print_unallocated_prints_successfully_to_screen(self):
        """To test if method prints unallocated people to screen."""
        self.free_variables()
        # create people without existing rooms
        self.amity.add_person("Fellow", "Daniel", "Maina1", "Y")
        self.amity.add_person("Fellow", "Daniel", "Maina2", "Y")
        self.amity.add_person("Fellow", "Daniel", "Maina3", "Y")
        self.assertEqual(self.amity.print_unallocated(),
                         "Successfully printed unallocated people to screen.")

    def test_print_unallocated_dumps_empty_file_if_no_unallocations(self):
        """To test if method dumps empty file when no unallocations."""
        self.free_variables()
        # create people without existing rooms
        self.amity.add_person("Fellow", "Daniel", "Maina1", "Y")
        self.amity.add_person("Fellow", "Daniel", "Maina2", "Y")
        self.amity.add_person("Fellow", "Daniel", "Maina3", "Y")
        self.assertEqual(self.amity.print_unallocated("test_file.txt"),
                         "Successfully dumped unallocated people to file.")

    def test_print_unallocated_dumps_to_file_if_unallocations(self):
        """To test if method dumps empty file when no unallocations."""
        self.free_variables()
        self.amity.add_person("Fellow", "Daniel", "Maina", "Y")
        self.amity.add_person("Fellow", "Daniel", "Maina", "Y")
        self.amity.add_person("Fellow", "Daniel", "Maina", "Y")
        self.amity.add_person("Fellow", "Daniel", "Maina", "Y")
        self.amity.add_person("Fellow", "Daniel", "Maina", "Y")
        self.amity.add_person("Fellow", "Daniel", "Maina", "Y")

        self.assertEqual(self.amity.print_unallocated("test_file.txt"),
                         "Successfully dumped unallocated people to file.")

    def test_load_state_prints_error_if_empty_db(self):
        """To test if method prints error message if empty db."""
        self.free_variables()
        self.assertEqual(self.amity.load_state("no_db.db"),
                         "No data in {}".format("no_db.db"))

    def test_load_state_prints_when_db_not_empty(self):
        """To test if method retreives data from db."""
        self.free_variables()
        self.assertEqual(self.amity.load_state("amity.db"),
                         "Data load from {} success".format("amity.db"))

    def test_load_people_rejects_load_if_file_not_found(self):
        """To test load_people rejects loading people if file not found."""
        self.free_variables()
        self.assertEqual(self.amity.load_people("i_am_not_here.txt"),
                         "File does not exist.")

    def test_load_people_loads_successfully_from_file(self):
        """To test that load_people loads successfully."""
        self.free_variables()
        self.assertEqual(self.amity.load_people("text.txt"),
                         "File found")

    def free_variables(self):
        """To free variables for fresh use in other tests."""
        self.amity.rooms["office"] = {}
        self.amity.rooms["living_space"] = {}
        self.amity.rooms["all_rooms"] = []
        self.amity.people["all_people"] = []
        self.amity.people["fellows"] = []
        self.amity.people["staff"] = []


if __name__ == '__main__':
    unittest.main()
