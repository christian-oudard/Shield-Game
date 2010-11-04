from __future__ import print_function

from nose.tools import assert_equal

import os
from textwrap import dedent

from main import load_level

import log
log.write = print

def test_load_level():
    world = load_level(dedent(
        '''
        2, 2
        .$
        #.
        @_
        __
        '''))
    assert_equal(world.level_completed, False)
    assert_equal(world.num_moves, 0)
    assert_equal(world.history, [])
    assert_equal(world.info_spaces, {})
    assert_equal(world.board_size, (2, 2))
    assert_equal(world.terrain, {(0, 0): '.', (1, 0): '$', (0, 1): '#', (1, 1): '.'})

    assert_equal(len(world.entities), 9) # The hero and 8 shield pieces.
    hero = world.hero
    assert_equal(hero.pos, (0, 0))
    assert_equal(len(hero.shield_pieces), 8)
    assert hero in world.entities

def test_load_level_info():
    world = load_level(dedent(
        '''
        3, 3
        ..$
        .i.
        #.i
        @__
        ___
        ___

        !i 1, 1
        note one

        !i 2, 2
        note two
        '''))
    assert_equal(world.board_size, (3, 3))
    assert_equal(world.terrain[(1, 1)], 'i')
    assert_equal(world.terrain[(2, 2)], 'i')
    assert_equal(world.info_spaces, {(1, 1): 'note one', (2, 2): 'note two'})

def test_load_all_game_levels():
    fail_count = 0
    for dirpath, dirnames, filenames in os.walk('levels'):
        for filename in filenames:
            if filename.startswith('.'):
                continue
            file_path = os.path.join(dirpath, filename)
            with open(file_path) as f:
                level_string = f.read()
            try:
                load_level(level_string)
            except Exception as e:
                print('problem loading level %s:' % file_path)
                print(e)
                print()
                fail_count += 1
    if fail_count:
        raise Exception('%d levels did not load' % fail_count)

def test_move_command():
    world = load_level(dedent(
        '''
        3, 1
        ..$
        @__
        '''))
    assert_equal(world.hero.pos, (0, 0))
    world.update(('move', (1, 0)))
    assert_equal(world.hero.pos, (1, 0))
    world.update(('move', (1, 0)))
    assert_equal(world.hero.pos, (2, 0))
