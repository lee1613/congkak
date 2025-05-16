class Congkak:
    top_player = None
    bottom_player = None
    def __init__(self, timer):
        self.timer = timer
    def add_player(self, player):
        if self.top_player is None:
            self.top_player = player
        elif self.bottom_player is None:
            self.bottom_player = player
        else:
            return "This Board is currently full, please find another game!"

class Player:
    score = 0
    def __init__(self, name):
        self.name = name


class Site:
    # The storehouse is always on the left to the player when they are sitting in front of the board
    # The gameplay is going on a clockwise direction
    storehouse = 0
    house = [7] * 7
    def __int__(self):
        pass
    def check_house(self, index):
        if 0 <= index < 7:
            return house[index]

class Storehouse:
    def __init__(self):



class house:
    def __init__(self):


