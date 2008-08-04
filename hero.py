import vec

from entity import Entity
from polyomino import Polyomino, Piece
from terrain_constants import WATER, SPIKE, GOAL

DIRECTIONS = {
    0: (0, -1),
    1: (1, -1),
    2: (1, 0),
    3: (1, 1),
    4: (0, 1),
    5: (-1, 1),
    6: (-1, 0),
    7: (-1, -1),
}
R_DIRECTIONS = dict([(value, key) for key, value in DIRECTIONS.items()])

class Hero(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.illegal_terrain.extend([
            WATER,
            SPIKE,
        ])

    def finish_move(self, direction):
        terrain_type = self.world.get_terrain(self.pos)
        if terrain_type == GOAL:
            self.world.goal()
            return True
        return Entity.finish_move(self, direction)

    def create_shield(self):
        self.shield_pieces = []
        for i in range(8):
            d = DIRECTIONS[i]
            pos = vec.add(self.pos, d)
            piece = Piece()
            piece.pos = pos
            piece.display_character = '-\|/'[i % 4]
            self.world.register_entity(piece)
            self.shield_pieces.append(piece)
        Polyomino([self] + self.shield_pieces)
        self.shield((0, 0))

    def shield(self, direction):
        self.shield_position = direction
        for s in self.shield_pieces:
            s.solid = False
        try:
            middle = R_DIRECTIONS[direction]
        except KeyError:
            return True
        left = (middle - 1) % 8
        right = (middle + 1) % 8
        for d in (left, middle, right):
            p = self.shield_pieces[d]
            p.solid = True
            if not p.finish_move(direction):
                return False
        return True
