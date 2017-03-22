"""This file defines database structure and methods to manipulate data."""
import sqlite3


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
