from copy import deepcopy

import log
import vec

class Entity(object):
    def __init__(self, world, pos):
        self.world = world
        self.pos = pos

    def move(self, dir_vec):
        self.pos = vec.add(self.pos, dir_vec)
        if self.world.collide_terrain(self.pos):
            return False
        e = self.collide_entity(self.pos)
        if e is not None:
            return e.move(dir_vec)
        return True

    def collide_entity(self, pos):
        for b in self.world.entities:
            if b is self:
                continue
            if pos == b.pos:
                return b

class Hero(Entity):
    pass

class Box(Entity):
    pass

TERRAIN_BLANK = '.'
WALL = '#'
ENTITY_BLANK = '_'
ENTITY_CODES = {
    '@': Hero,
    'X': Box,
}
for code, Class in ENTITY_CODES.items():
    Class.display_character = code

class World(object):
    def __init__(self, terrain_string, entity_string):
        self.history = []
        self.terrain, self.board_size = parse_grid(terrain_string)
        entity_dict, _ = parse_grid(entity_string, ENTITY_BLANK)
        self.hero = None
        self.entities = []
        for pos, code in entity_dict.items():
            Class = ENTITY_CODES[code]
            self.entities.append(Class(self, pos))
            if Class is Hero and self.hero is None:
                self.hero = self.entities[-1]

    def update(self, command):
        move_dir = command #STUB, all commands are movement commands
        self.checkpoint()
        if not self.hero.move(move_dir):
            self.rollback()
            return

    def checkpoint(self):
        history_item = tuple(b.pos for b in self.entities)
        self.history.append(history_item)
    
    def rollback(self):
        try:
            history_item = self.history.pop()
        except IndexError:
            return False
        for e, old_pos in zip(self.entities, history_item):
            e.pos = old_pos

    def collide_terrain(self, pos):
        try:
            return self.terrain[pos] == WALL
        except KeyError:
            return True

def parse_grid(data_string, blanks=''):
    lines = data_string.split('\n')
    try:
        while True: # remove blank lines
            lines.remove('')
    except ValueError: pass

    # fill data from string
    init_data = {}
    x_vals = []
    y_vals = []
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            if not character.isspace():
                x_vals.append(x)
                y_vals.append(y)
                if character not in blanks:
                    init_data[(x,y)] = character

    # bounds correction
    for pos in init_data.keys():
        x, y = pos
    min_x, max_x = min(x_vals), max(x_vals)
    min_y, max_y = min(y_vals), max(y_vals)
    data = {}
    for key, value in init_data.items():
        x, y = key
        data[(x-min_x, y-min_y)] = value

    log.write('max x, max y =', max_x, ',', max_y)
    return data, (max_x + 1, max_y + 1)
