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
    def __init__(self):
        self.sliding = False
        super(SlideBlock, self).__init__()

    def move(self, direction):
        # When a sliding block is pushed, it keeps moving until it can't
        # anymore.
        if not self.sliding:
            self.sliding = False
            result = super(SlideBlock, self).move(direction)
            if not result:
                return result
            self.sliding = True
        while self.solid:
            old_pos = self.pos
            self.start_move(direction)
            result = self.finish_move(direction)
            if result:
                self.terrain_trigger()
            if not result:
                self.pos = old_pos
                self.sliding = False
                break
        return True

    def bump_entity(self, entity, direction):
        # Don't transmit pushes through to adjacent objects while sliding.
        if self.sliding:
            # If you hit another slide block while sliding, transfer momentum.
            if isinstance(entity, SlideBlock):
                entity.sliding = True
                entity.get_bumped(self, direction)
            return False
        return super(SlideBlock, self).bump_entity(entity, direction)
