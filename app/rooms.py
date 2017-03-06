class Room(object):
    # set as none to allow inheriting classes to specify its value
    room_capacity = None

    def __init__(self, name):
        self.room_id = id(self)
        self.name = name
