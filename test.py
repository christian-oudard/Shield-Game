from __future__ import print_function

from nose.tools import assert_equal

import os
from textwrap import dedent

from main import load_level
from move_shortcuts import *

import log
log.write = print


class MockDisplay(object):
    def show_bump(self):
        pass


def test_load_level():
    world = load_level(dedent(
        '''
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
        ..$
        @__
        '''))
    assert_equal(world.hero.pos, (0, 0))
    world.update(('move', east))
    assert_equal(world.hero.pos, (1, 0))
    world.update(('move', east))
    assert_equal(world.hero.pos, (2, 0))
    assert_equal(world.level_completed, True)

def test_shield_bump():
    world = load_level(dedent(
        '''
        ....
        ...#
        ....
        ____
        _@__
        ____
        '''))
    world.display = MockDisplay()

    assert_equal(world.hero.pos, (1, 1))

    # Before opening the shield, he can move left and right.
    world.update(('move', west))
    assert_equal(world.hero.pos, (0, 1))
    world.update(('move', east))

    world.update(('move', east))
    assert_equal(world.hero.pos, (2, 1))
    world.update(('move', west))

    assert_equal(world.hero.pos, (1, 1))

    # After opening the shield right, he can move left, but not right.
    world.update(('shield', east))

    world.update(('move', west))
    assert_equal(world.hero.pos, (0, 1))
    world.update(('move', east))

    world.update(('move', east))
    assert_equal(world.hero.pos, (1, 1)) # Blocked on wall tile.

    # After opening the shield left, he can move right, but not left.
    world.update(('shield', west))

    world.update(('move', east))
    assert_equal(world.hero.pos, (2, 1))
    world.update(('move', west))

    world.update(('move', west))
    assert_equal(world.hero.pos, (1, 1)) # Blocked on level edge.
