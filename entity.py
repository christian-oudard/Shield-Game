import log
import vec

class Entity(object):
    def __init__(self, world, pos):
        self.world = world
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

class Hero(Entity):
    pass

class Box(Entity):
    pass

ENTITY_CODES = {
    '@': Hero,
    'X': Box,
}
for code, Class in ENTITY_CODES.items():
    Class.display_character = code
