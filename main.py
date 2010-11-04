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
    try:
        with open(sys.argv[1]) as level_file:
            level_string = level_file.read()
    except IndexError:
        log.write('must specify level file as an argument')
        return
    except IOError:
        log.write('level file "%s" not found' % sys.argv[1])
        return
    world = load_level(level_string)
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

def load_level(level_string):
    # Determine where the tags start, if they exist.
    if '!' in level_string:
        i = level_string.index('!')
        tag_string = level_string[i:]
        level_string = level_string[:i]
    else:
        tag_string = ''

    # Determine the height and width of the level. Half the lines are the
    # terrain map, and half are the entity map.
    lines = level_string.strip().split('\n')
    width = max(len(line) for line in lines)
    height = len(lines) // 2
    assert height * 2 == len(lines), 'Must have an equal size terrain map and entity map.'

    terrain_lines = lines[:height]
    del lines[:height]
    entity_lines = lines[:height]
    del lines[:height]

    # Construct the world.
    world = World('\n'.join(terrain_lines), '\n'.join(entity_lines))

    # Parse the tags.
    tags_list = tag_string.split('!')
    for tag in tags_list:
        tag = tag.strip()
        if tag == '':
            continue
        tag_lines = tag.split('\n')
        header_line = tag_lines.pop(0).strip()
        tag_type, arguments = header_line.split(' ', 1)
        if tag_type == 'i':
            x, y = [int(a.strip()) for a in arguments.split(',', 1)]
            pos = (x, y)
            assert(world.terrain[pos] == 'i'), 'no "i" square at position %s' % pos
            world.info_spaces[pos] = '\n'.join(tag_lines)
    # Make sure every "i" square has a tag.
    for pos, terrain in world.terrain.items():
        if terrain == 'i':
            assert pos in world.info_spaces, 'un-matched "i" square'

    return world

if __name__ == '__main__':
    curses.wrapper(curses_main)

