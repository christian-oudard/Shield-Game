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
    board_win = init(stdscr)
    world = World(BOARD_SIZE)
    while True:
        try:
            draw(board_win, world)
        except curses.error:
            pass
        c = stdscr.getch()
        try:
            command = key_mapping[c]
        except KeyError:
            continue
        world.update(command)

def draw(win, world):
    x, y = world.hero.pos
    win.erase()
    win.border(*'||--++++')
    win.addch(y + 1, x + 1, '@')
    for b in world.boxes:
        x, y = b.pos
        win.addch(y + 1, x + 1, 'X')
    win.refresh()

def init(stdscr):
    log.init('py_curses_log')
    curses.curs_set(0)
    board_win = curses.newwin(BOARD_Y + 2, BOARD_X + 2, ORIGIN_Y, ORIGIN_X)
    board_win.leaveok(1)
    stdscr.refresh() # refresh right away so first call to stdscr.getch() doesn't overwrite the first draw()
    return board_win

if __name__ == '__main__':
    curses.wrapper(curses_main)

