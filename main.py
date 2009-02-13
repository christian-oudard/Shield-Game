#! /usr/bin/env python

import curses
import time
import os
import sys

import log
import vec

from world import World
from keys import get_command
from display import GameDisplay

def curses_main(stdscr):
    log.init('curses_game_log')
    display = GameDisplay(stdscr)
    world = load_level(sys.argv[1])
    if world is None:
        return
    display.world = world
    world.display = display
    while True:
        display.refresh()
        command = get_command(stdscr)
        if command is None:
            continue
        if command == 'undo':
            world.undo()
        elif command == 'restart':
            display.show_message('Press key again to restart level.')
            if get_command(stdscr) == 'restart':
                world.restart()
        elif command == 'quit':
            display.show_message('Press key again to quit game.')
            if get_command(stdscr) == 'quit':
                stdscr.erase()
                stdscr.refresh()
                break
        elif command == 'shield':
            command2 = get_command(stdscr)
            if command2 == 'shield':
                world.update(('shield', (0, 0)))
            else:
                try:
                    action, direction = command2
                except ValueError:
                    continue
                except TypeError:
                    continue
                world.update(('shield', direction))
        else:
            world.update(command)
        if world.level_completed:
            display.refresh()
            display.show_message('Level Completed in %i moves' % world.num_moves)
            stdscr.refresh()
            time.sleep(1)
            #STUB, load next level
            break

def load_level(filename):
    try:
        f = open(filename)
    except IOError:
        log.write('level file "%s" not found' % filename)
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
    world = World(terrain_lines, entity_lines)
    tags = f.read() # remainder of file is tag lines
    tags_list = tags.split('#')
    for tag in tags_list:
        if tag.strip() == '':
            continue
        tag_lines = tag.split('\n')
        header_line = tag_lines.pop(0).strip()
        tag_type, arguments = header_line.split(' ', 1)
        if tag_type == 'i':
            x, y = [int(a.strip()) for a in arguments.split(',', 1)]
            pos = (x, y)
            assert(world.terrain[pos] == 'i')
            world.info_spaces[pos] = '\n'.join(tag_lines)
    return world

if __name__ == '__main__':
    curses.wrapper(curses_main)

