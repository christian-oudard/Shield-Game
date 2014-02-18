from copy import copy

from curses_game.terrain_constants import all_terrain_codes
from curses_game.entity.codes import ENTITY_CODES
from curses_game.entity import Entity
from curses_game.entity.hero import Hero
from curses_game.entity.polyomino import Polyomino, Piece

class World(object):
    def __init__(self, terrain_array, entity_array):
        self.level_completed = False
        self.num_moves = 0
        self.history = []
        self.info_spaces = {}
        self.init_terrain(terrain_array)
        self.init_entities(entity_array)

    def update(self, command):
        self.checkpoint(command)
        if command == ('move', (0, 0)):
            command = ('shield', (0, 0))
        cmd_type, direction = command
        if cmd_type == 'move':
            result = self.hero.move(direction)
        elif cmd_type == 'shield':
            result = self.hero.shield(direction)
        if not result:
            self.rollback()
        else:
            self.num_moves += 1
        self.check_sanity()
        return result

    def goal(self):
        self.level_completed = True

    def checkpoint(self, command):
        history_item = {
            'command': command,
            'moves' : self.num_moves,
            'terrain': copy(self.terrain),
            'positions': dict((e, e.pos) for e in self.entities),
            'solidity': dict((e, e.solid) for e in self.entities),
        }
        self.history.append(history_item)

    def get_replay(self):
        return [h['command'] for h in self.history]

    def rollback(self):
        self.display.show_bump()
        self.undo()

    def restart(self):
        if self.history:
            self.history = [self.history[0]]
            self.undo()

    def undo(self):
        if not self.history:
            return
        history_item = self.history.pop()
        self.num_moves = history_item['moves']
        self.terrain = history_item['terrain']
        for e in self.entities:
            e.pos = history_item['positions'][e]
            e.solid = history_item['solidity'][e]

    def init_terrain(self, terrain_array):
        self.terrain, self.board_size = grid_to_dict(terrain_array)
        for pos, code in self.terrain.items():
            if code not in all_terrain_codes:
                raise KeyError('Illegal terrain code at position %s: "%s"' % (pos, code))

    def init_entities(self, entity_array):
        entity_dict, _ = grid_to_dict(entity_array)
        self.entities = set()
        poly_groups = {}
        for pos, code in entity_dict.items():
            if code in all_terrain_codes:
                continue # Ignore terrain in entity grid.
            if code not in ENTITY_CODES:
                raise KeyError('Illegal entity code at position %s: "%s"' % (pos, code))
            Class = ENTITY_CODES[code]
            if Class is None:
                continue
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

    def check_sanity(self):
        # Check that no solid object is on terrain it may not occupy.
        for e in self.entities:
            if e.solid:
                assert e.current_terrain() is not None, 'Entity out of bounds at %s' % (e.pos,)
                assert e.current_terrain() not in e.illegal_terrain, 'Entity on illegal terrain at %s' % (e.pos,)
        # Check that no two solid objects occupy the same space.
        for a, b in all_pairs(self.entities):
            if a.solid and b.solid:
                assert a.pos != b.pos, 'Two solid objects both occupying space %s' % (a.pos,)


def grid_to_dict(data_array):
    # fill data from string
    data = {}
    x_vals = []
    y_vals = []
    for y, line in enumerate(data_array):
        for x, character in enumerate(line):
            if not character.isspace():
                x_vals.append(x)
                y_vals.append(y)
                data[(x, y)] = character
    max_x = max(x_vals)
    max_y = max(y_vals)
    return data, (max_x + 1, max_y + 1)

def all_pairs(iterable):
    """
    Iterate over all possible pairs in the iterable, in lexicographic order.

    >>> list(''.join(pair) for pair in all_pairs('abcd'))
    ['ab', 'ac', 'ad', 'bc', 'bd', 'cd']
    """
    iterable = list(iterable)
    for i, a in enumerate(iterable):
        for b in iterable[i+1:]:
            yield (a, b)
