from entity import Entity

class Polyomino(object):
    def __init__(self, pieces):
        self.pieces = pieces
        for p in self.pieces:
            p.polyomino = self

    def move_poly(self, direction):
        for p in self.pieces:
            p.start_move(direction)
        result = all(p.finish_move(direction) for p in self.pieces)
        if result:
            for p in self.pieces:
                p.terrain_trigger()
        return result

    def terrain_trigger(self):
        if not all(p.terrain_trigger_test() for p in self.pieces):
            return
        for p in self.pieces:
            p.terrain_trigger_action()


class Piece(Entity):
    def move(self, direction):
        return self.polyomino.move_poly(direction)

    def terrain_trigger(self):
        return self.polyomino.terrain_trigger()

    def terrain_trigger_test(self):
        return True # overriden in subclasses

    def terrain_trigger_action(self):
        pass # overriden in subclasses


from terrain_constants import WATER, FLOOR
class BlockPiece(Piece):
    def terrain_trigger_test(self):
        return self.current_terrain() == WATER

    def terrain_trigger_action(self):
        self.world.terrain[self.pos] = FLOOR
        self.solid = False
