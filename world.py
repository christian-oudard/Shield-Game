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
        e = self.check_collision(self.pos)
        if e is not None:
            return e.move(dir_vec)
        return True

    def check_collision(self, pos):
        for b in self.world.boxes:
            if b is self:
                continue
            if pos == b.pos:
                log.write('collision on %s' % (pos,))
                return b

class Hero(Entity):
    pass

class Box(Entity):
    pass

class World(object):
    def __init__(self, board_size):
        self.board_size = board_size
        self.hero = Hero(self, (0, 0))
        self.boxes = (
            Box(self, (2,3)),
            Box(self, (3,2)),
            Box(self, (3,3)),
        )
        self.history = []

    def update(self, command):
        move_dir = command #STUB, all commands are movement commands
        self.checkpoint()
        if not self.hero.move(move_dir):
            self.rollback()
            return

    def checkpoint(self):
        history_item = (
            self.hero.pos,
            tuple(b.pos for b in self.boxes),
        )
        self.history.append(history_item)
    
    def rollback(self):
        try:
            history_item = self.history.pop()
        except IndexError:
            return False
        old_hero_pos, old_boxes_pos = history_item
        self.hero.pos = old_hero_pos
        for b, old_pos in zip(self.boxes, old_boxes_pos):
            b.pos = old_pos

    def check_bounds(self, pos):
        x, y = pos
        board_x, board_y = self.board_size
        return x < 0 or y < 0 or x >= board_x or y >= board_y

