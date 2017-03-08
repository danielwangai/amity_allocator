from amity import Amity
from fellow import Fellow
from staff import Staff
from office import Office
from living_space import LivingSpace

import unittest


class TestAmity(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()
        # office and its allocations
        for i in ["Narnia", "Krypton", "Platform"]:
            self.new_office = Office(i)
            self.amity.rooms["office"][self.new_office] = []
        # prepulate living spaces
        for i in ["Python", "Scala", "Go"]:
            # (self.amity.rooms["living_space"]).append(i)
            self.new_living_space = LivingSpace(i)
            self.amity.rooms["living_space"][self.new_living_space] = []

    def test_create_room_adds_rooms_successfully(self):
        # list of new room to be added
        new_office = ["Hogwarts"]
        # assert that new room is not is list of all rooms
        self.assertFalse(new_office[0] in self.amity.rooms["all_rooms"])
        # add room
        self.assertEqual(self.amity.create_room(new_office, "o"), "Room successfully added")
        # assert that new room was added
        self.assertTrue(new_office[0] in self.amity.get_all_rooms(self.amity.rooms["all_rooms"]))

    def test_create_room_does_not_create_duplicate_rooms(self):
        # new room to be created
        new_office = "Valhalla"
        # assert that new room is not is list of all rooms
        self.assertFalse(new_office in self.amity.rooms["all_rooms"])
        # add room
        self.assertEqual(self.amity.create_room([new_office], "o"), "Room successfully added")
        # assert that new room was added
        self.assertTrue(new_office in self.amity.get_all_rooms(self.amity.rooms["all_rooms"]))
        # try adding the same room again
        self.assertEqual(self.amity.create_room([new_office], "o"), "Cannot create room since a room with the same naem exists.")
        # confirm that the room has not been added again
        self.assertIn(new_office, self.amity.get_all_rooms(self.amity.rooms["all_rooms"]))

    def test_create_room_does_not_create_office_and_living_space_with_same_name(self):
        # new room to create
        new_room = "Oculus"
        # assert that new room is not is list of all rooms
        self.assertFalse(new_room in [i.name for i in list(self.amity.rooms["office"].keys())])
        # add room
        self.assertEqual(self.amity.create_room([new_room], "o"), "Room successfully added")
        # assert that new office was added
        self.assertIn(new_room, [i.name for i in list(self.amity.rooms["office"].keys())])
        # try creating an office with the same name
        self.assertEqual(self.amity.create_room([new_room], "l"), "Cannot create room since a room with the same naem exists.")

        self.assertNotIn(new_room, [i.name for i in list(self.amity.rooms["living_space"].keys())])


    def test_add_person_creates_person_successfully(self):
        # new person
        name = "Dan"
        # get initial number of people
        length = len(self.amity.people["all_people"])
        # create a person
        self.assertEqual(self.amity.add_person("Dave", "F", "N"), "Person successfully added")
        # get the new number of people
        new_length = len(self.amity.people["all_people"])
        # test that person is added
        self.assertEqual((length + 1), new_length)

    def test_load_people_file_does_not_exist(self):
        file_path = '/path/to/no where'
        self.assertEqual(self.amity.load_people(file_path), 'File doesnt exist')

    def test_load_people_loads_people_successfully(self):
        # assign file path
        file_path = 'files/test_people.txt'
        # get people count
        fellows_before = len(self.amity.people["fellows"])
        # load people from file
        self.assertEqual(self.amity.load_people(file_path), 'People loaded successfully.')
        # get count after loading people
        fellows_after = len(self.amity.people["fellow"]["no_accomodation"])
        # assert for increment
        self.assertEqual((fellows_after - fellows_after), 2)

    def test_print_room_does_not_print_inexistent_room(self):
        # name of inexistent room
        room_name = "asdbakdsjs"
        self.assertEqual(self.amity.print_room(room_name), "The room {0} does not exist".format(room_name))

if __name__== '__main__':
    unittest.main()
