from .rooms import Room

class LivingSpace(Room):
    '''
        LivingSpace has slots for at most 4 people(Fellows ONLY)
    '''
    room_capacity = 6
    def init(self):
        super(LivingSpace, self).__init__(name)
