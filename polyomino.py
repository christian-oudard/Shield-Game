from entity import Entity

class Polyomino(object):
    def __init__(self, pieces):
        self.pieces = pieces
        for p in self.pieces:
            p.parent = self

    def move_poly(self, direction):
        for p in self.pieces:
            p.start_move(direction)
        return all(p.finish_move(direction) for p in self.pieces)

class Piece(Entity):
    def move(self, direction):
        return self.parent.move_poly(direction)
