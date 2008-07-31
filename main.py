#! /usr/bin/env python

import curses
import time
from copy import deepcopy

import log
import vec
from keys import key_mapping
from world import World

BOARD_X, BOARD_Y = BOARD_SIZE = (5, 5)
ORIGIN_X, ORIGIN_Y = ORIGIN = (2, 2)

def curses_main(stdscr):
    init(stdscr)
    world = World(BOARD_SIZE)
    while True:
        try:
            draw(stdscr, world)
        except curses.error:
            pass
        c = stdscr.getch()
        try:
            command = key_mapping[c]
        except KeyError:
            continue
        if command == 'undo':
            world.rollback()
        elif command == 'quit':
            break
        else:
            world.update(command)

def init(stdscr):
    log.init('py_curses_log')
    curses.curs_set(0)
    stdscr.refresh() # refresh right away so first call to stdscr.getch() doesn't overwrite the first draw()

def draw(win, world):
    x, y = to_screen(world.hero.pos)
    win.erase()
    draw_border(win, ORIGIN_Y - 1, ORIGIN_X - 1, BOARD_Y + 1, BOARD_X + 1)
    win.addch(y, x, '@')
    for b in world.boxes:
        x, y = to_screen(b.pos)
        win.addch(y, x, 'X')
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

def to_screen(pos):
    return vec.add(pos, ORIGIN)

if __name__ == '__main__':
    curses.wrapper(curses_main)

