from entity import Entity
from terrain_constants import WATER, FLOOR

class Block(Entity):
    def __init__(self):
        Entity.__init__(self)

    def terrain_trigger(self):
        if self.current_terrain() == WATER:
            self.world.terrain[self.pos] = FLOOR
            self.solid = False
