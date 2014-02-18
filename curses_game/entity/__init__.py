import vec

from curses_game.terrain_constants import WALL

class Entity(object):
    def __init__(self):
        self.solid = True
        self.illegal_terrain = [None, WALL]

    def move(self, direction):
        self.start_move(direction)
        result = self.finish_move(direction)
        if result:
            self.terrain_trigger()
        return result

    def start_move(self, direction):
        self.pos = vec.add(self.pos, direction)

    def finish_move(self, direction):
        if self.solid and self.collide_terrain():
            return False
        e = self.collided_entity()
        if e:
            return self.bump_entity(e, direction)
        return True

    def get_bumped(self, entity, direction):
        # When you are triggered to move in a direction, do so.
        # Subclasses can override this.
        return self.move(direction)

    def bump_entity(self, entity, direction):
        """
        This specifies what action you take when you bump another entity.
        """
        return entity.get_bumped(self, direction)

    def collided_entity(self):
        if not self.solid:
            return None
        # Temporarily turn off solidity to check what other solid entities might be here.
        self.solid = False
        other = self.world.entity_at(self.pos)
        self.solid = True
        return other

    def current_terrain(self):
        return self.world.terrain.get(self.pos)

    def collide_terrain(self):
        terrain_type = self.world.terrain.get(self.pos)
        return terrain_type in self.illegal_terrain

    def terrain_trigger(self):
        pass # Overriden in subclasses.
