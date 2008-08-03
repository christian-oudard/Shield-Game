from curses import *

# format:
# key code: (dx, dy)
# where dx and dy are the difference in x and y coordinate
KEY_MAPPING = {
    'q': 'quit',
    'u': 'undo',
    KEY_DC: 'undo',
    KEY_BACKSPACE: 'undo',
    KEY_UP: ('move', (0, -1)),
    KEY_DOWN: ('move', (0, 1)),
    KEY_LEFT: ('move', (-1, 0)),
    KEY_RIGHT: ('move', (1, 0)),
    ' ': ('shield',), # dead-key for shield

    # dvorak nethack-style bindings
    't': ('move', (0, -1)),
    'h': ('move', (0, 1)),
    'd': ('move', (-1, 0)),
    'n': ('move', (1, 0)),
    'f': ('move', (-1, -1)),
    'g': ('move', (1, -1)),
    'b': ('move', (-1, 1)),
    'm': ('move', (1, 1)),
    'v': ('move', (0, 0)),
    'T': ('shield', (0, -1)),
    'H': ('shield', (0, 1)),
    'D': ('shield', (-1, 0)),
    'N': ('shield', (1, 0)),
    'F': ('shield', (-1, -1)),
    'G': ('shield', (1, -1)),
    'B': ('shield', (-1, 1)),
    'M': ('shield', (1, 1)),

    # numpad bindings
    '8': ('move', (0, -1)),
    '2': ('move', (0, 1)),
    '4': ('move', (-1, 0)),
    '6': ('move', (1, 0)),
    '7': ('move', (-1, -1)),
    '9': ('move', (1, -1)),
    '1': ('move', (-1, 1)),
    '3': ('move', (1, 1)),
    '5': ('move', (0, 0)),
    '+': ('shield',), # dead-key for shield
}
for key, value in KEY_MAPPING.items():
    try:
        KEY_MAPPING[ord(key)] = value
    except TypeError:
        pass

def get_command(stdscr):
    command = get_key(stdscr)
    try:
        if len(command) == 1: # dead key command, length 1 list
            key = command[0]
            command2 = get_key(stdscr)
            if len(command2) == 1:
                key2 = command2[0]
                if key == key2:
                    return (key, (0, 0))
            _, dir_vec = command2
            return (key, dir_vec)
    except TypeError:
        return None
    except ValueError:
        return None
    return command
             
def get_key(stdscr):
    c = stdscr.getch()
    try:
        key = KEY_MAPPING[c]
    except KeyError:
        return #STUB
    return key
