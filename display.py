import time
import curses
from curses import *

import log
import vec

from entity import FLOOR

ORIGIN_X, ORIGIN_Y = ORIGIN = (3, 2)

class Display(object):
    def __init__(self, scr):
        self.scr = scr
        curses.curs_set(0)
        scr.refresh() # refresh right away so first call to stdscr.getch() doesn't overwrite the first draw()

    def show_bump(self):
        self.draw()
        time.sleep(.2)

    def show_message(self, message):
        board_x, board_y = self.world.board_size
        self.scr.addstr(ORIGIN_Y + board_y + 2, 0, message)

    def show_info(self):
        pos = self.world.hero.pos
        if pos not in self.world.info_spaces:
            return
        info = world.info_spaces[pos]
        self.show_message(info)
    
    def draw(self):
        board_x, board_y = self.world.board_size
        self.scr.erase()
        self.draw_border(ORIGIN_Y - 1, ORIGIN_X - 1, board_y + 1, board_x + 1)
        self.show_info()
        self.scr.addstr(0, 0, str(self.world.num_moves))#DEBUG
        for pos, ter in self.world.terrain.items():
            if ter == FLOOR:
                ter = ' '
            x, y = to_screen(pos)
            self.scr.addch(y, x, ter)
        for e in self.world.entities:
            if not e.solid:
                continue
            x, y = to_screen(e.pos)
            self.scr.addch(y, x, e.display_character)
        self.scr.refresh()

    def draw_border(self, top, left, height, width):
        bottom = top + height
        right = left + width
        corners = (
            (top, left),
            (top, right),
            (bottom, left),
            (bottom, right),
        )
        for y, x in corners:
            self.scr.addch(y, x, '#')
        self.scr.hline(top, left + 1, '#', width - 1)
        self.scr.hline(bottom, left + 1, '#', width - 1)
        self.scr.vline(top + 1, left, '#', height - 1)
        self.scr.vline(top + 1, right, '#', height - 1)

def to_screen(pos):
    return vec.add(pos, ORIGIN)
