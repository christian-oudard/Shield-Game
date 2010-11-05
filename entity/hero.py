import log
import vec

from polyomino import Polyomino, Piece
from terrain_constants import WATER, SPIKE, GOAL
from move_shortcuts import (
    northwest,
    west,
    southwest,
    north,
    center,
    south,
    northeast,
    east,
    southeast,
)

DIRECTIONS = {
    0: north,
    1: northeast,
    2: east,
    3: southeast,
    4: south,
    5: southwest,
    6: west,
    7: northwest,
}
R_DIRECTIONS = dict([(value, key) for key, value in DIRECTIONS.items()])

class Hero(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.illegal_terrain.extend([
            WATER,
            SPIKE,
        ])

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
        if direction == center:
            return True # Close the shield.
        middle = R_DIRECTIONS[direction]
        left = (middle - 1) % 8
        right = (middle + 1) % 8
        for d in (left, middle, right):
            p = self.shield_pieces[d]
            p.solid = True
            if not p.finish_move(direction):
                return False
        return True

    def terrain_trigger_test(self):
        return self.current_terrain() == GOAL

    def terrain_trigger_action(self):
        self.world.goal()
