TERRAIN_BLANK = '.'
WALL = '#'
ENTITY_BLANK = '_'

from curses import *

# format:
# key code: (dx, dy)
# where dx and dy are the difference in x and y coordinate
KEY_MAPPING = {
    'q': 'quit',
    'u': 'undo',
    KEY_UP: (0, -1),
    KEY_DOWN: (0, 1),
    KEY_LEFT: (-1, 0),
    KEY_RIGHT: (1, 0),
    't': (0, -1),
    'h': (0, 1),
    'd': (-1, 0),
    'n': (1, 0),
    'f': (-1, -1),
    'g': (1, -1),
    'b': (-1, 1),
    'm': (1, 1),
}
for key, value in KEY_MAPPING.items():
    try:
        KEY_MAPPING[ord(key)] = value
    except TypeError:
        pass
