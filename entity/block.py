from entity import Entity
from terrain_constants import WATER, FLOOR

class Block(Entity):
    def terrain_trigger(self):
        if self.current_terrain() == WATER:
            self.world.terrain[self.pos] = FLOOR
            self.solid = False

class HeavyBlock(Block):
    def get_bumped(self, entity, direction):
        if isinstance(entity, Block):
            return False # Don't respond to pushes from other blocks.
        return Block.get_bumped(self, entity, direction)

    def bump_entity(self, entity, direction):
        return False # Don't transmit pushes through to adjacent objects.
