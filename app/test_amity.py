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



if __name__== '__main__':
    unittest.main()
