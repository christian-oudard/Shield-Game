from copy import copy

import log

from entity import *

ENTITY_BLANK = '_'

class World(object):
    def __init__(self, terrain_string, entity_string):
        self.level_completed = False
        self.history = []
        self.terrain, self.board_size = parse_grid(terrain_string)
        entity_dict, _ = parse_grid(entity_string, ENTITY_BLANK)
        self.entities = set()
        poly_groups = {}
        for pos, code in entity_dict.items():
            Class = ENTITY_CODES[code]
            e = Class()
            e.pos = pos
            e.display_character = code
            self.register_entity(e)
            if Class is Hero: 
                self.hero = e
            elif Class is Piece:
                try:
                    poly_groups[code].append(e)
                except KeyError:
                    poly_groups[code] = [e]
        for pieces in poly_groups.values():
            Polyomino(pieces)
        self.hero.create_shield()
        self.entities = tuple(self.entities)
                                    
    def register_entity(self, entity):
        self.entities.add(entity)
        entity.world = self

    def update(self, command):
        self.checkpoint()
        type, dir_vec = command
        if type == 'move':
            result = self.hero.move(dir_vec)
        elif type == 'shield':
            result = self.hero.shield(dir_vec)
        if not result:
            self.rollback()
            return

    def goal(self):
        self.level_completed = True

    def get_terrain(self, pos):
        try:
            return self.terrain[pos]
        except KeyError:
            return None

    def checkpoint(self):
        history_item = {
            'positions': tuple(e.pos for e in self.entities),
            'solidity': tuple(e.solid for e in self.entities),
            'terrain': copy(self.terrain)
        }
        self.history.append(history_item)

    def rollback(self):
        self.display.show_bump(self)
        self.undo()
    
    def undo(self):
        try:
            history_item = self.history.pop()
        except IndexError:
            return False
        self.terrain = history_item['terrain']
        for e, old_pos in zip(self.entities, history_item['positions']):
            e.pos = old_pos
        for e, old_solid in zip(self.entities, history_item['solidity']):
            e.solid = old_solid


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

    return data, (max_x + 1, max_y + 1)
