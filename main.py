#! /usr/bin/env python

import curses
import time
import sys

from curses_game.world import World
from curses_game.keys import KEY_MAPPING
from curses_game.game_display import GameDisplay
from curses_game.move_shortcuts import move_codes, reverse_move_codes


def curses_main(stdscr):
    #debug(stdscr)
    args = sys.argv[1:]
    try:
        filename = args.pop()
    except IndexError:
        raise IndexError('Please specify a level.')

    replay_data = []
    if args and args[-1] == '--replay':
        with open(filename + '.solution') as f:
            contents = f.read()
        replay_data = load_replay(contents)

        def get_command(stdscr):
            time.sleep(.5)
            return replay_data.pop(0)

    try:
        with open(filename) as level_file:
            level_string = level_file.read()
    except IOError:
        return

    display = GameDisplay(stdscr)
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
            # Save a replay if we've improved the solution.
            with open(filename + '.solution') as f:
                contents = f.read()
            old_replay_data = load_replay(contents)
            new_replay_data = world.get_replay()
            if len(new_replay_data) < len(old_replay_data):
                with open(filename + '.solution', 'w') as f:
                    save_replay(new_replay_data, f)
            #STUB, load next level
            break

def get_command(stdscr):
    c = stdscr.getch()
    return KEY_MAPPING.get(c)

def save_replay(replay, f):
    for move in replay:
        f.write(move_codes[move] + '\n')

def load_replay(contents):
    replay = []
    for line in contents.splitlines():
        code = line.rstrip('\n')
        replay.append(reverse_move_codes[code])
    return replay

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
    lines = [l for l in level_string.splitlines() if l.strip() != '']
    width = max(len(line) for line in lines)
    height = len(lines) // 2
    assert height * 2 == len(lines), 'Must have an equal size terrain map and entity map.'

    terrain_lines = lines[:height]
    del lines[:height]
    entity_lines = lines[:height]
    del lines[:height]

    # Construct the world.
    world = World(terrain_lines, entity_lines)

    # Parse the tags.
    tag_string = '\n' + tag_string
    tags_list = tag_string.split('\n!')
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
            assert(world.terrain[pos] == 'i'), 'no "i" square at position %s' % (pos,)
            world.info_spaces[pos] = '\n'.join(tag_lines)
    # Make sure every "i" square has a tag.
    for pos, terrain in world.terrain.items():
        if terrain == 'i':
            assert pos in world.info_spaces, 'un-matched "i" square'

    world.check_sanity()

    return world

def debug(stdscr):
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    curses.wrapper(curses_main)
