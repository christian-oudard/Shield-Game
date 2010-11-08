from entity import Entity
from terrain_constants import WATER, FLOOR

class Block(Entity):
    def terrain_trigger(self):
        if self.current_terrain() == WATER:
            self.world.terrain[self.pos] = FLOOR
            self.solid = False
        return super(Block, self).terrain_trigger()

class HeavyBlock(Block):
    def get_bumped(self, entity, direction):
        if isinstance(entity, Block):
            return False # Don't respond to pushes from other blocks.
        return super(HeavyBlock, self).get_bumped(entity, direction)

    def bump_entity(self, entity, direction):
        return False # Don't transmit pushes through to adjacent objects.

class SlideBlock(Block):
    def move(self, direction):
        # When a sliding block is pushed, it keeps moving until it can't
        # anymore.
        first_result = super(SlideBlock, self).move(direction)
        while True:
            old_pos = self.pos
            self.start_move(direction)
            result = self.finish_move(direction)
            if not result:
                self.pos = old_pos
                break
        return first_result

    def bump_entity(self, entity, direction):
        return False # Don't transmit pushes through to adjacent objects.
