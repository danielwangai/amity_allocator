class Person(object):
    def __init__(self, first_name, last_name):
        self.person_id = id(self)
        self.first_name = first_name
        self.last_name = last_name
