from curses import *

import log
import vec

ORIGIN_X, ORIGIN_Y = ORIGIN = (3, 2)

def draw(win, world):
    board_x, board_y = world.board_size
    win.erase()
    draw_border(win, ORIGIN_Y - 1, ORIGIN_X - 1, board_y + 1, board_x + 1)
    for pos, t in world.terrain.items():
        x, y = to_screen(pos)
        win.addch(y, x, t)
    for e in world.entities:
        if not e.solid:
            continue
        x, y = to_screen(e.pos)
        win.addch(y, x, e.display_character)
    win.refresh()

def draw_border(win, top, left, height, width):
    bottom = top + height
    right = left + width
    corners = (
        (top, left),
        (top, right),
        (bottom, left),
        (bottom, right),
    )
    for y, x in corners:
        win.addch(y, x, '+')
    win.hline(top, left + 1, '-', width - 1)
    win.hline(bottom, left + 1, '-', width - 1)
    win.vline(top + 1, left, '|', height - 1)
    win.vline(top + 1, right, '|', height - 1)

def to_screen(pos):
    return vec.add(pos, ORIGIN)
