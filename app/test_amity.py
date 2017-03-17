import os.path
import unittest

from amity import Amity
from fellow import Fellow
from staff import Staff
from office import Office
from living_space import LivingSpace


class TestAmity(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()
        self.amity.create_room({"<name>": ["Narnia"], "office": True, "living_space": False})
        self.amity.create_room({"<name>": ["Python"], "office": False, "living_space": True})


    def test_create_room_adds_offices_successfully(self):
        # list of new room to be added
        new_office = ["Hogwarts"]
        # assert that new room is not is list of all rooms
        self.assertNotIn(new_office[0], self.amity.get_all_rooms(self.amity.rooms["all_rooms"]))
        # print(self.amity.get_all_rooms(self.amity.rooms["all_rooms"]))
        # add room
        self.amity.create_room({"<name>": new_office, "office": True, "living_space": False})
        # assert that new room was added
        self.assertIn(new_office[0], self.amity.get_all_rooms(self.amity.rooms["all_rooms"]))

    def test_create_room_adds_living_space_successfully(self):
        # list of new room to be added
        new_living_space = ["PHP"]
        # assert that new room is not is list of all rooms
        self.assertNotIn(new_living_space[0], self.amity.get_all_rooms(self.amity.rooms["all_rooms"]))
        # print(self.amity.get_all_rooms(self.amity.rooms["all_rooms"]))
        # add room
        self.amity.create_room({"<name>": new_living_space, "office": False, "living_space": True})
        # assert that new room was added
        self.assertIn(new_living_space[0], self.amity.get_all_rooms(self.amity.rooms["all_rooms"]))

    def test_create_room_does_not_create_duplicate_rooms(self):
        # new room to be created
        new_office = "Valhalla"
        # assert that new room is not is list of all rooms
        self.assertNotIn(new_office[0], self.amity.get_all_rooms(self.amity.rooms["all_rooms"]))
        # # add room
        self.amity.create_room({"<name>": [new_office], "office": True, "living_space": False})
        original_number_of_rooms = len(self.amity.rooms["all_rooms"])
        # assert that new room was added
        self.assertIn([new_office][0], self.amity.get_all_rooms(self.amity.rooms["all_rooms"]))
        # # try adding the same room again
        self.amity.create_room({"<name>": [new_office], "office": True, "living_space": False})
        number_of_rooms_after_duplication_attempt = len(self.amity.rooms["all_rooms"])

        self.assertEqual(original_number_of_rooms, number_of_rooms_after_duplication_attempt)

    def test_create_room_does_not_create_office_and_living_space_with_same_name(self):
        # new room to create
        new_room = "Oculus"
        # assert that new room is not is list of all rooms
        self.assertFalse(new_room in [i.name for i in list(self.amity.rooms["office"].keys())])
        # add room
        self.amity.create_room([new_room], "o")
        # assert that new office was added
        self.assertIn(new_room, [i.name for i in list(self.amity.rooms["office"].keys())])
        # try creating an office with the same name
        self.assertEqual(self.amity.create_room([new_room], "l"), "Cannot create room since a room with the same naem exists.")

        self.assertNotIn(new_room, [i.name for i in list(self.amity.rooms["living_space"].keys())])


    def test_add_person_creates_fellow_successfully(self):
        # new person
        name = "Dan"
        # get initial number of people
        length = len(self.amity.people["fellows"])
        # create a person
        self.amity.add_person("Dave", "F", "N")
        # get the new number of people
        new_length = len(self.amity.people["fellows"])
        # test that person is added
        self.assertEqual((length + 1), new_length)

    def test_add_person_creates_staff_successfully(self):
        # new person
        name = "James"
        # get initial number of people
        length = len(self.amity.people["staff"])
        # create a person
        self.amity.add_person("Dave", "S", "N")
        # get the new number of people
        new_length = len(self.amity.people["staff"])
        # test that person is added
        self.assertEqual((length + 1), new_length)

    def test_load_people_file_does_not_exist(self):
        file_path = '/path/to/no where'
        self.assertEqual(self.amity.load_people(file_path), 'File doesnt exist')

    def test_load_people_loads_people_successfully(self):
    #     # assign file path
        file_path = 'files/test_people.txt'
        # get people count
        fellows_before = len(self.amity.people["fellows"])
        # load people from file
        self.amity.load_people(file_path)
        # get count after loading people
        fellows_after = len(self.amity.people["fellows"])
        # assert for increment
        self.assertEqual((fellows_after - fellows_after), 2)

    def test_reallocate_person_reallocates_to_office_successfully(self):
        # create person
        name = "Dan"
        # get initial number of people
        length = len(self.amity.people["fellows"])
        # create a person
        self.amity.add_person("Dave", "F", "N")
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
        self.amity.create_room(["Camelot"], "o")
        new_room_object = self.amity.get_room_from_room_name("Camelot", "o")
        self.amity.reallocate_person(person_object.person_id, "o", "Camelot")
        self.assertNotIn(person_object, self.amity.rooms["office"][current_room])
        self.assertIn(person_object, self.amity.rooms["office"][new_room_object])

    def test_reallocate_person_reallocates_to_living_space_successfully(self):
        # create person
        name = "Dan"
        # get initial number of people
        length = len(self.amity.people["fellows"])
        # create a person
        self.amity.add_person("Dave", "F", "Y")
        # get the new number of people
        new_length = len(self.amity.people["fellows"])
        # test that person is added
        self.assertEqual((length + 1), new_length)
        # get person_id
        person_object = self.amity.people["all_people"][0]
        # get current_room
        current_room = list(self.amity.rooms["living_space"].keys())[0]
        # assert that person is in room
        self.assertIn(person_object, self.amity.rooms["living_space"][current_room])
        # get new_room
        self.amity.create_room(["Ruby"], "l")
        new_room_object = self.amity.get_room_from_room_name("Ruby", "l")
        self.amity.reallocate_person(person_object.person_id, "l", "Ruby")
        # self.assertNotIn(person_object, self.amity.rooms["living_space"][current_room])
        self.assertIn(person_object, self.amity.rooms["living_space"][new_room_object])

    def test_reallocate_person_rejects_reallocation_to_office_given_unexistent_person_id(self):
        person_id = 312312312

        new_room = list(self.amity.rooms["office"].keys())[0]
        original_number_of_occupants = len(self.amity.rooms["office"][new_room])
        # print(list(self.amity.rooms["office"].keys())[0])
        self.assertEqual(self.amity.reallocate_person(person_id, "o", new_room.name), "person with id {0} does not exist".format(person_id))
        number_after_adding_attempt = len(self.amity.rooms["office"][new_room])
        self.assertEqual(original_number_of_occupants, number_after_adding_attempt)

    def test_reallocate_person_rejects_reallocation_to_living_space_given_unexistent_person_id(self):
        person_id = 312312312

        new_room = list(self.amity.rooms["living_space"].keys())[0]
        original_number_of_occupants = len(self.amity.rooms["living_space"][new_room])
        # print(list(self.amity.rooms["living_space"].keys())[0])
        self.assertEqual(self.amity.reallocate_person(person_id, "l", new_room.name), "person with id {0} does not exist".format(person_id))
        number_after_adding_attempt = len(self.amity.rooms["living_space"][new_room])
        self.assertEqual(original_number_of_occupants, number_after_adding_attempt)

    def test_reallocate_person_rejects_reallocation_to_office_given_unexistent_room_name(self):
        new_room_name = "I do not exist"
        # create person
        name = "Dan"
        # get initial number of people
        length = len(self.amity.people["fellows"])
        # create a person
        self.amity.add_person("Dave", "F", "Y")
        # get the new number of people
        new_length = len(self.amity.people["fellows"])
        # test that person is added
        self.assertEqual((length + 1), new_length)
        # get person_id
        person_object = self.amity.people["all_people"][0]
        current_room = list(self.amity.rooms["office"].keys())[0]
        # get original number of room occupants
        original_number_of_occupants = len(self.amity.rooms["office"][current_room])
        print(original_number_of_occupants)
        # self.assertEqual(self.amity.reallocate_person(person_object.person_id, "o", new_room_name), "Room {0} does not exist".format(new_room_name))
        self.amity.reallocate_person(person_object.person_id, "o", new_room_name)
        number_after_adding_attempt = len(self.amity.rooms["office"][current_room])
        self.assertEqual(original_number_of_occupants, number_after_adding_attempt)

    def test_reallocate_person_rejects_reallocation_to_living_space_given_unexistent_room_name(self):
        new_room_name = "I do not exist"
        # create person
        name = "Dan"
        # get initial number of people
        length = len(self.amity.people["fellows"])
        # create a person
        self.amity.add_person("Dave", "F", "Y")
        # get the new number of people
        new_length = len(self.amity.people["fellows"])
        # test that person is added
        self.assertEqual((length + 1), new_length)
        # get person_id
        person_object = self.amity.people["all_people"][0]
        current_room = list(self.amity.rooms["living_space"].keys())[0]
        # get original number of room occupants
        original_number_of_occupants = len(self.amity.rooms["living_space"][current_room])
        print(original_number_of_occupants)
        # self.assertEqual(self.amity.reallocate_person(person_object.person_id, "o", new_room_name), "Room {0} does not exist".format(new_room_name))
        self.amity.reallocate_person(person_object.person_id, "l", new_room_name)
        number_after_adding_attempt = len(self.amity.rooms["living_space"][current_room])
        self.assertEqual(original_number_of_occupants, number_after_adding_attempt)

    def test_print_room_successfully(self):
        # get room
        room = list(self.amity.rooms["office"].keys())[0]
        self.assertEqual(type(self.amity.print_room(room.name)[1]), list)

    def test_print_room_does_not_print_when_given_wrong_name(self):
        # get room
        room = "I do not exist"
        self.assertEqual(self.amity.print_room(room), "Room {0} does not exist".format(room))

    def test_print_room_does_not_print_inexistent_room(self):
        # name of inexistent room
        room_name = "asdbakdsjs"
        self.assertEqual(self.amity.print_room(room_name), "The room {0} does not exist".format(room_name))

    def test_print_unallocated_to_office_dumps_to_file_successfully(self):
        file_name = "test.txt"
        self.amity.print_unallocated_to_office(file_name)
        self.assertTrue(os.path.exists(file_name))
        os.remove(file_name)

if __name__== '__main__':
    unittest.main()
