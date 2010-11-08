from copy import copy

import log

from entity.codes import ENTITY_CODES
from entity.entity import Entity
from entity.hero import Hero
from entity.polyomino import Polyomino, Piece

class World(object):
    def __init__(self, terrain_array, entity_array):
        self.level_completed = False
        self.num_moves = 0
        self.history = []
        self.info_spaces = {}
        self.init_terrain(terrain_array)
        self.init_entities(entity_array)

    def update(self, command):
        self.checkpoint()
        cmd_type, direction = command
        if cmd_type == 'move':
            result = self.hero.move(direction)
        elif cmd_type == 'shield':
            result = self.hero.shield(direction)
        if not result:
            self.rollback()
        else:
            self.num_moves += 1

    def goal(self):
        log.write('level finished')
        self.level_completed = True

    def checkpoint(self):
        history_item = {
            'moves' : self.num_moves,
            'terrain': copy(self.terrain),
            'positions': tuple(e.pos for e in self.entities),
            'solidity': tuple(e.solid for e in self.entities),
        }
        self.history.append(history_item)

    def rollback(self):
        self.display.show_bump()
        self.undo()

    def restart(self):
        self.history = [self.history[0]]
        self.undo()

    def undo(self):
        try:
            history_item = self.history.pop()
        except IndexError:
            return False
        self.num_moves = history_item['moves']
        self.terrain = history_item['terrain']
        for e, old_pos in zip(self.entities, history_item['positions']):
            e.pos = old_pos
        for e, old_solid in zip(self.entities, history_item['solidity']):
            e.solid = old_solid

    def init_terrain(self, terrain_array):
        self.terrain, self.board_size = grid_to_dict(terrain_array)

    def init_entities(self, entity_string):
        entity_dict, _ = grid_to_dict(
            entity_string,
            valid_characters=ENTITY_CODES.keys(),
        )
        self.entities = set()
        poly_groups = {}
        for pos, code in entity_dict.items():
            Class = ENTITY_CODES[code]
            e = Class()
            e.pos = pos
            e.display_character = code
            self.register_entity(e)
            if isinstance(e, Hero):
                self.hero = e
            elif isinstance(e, Piece):
                poly_groups.setdefault(code, []).append(e)
        for pieces in poly_groups.values():
            Polyomino(pieces)
        self.hero.create_shield()
        self.entities = tuple(self.entities)

    def register_entity(self, entity):
        self.entities.add(entity)
        entity.world = self

    def entity_at(self, pos):
        entities = [
            e for e in self.entities
            if e.pos == pos and e.solid
        ]
        assert len(entities) <= 1
        if entities:
            return entities[0]
        else:
            return None


def grid_to_dict(data_array, valid_characters=None):
    # fill data from string
    data = {}
    x_vals = []
    y_vals = []
    for y, line in enumerate(data_array):
        for x, character in enumerate(line):
            if not character.isspace():
                x_vals.append(x)
                y_vals.append(y)
                if valid_characters is None or character in valid_characters:
                    data[(x, y)] = character
    max_x = max(x_vals)
    max_y = max(y_vals)
    return data, (max_x + 1, max_y + 1)
