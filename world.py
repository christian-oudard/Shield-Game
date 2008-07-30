from copy import deepcopy

import log
import vec

class Entity(object):
    pass

class Box(object):
    pass

class World(object):
    def __init__(self, board_size):
        self.board_size = board_size
        self.hero = Entity()
        self.hero.pos = (0, 0)
        self.boxes = [Box()]

    def update(self, command):
        move = command #STUB, all commands are movement commands
        old_state = deepcopy(self)
        hero = self.hero
        hero.pos = vec.add(hero.pos, move)
        x, y = hero.pos
        if self.check_bounds(hero.pos):
            hero.pos = old_state.hero.pos
    
    def check_bounds(self, pos):
        x, y = pos
        board_x, board_y = self.board_size
        return x < 0 or y < 0 or x >= board_x or y >= board_y

