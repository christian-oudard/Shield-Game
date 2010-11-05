import log
import vec

from terrain_constants import WALL

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
        e = self.collide_entity()
        if e:
            return e.move(direction)
        return True

    def collide_terrain(self):
        terrain_type = self.world.terrain.get(self.pos)
        return terrain_type in self.illegal_terrain

    def collide_entity(self):
        if not self.solid:
            return None
        for b in self.world.entities:
            if b is self or not b.solid:
                continue
            if self.pos == b.pos:
                return b

    def current_terrain(self):
        return self.world.terrain.get(self.pos)

    def terrain_trigger(self):
        pass # overriden in subclasses

