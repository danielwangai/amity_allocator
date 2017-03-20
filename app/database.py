import os
import sys
import sqlite3

class Database(object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        return self.conn.commit()

    def create_tables(self):
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
            allocation_id INTEGER PRIMARY KEY,
            person_id INTEGER,
            room_id INTEGER,
            FOREIGN KEY (person_id) REFERENCES employee(person_id),
            FOREIGN KEY (room_id) REFERENCES room(room_id),
            unique (person_id, room_id));"""
        cursor.execute(allocation)

        unallocated = """
            CREATE TABLE IF NOT EXISTS unallocated (
            unallocated_id INTEGER PRIMARY KEY,
            person_id INTEGER,
            FOREIGN KEY (person_id) REFERENCES employee(person_id),
            unique (person_id));"""
        cursor.execute(unallocated)


    def close_connection(self):
        return self.conn.close()

# db = Database("test.db")
# db.create()
