from amity import Amity
import unittest


class TestAmity(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()

    def test_create_room_adds_rooms_successfully(self):
        offices = ["Hogwarts", "Narnia", "Midgar"]
        self.assertEqual(self.amity.create_room(offices, "O"), "Room successfully added")
        # rooms are added to the rooms office dictionary
        self.assertTrue(len(self.amity.rooms["office"]), 3)


    def test_create_room_does_not_create_duplicate_rooms(self):
        # create rooom
        self.assertEqual(self.amity.create_room(["Hogwarts"], "O"), "Room successfully added")
        # assert that ONE office has been added
        self.assertTrue(len(self.amity.rooms["office"]) == 1)
        # try creating a room with the same name
        self.assertEqual(self.amity.create_room(["Hogwarts"], "O"), "Cannot create duplocate rooms.")
        # confirm duplicate not added
        self.assertTrue(len(self.amity.rooms["office"]) == 1)

if __name__== '__main__':
    unittest.main()
