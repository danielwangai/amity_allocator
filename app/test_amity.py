from amity import Amity
import unittest


class TestAmity(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()
        # office and its allocations
        for i in ["Narnia", "Hogwarts", "Platform"]:
            (self.amity.rooms["office"]).append(i)
        # prepulate living spaces
        for i in ["Python", "Scala", "Go"]:
            (self.amity.rooms["living_space"]).append(i)

    def test_create_room_adds_rooms_successfully(self):
        # check the current number of rooms
        old_number_of_offices = len(self.amity.rooms["office"])
        self.assertEqual(old_number_of_offices, 3)
        # list of new office to be added
        new_office = ["Hogwarts"]
        self.assertEqual(self.amity.create_room(new_office, "O"), "Room successfully added")
        # get new number of rooms
        new_number_of_offices = self.amity.rooms["office"]
        # expected - increase by 1
        self.assertEqual((new_number_of_offices - new_number_of_offices), 1)

    def test_create_room_does_not_create_duplicate_rooms(self):
        # check current number of rooms
        old_number_of_offices = len(self.amity.rooms["office"])
        # create rooom
        self.assertEqual(self.amity.create_room(["Hogwarts"], "O"), "Cannot create room since a room with the same naem exists.")
        # get new number of rooms
        new_number_of_offices = self.amity.rooms["office"]
        # expected - old_number_of_rooms = new_number_of_rooms
        self.assertEqual(new_number_of_offices, new_number_of_offices)

    def test_create_room_does_not_create_office_and_living_space_with_same_name(self):
        # check current number of offices
        old_number_of_offices = len(self.amity.rooms["office"])
        # create an office
        self.assertEqual(self.amity.create_room(["Hogwarts"], "O"), "Room successfully added")
        # get new number of offices
        new_number_of_offices = self.amity.rooms["office"]
        # confirm addition of new office
        self.assertEqual((new_number_of_offices - old_number_of_offices), 1)

        # check current number of offices
        old_number_of_living_spaces = len(self.amity.rooms["living_space"])
        # create living space with same name as office
        self.assertEqual(self.amity.create_room(["Hogwarts"], "L"), "Cannot add living space. An office with same name exists.")
        # new number of living spaces
        new_number_of_living_spaces = self.amity.rooms["living_space"]
        # confirm that living space has not been added
        self.assertTrue((new_number_of_living_spaces - old_number_of_living_spaces) == 0)

    def test_add_person_creates_person_successfully(self):
        # get number of people(fellows)
        fellows_before = len(self.amity.people["fellows"]["no_accomodation"])
        # create a person(fellow)
        self.assertEqual(self.amity.add_person("Dave", "F", "N"), "Person successfully added")
        # check number of fellows after
        fellows_after = len(self.amity.people["fellow"]["no_accomodation"])
        # check if added fellow is reflected in the list
        self.assertEqual((fellows_before + 1), fellows_after)

    def test_load_people_file_does_not_exist(self):
        file_path = '/path/to/no where'
        self.assertEqual(self.amity.load_people(file_path), 'File doesnt exist')

    def test_load_people_loads_people_successfully(self):
        # assign file path
        file_path = 'files/test_people.txt'
        # get people count
        fellows_before = len(self.amity.people["fellows"]["no_accomodation"])
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
