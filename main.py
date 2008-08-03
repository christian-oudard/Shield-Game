#! /usr/bin/env python

import curses
import time
import sys

import log
import vec

from world import World
from keys import get_command
from display import Display

def curses_main(stdscr):
    display = init(stdscr)
    world = load_level(sys.argv[1])
    if world is None:
        return
    world.display = display
    while True:
        display.draw(world)
        command = get_command(stdscr)
        if command is None:
            continue
        if command == 'undo':
            world.undo()
        elif command == 'quit':
            stdscr.erase()
            stdscr.refresh()
            break
        else:
            world.update(command)
            if world.level_completed:
                log.write('level finished')
                display.draw(world)
                stdscr.addstr(0, 0, 'WINNER')
                stdscr.refresh()
                time.sleep(1)
                #STUB, load next level
                break

def init(stdscr):
    log.init('curses_game_log')
    return Display(stdscr)

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
    terrain_lines = ''.join(f.readline() for i in range(height))
    entity_lines = ''.join(f.readline() for i in range(height))
    return World(terrain_lines, entity_lines)

if __name__ == '__main__':
    curses.wrapper(curses_main)

