from entity import Entity
from terrain_constants import WATER, FLOOR

class Block(Entity):
    def __init__(self):
        Entity.__init__(self)

    def finish_move(self, direction):
        terrain_type = self.world.get_terrain(self.pos)
        if terrain_type == WATER:
            self.world.terrain[self.pos] = FLOOR
            self.solid = False
            return True
        return Entity.finish_move(self, direction)
