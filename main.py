#! /usr/bin/env python

import curses
import time
from copy import deepcopy

import log
import vec
from keys import key_mapping
from world import World

ORIGIN_X, ORIGIN_Y = ORIGIN = (3, 2)

def curses_main(stdscr):
    init(stdscr)
    world = load_level('1')
    if world is None:
        return #STUB
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
    board_x, board_y = world.board_size
    x, y = to_screen(world.hero.pos)
    win.erase()
    draw_border(win, ORIGIN_Y - 1, ORIGIN_X - 1, board_y + 1, board_x + 1)
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
    win.hline(top, left + 1, '-', width - 1)
    win.hline(bottom, left + 1, '-', width - 1)
    win.vline(top + 1, left, '|', height - 1)
    win.vline(top + 1, right, '|', height - 1)

import os
LEVEL_PATH = 'levels'
def load_level(filename):
    file_path = os.path.join(LEVEL_PATH, filename)
    try:
        f = open(file_path)
    except IOError:
        log.write('level file "%s" not found' % file_path)
        return None
    size_line = f.readline()
    try:
        width, height = size_line.strip().split(',')
        width = int(width)
        height = int(height)
    except ValueError:
        log.write('invalid level-size line: %r' % size_line)
        return None
    return World((width, height))

def to_screen(pos):
    return vec.add(pos, ORIGIN)

if __name__ == '__main__':
    curses.wrapper(curses_main)

