import log
import vec

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
print R_DIRECTIONS

class Entity(object):
    def __init__(self, pos):
        self.pos = pos
        self.solid = True

    def move(self, dir_vec):
        self.start_move(dir_vec)
        return self.finish_move(dir_vec)

    def start_move(self, dir_vec):
        self.pos = vec.add(self.pos, dir_vec)

    def finish_move(self, dir_vec):
        if self.solid and self.world.collide_terrain(self.pos):
            return False
        e = self.collide_entity()
        if e:
            return e.move(dir_vec)
        return True

    def collide_entity(self):
        if not self.solid:
            return None
        for b in self.world.entities:
            if b is self or not b.solid:
                continue
            if self.pos == b.pos:
                return b


class Polyomino(object):
    def __init__(self, pieces):
        self.pieces = pieces
        for p in self.pieces:
            p.parent = self

    def move_poly(self, dir_vec):
        for p in self.pieces:
            p.start_move(dir_vec)
        return all(p.finish_move(dir_vec) for p in self.pieces)


class Piece(Entity):
    def move(self, dir_vec):
        return self.parent.move_poly(dir_vec)


class Hero(Piece):
    def create_shield(self):
        self.shield_pieces = []
        for i in range(8):
            d = DIRECTIONS[i]
            pos = vec.add(self.pos, d)
            piece = Piece(pos)
            piece.display_character = '*'
            self.world.register_entity(piece)
            self.shield_pieces.append(piece)
        Polyomino([self] + self.shield_pieces)
        self.shield((0, 0))

    def shield(self, dir_vec):
        self.shield_position = dir_vec
        for s in self.shield_pieces:
            s.solid = False
        try:
            center = R_DIRECTIONS[dir_vec]
        except KeyError:
            return True
        left = (center - 1) % 8
        right = (center + 1) % 8
        for d in (left, center, right):
            p = self.shield_pieces[d]
            p.solid = True
            if not p.finish_move(dir_vec):
                return False
        return True #STUB, check whether there is room


class Box(Entity):
    pass

ENTITY_CODES = {
    '@': Hero,
    'X': Box,
    'A': Piece,
    'B': Piece,
    'C': Piece,
    'D': Piece,
}

