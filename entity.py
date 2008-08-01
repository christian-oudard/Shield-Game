import log
import vec

class Entity(object):
    def __init__(self, pos):
        self.pos = pos

    def move(self, dir_vec):
        self.pos = vec.add(self.pos, dir_vec)
        if self.world.collide_terrain(self.pos):
            return False
        e = self.collide_entity()
        if e:
            return e.move(dir_vec)
        return True

    def collide_entity(self):
        for b in self.world.entities:
            if b is self:
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
    def __init__(self, pos):
        Entity.__init__(self, pos)

    def move(self, dir_vec):
        return self.parent.move_poly(dir_vec)

    def start_move(self, dir_vec):
        self.pos = vec.add(self.pos, dir_vec)

    def finish_move(self, dir_vec):
        if self.world.collide_terrain(self.pos):
            return False
        e = self.collide_entity()
        if e:
            return e.move(dir_vec)
        return True


class Hero(Entity):
    pass

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

