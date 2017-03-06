from amity import Amity
import unittest


class TestAmity(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()
        # office and its allocations
        for i in ["Narnia", "Hogwarts", "Platform"]:
            self.amity.rooms["office"][i] = []

    def test_create_room_adds_rooms_successfully(self):
        # check the current number of rooms
        old_number_of_offices = len(self.amity.rooms["office"])
        self.assertEqual(old_number_of_offices, 3)
        # list of new office to be added
        new_office = ["Hogwarts"]
        self.assertEqual(self.amity.create_room(new_office, "O"), "Room successfully added")
        # confirm that extra room has been added
        new_number_of_offices = self.amity.rooms["office"]
        # expected - increase by 1
        self.assertEqual((new_number_of_offices - new_number_of_offices), 1)

    def test_create_room_does_not_create_duplicate_rooms(self):
        # create rooom
        self.assertEqual(self.amity.create_room(["Hogwarts"], "O"), "Room successfully added")
        # assert that ONE office has been added
        self.assertTrue(len(self.amity.rooms["office"]) == 1)
        # try creating a room with the same name
        self.assertEqual(self.amity.create_room(["Hogwarts"], "O"), "Cannot create duplocate rooms.")
        # confirm duplicate not added
        self.assertTrue(len(self.amity.rooms["office"]) == 1)

    def test_create_room_does_not_create_office_and_living_space_with_same_name(self):
        # create an office
        self.assertEqual(self.amity.create_room(["Hogwarts"], "O"), "Room successfully added")
        # create living space with same name as office
        self.assertEqual(self.amity.create_room(["Hogwarts"], "L"), "Room successfully added")
        # confirm that living space has not been added
        self.assertTrue(len(self.amity.rooms["living_space"]) == 0)

    def test_add_person_creates_person_successfully(self):
        # get number of people(fellows)
        fellows_before = len(self.amity.people["fellows"]["no_accomodation"])
        # create a person(fellow)
        self.assertEqual(self.amity.add_person("Dave", "F", "N"), "Person successfully added")
        # check number of fellows after
        fellows_after = len(self.amity.people["fellow"]["no_accomodation"])
        # check if added fellow is reflected in the list
        self.assertEqual((fellows_before + 1), fellows_after)

if __name__== '__main__':
    unittest.main()
