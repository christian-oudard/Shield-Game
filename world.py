from copy import deepcopy

import log
import vec

class Entity(object):
    def __init__(self, world, pos):
        self.world = world
        self.pos = pos

    def move(self, dir_vec):
        self.pos = vec.add(self.pos, dir_vec)
        if self.world.check_bounds(self.pos):
            return False
        return True

class Hero(Entity):
    pass

class Box(Entity):
    pass

class World(object):
    def __init__(self, board_size):
        self.board_size = board_size
        self.hero = Hero(self, (0, 0))
        self.boxes = [Box(self, (3,3))]

    def update(self, command):
        move_dir = command #STUB, all commands are movement commands
        self.old_state = deepcopy(self)
        if not self.hero.move(move_dir):
            self.rollback()
            return
    
    def rollback(self):
        self.hero.pos = self.old_state.hero.pos

    def check_bounds(self, pos):
        x, y = pos
        board_x, board_y = self.board_size
        return x < 0 or y < 0 or x >= board_x or y >= board_y

