"""This file defines database structure and methods to manipulate data."""
import sqlite3

from termcolor import cprint

# from .amity import Amity


class Database(object):
    """This class defines database structure and methods.

    The methods aid in data manipulation.
    """

    def __init__(self, db):
        """To initialize with database connection."""
        self.conn = sqlite3.connect(db)

    def cursor(self):
        """To aid in database functions.

        - traversal
        - retreival
        - update
        - delete
        """
        return self.conn.cursor()

    def commit(self):
        """To persist data permanently to database."""
        return self.conn.commit()

    def create_tables(self):
        """Method contains the schema for creating the tables."""
        cursor = self.cursor()
        create_room = '''
            CREATE TABLE IF NOT EXISTS room(
                id INTEGER PRIMARY KEY,
                name VARCHAR(30),
                room_type VARCHAR(30)
            );
        '''
        cursor.execute(create_room)

        create_person = '''
            CREATE TABLE IF NOT EXISTS person(
                id INTEGER PRIMARY KEY,
                first_name VARCHAR(30),
                last_name VARCHAR(30),
                category VARCHAR(30)
            );
        '''
        cursor.execute(create_person)

        allocation = """
            CREATE TABLE IF NOT EXISTS allocations (
            allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            room_id INTEGER,
            FOREIGN KEY (person_id) REFERENCES person(person_id),
            FOREIGN KEY (room_id) REFERENCES room(room_id),
            unique (person_id, room_id));"""
        cursor.execute(allocation)

        unallocated = """
            CREATE TABLE IF NOT EXISTS unallocated (
            unallocated_id INTEGER PRIMARY KEY AUTOINCREMENT,
            missing_room VARCHAR(30),
            person_id INTEGER,
            FOREIGN KEY (person_id) REFERENCES person(person_id),
            unique (person_id));"""
        cursor.execute(unallocated)

    def close_connection(self):
        """Method to close connection to databse."""
        return self.conn.close()

    def save_state(self, db_name, people, rooms):
        """To persist data to the database."""
        # save people data
        self.create_tables()
        cursor = self.cursor()

        # Save all people
        cprint('Saving...', "red")
        for key, value in people.items():
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
        for room in list(rooms["office"].keys()):
            try:
                cursor.execute("INSERT INTO room VALUES (?, ?, ?);",
                               (room.room_id, room.name, 'office'))
            except sqlite3.IntegrityError:
                continue

        # save living_space data
        cprint('Saving Living Space...', "red")
        for room in list(rooms["living_space"].keys()):
            try:
                cursor.execute("INSERT INTO room VALUES (?, ?, ?);",
                               (room.room_id, room.name, 'living_space'))
            except sqlite3.IntegrityError:
                continue
        # save allcations - offices
        cprint("Saving office allocations", "red")
        for room in list(rooms["office"].keys()):
            for person in rooms["office"][room]:
                try:
                    cursor.execute("INSERT INTO allocations(person_id, room_id)\
                     VALUES(?, ?);",
                                   (person.person_id, room.room_id))
                except sqlite3.IntegrityError:
                    continue

        # save allcations - living spaces
        cprint("Saving living space allocations", "red")
        for room in list(rooms["living_space"].keys()):
            for person in rooms["living_space"][room]:
                try:
                    cursor.execute("INSERT INTO allocations(person_id, room_id)\
                     VALUES(?, ?);",
                                   (person.person_id, room.room_id))
                except sqlite3.IntegrityError:
                    continue

        # save unallocated people to office waiting lists
        cprint("Saving people unallocated to offices", "red")
        for person in rooms["office_waiting_list"]:

            try:
                # print(type(person.person_id))
                cursor.execute("INSERT INTO unallocated (person_id,\
                 missing_room) VALUES(?, ?)",
                               (person.person_id, "s", ))
            except sqlite3.IntegrityError:
                continue

        # save unallocated people to office waiting lists
        cprint("Saving people unallocated to living spaces", "red")
        for person in rooms["living_space_waiting_list"]:

            try:
                # print(type(person.person_id))
                cursor.execute("INSERT INTO unallocated (person_id,\
                 missing_room) VALUES(?, ?)",
                               (person.person_id, "living_space", ))
            except sqlite3.IntegrityError:
                continue

        self.commit()

    def load_state(self, db_name, people, rooms):
        """To fetch data saved in the database and load them to amity."""
        # get db
        self.create_tables()
        cursor = self.cursor()

        # fetch people
        cprint('Loading people', "red")
        cursor.execute("SELECT * from person")
        people = cursor.fetchall()
        cursor.execute("SELECT * FROM room")
        rooms = cursor.fetchall()

        cursor.execute("SELECT * FROM allocations")
        allocated_people = cursor.fetchall()

        cursor.execute("SELECT * FROM unallocated")
        unallocated_people = cursor.fetchall()

        return people, rooms, allocated_people, unallocated_people
