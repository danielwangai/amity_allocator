class Person(object):
    def __init__(self, name):
        self.person_id = id(self)
        self.name = name
