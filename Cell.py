

class Cell:
    def __init__(self, value):
        self.collapsed = False
        if type(value) == type([]):
            self.options = value
        else:
            self.options = list(map(lambda x: x, range(value)))