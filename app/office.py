from .rooms import Room

class Office(Room):
    '''
        Office has slots for at most 6 people(Fellows and or Staff)
    '''
    room_capacity = 6
    def init(self):
        super(Office, self).__init__(name)
