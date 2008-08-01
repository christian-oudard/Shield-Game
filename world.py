from copy import deepcopy

import log

from entity import *

ENTITY_BLANK = '_'
WALL = '#'

class World(object):
    def __init__(self, terrain_string, entity_string):
        self.history = []
        self.terrain, self.board_size = parse_grid(terrain_string)
        entity_dict, _ = parse_grid(entity_string, ENTITY_BLANK)
        self.entities = set()
        for pos, code in entity_dict.items():
            Class = ENTITY_CODES[code]
            e = Class(pos)
            self.register_entity(e)
            if Class is Hero: 
                self.hero = e
        #debug
        pieces = [
            Piece((1, 1)),
            Piece((2, 2)),
        ]
        Polyomino(pieces)
        for p in pieces:
            self.register_entity(p)
        pieces = [
            Piece((2, 1)),
            Piece((1, 2)),
        ]
        Polyomino(pieces)
        for p in pieces:
            self.register_entity(p)
        
                                    
    def register_entity(self, entity):
        self.entities.add(entity)
        entity.world = self

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
