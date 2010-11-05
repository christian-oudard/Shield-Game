from __future__ import print_function

from nose.tools import assert_equal

import os
from textwrap import dedent

from main import load_level
from move_shortcuts import *
from entity.polyomino import Piece
from entity.block import Block, HeavyBlock

import log
log.write = print

class MockDisplay(object):
    def show_bump(self):
        pass

def make_world(level_data):
    world = load_level(dedent(level_data))
    world.display = MockDisplay()
    return world

def show_world(world):
    height = max(y for x, y in world.terrain.keys()) + 1
    width = max(x for x, y in world.terrain.keys()) + 1
    for y in range(height):
        for x in range(width):
            c = ' '
            pos = (x, y)
            c = world.terrain.get(pos, c)
            entity = world.entity_at(pos)
            if entity:
                c = entity.display_character
            print(c, end='')
        print()

def test_load_level():
    world = make_world(
        '''
        .$
        #.
        @_
        __
        ''')
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
    world = make_world(
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
        ''')
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
    world = make_world(
        '''
        ..$
        @__
        ''')
    assert_equal(world.hero.pos, (0, 0))
    world.update(('move', east))
    assert_equal(world.hero.pos, (1, 0))
    world.update(('move', east))
    assert_equal(world.hero.pos, (2, 0))
    assert_equal(world.level_completed, True)

def test_shield_bump():
    world = make_world(
        '''
        ....
        ...#
        ....
        ____
        _@__
        ____
        ''')

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

def test_close_shield():
    world = make_world(
        '''
        ...
        ...
        ...
        ___
        _@_
        ___
        ''')

    # Nothing in the north square to start.
    assert_equal(world.entity_at((1, 0)), None)

    # Open the shield, the shield occupies the north square.
    world.update(('shield', north))
    piece = world.entity_at((1, 0))
    assert isinstance(piece, Piece)
    assert_equal(piece.polyomino, world.hero.polyomino)

    # Close the shield, the shield no longer occupies the north square.
    world.update(('shield', center))
    assert_equal(world.entity_at((1, 0)), None)

def test_open_shield_bump():
    world = make_world(
        '''
        ..
        ..
        .#
        @_
        __
        __
        ''')

    # Open the shield, it is blocked by the edge of the level.
    assert_equal(world.hero.pos, (0, 0))
    world.update(('shield', east))
    assert_equal(world.entity_at((1, 0)), None)

    # Move down.
    world.update(('move', south))
    assert_equal(world.hero.pos, (0, 1))

    # Open the shield, it is blocked by terrain.
    world.update(('shield', east))
    assert_equal(world.entity_at((1, 1)), None)

def test_block_push():
    world = make_world(
        '''
        ...
        @O_
        ''')

    assert_equal(world.hero.pos, (0, 0))
    assert_equal(world.entity_at((0, 0)), world.hero)
    block = world.entity_at((1, 0))
    assert_equal(block.pos, (1, 0))

    # Push the block east.
    world.update(('move', east))

    assert_equal(world.hero.pos, (1, 0))
    assert_equal(world.entity_at((1, 0)), world.hero)
    assert_equal(block.pos, (2, 0))
    assert_equal(world.entity_at((2, 0)), block)

    # Try to push the block east, but it bumps the wall.
    world.update(('move', east))

    assert_equal(world.hero.pos, (1, 0))
    assert_equal(world.entity_at((1, 0)), world.hero)
    assert_equal(block.pos, (2, 0))
    assert_equal(world.entity_at((2, 0)), block)

def test_heavy_block_push():
    world = make_world(
        '''
        ....
        ....
        ....
        ....
        ....
        ....
        @O__
        _H__
        _OO_
        _HH_
        _HO_
        _OH_
        ''')

    # Push a single light block.
    assert_equal(world.hero.pos, (0, 0))

    world.update(('move', east))
    assert_equal(world.hero.pos, (1, 0))
    block = world.entity_at((2, 0))
    assert isinstance(block, Block)

    # Push a single heavy block.
    world.update(('move', west))
    world.update(('move', south))
    assert_equal(world.hero.pos, (0, 1))

    world.update(('move', east))
    assert_equal(world.hero.pos, (1, 1))
    block = world.entity_at((2, 1))
    assert isinstance(block, HeavyBlock)

    # Push two light blocks.
    world.update(('move', west))
    world.update(('move', south))
    assert_equal(world.hero.pos, (0, 2))

    world.update(('move', east))
    assert_equal(world.hero.pos, (1, 2))
    block = world.entity_at((3, 2))
    assert isinstance(block, Block)

    # Can't push two heavy blocks.
    world.update(('move', west))
    world.update(('move', south))
    assert_equal(world.hero.pos, (0, 3))

    world.update(('move', east))
    assert_equal(world.hero.pos, (0, 3))
    assert_equal(world.entity_at((3, 3)), None)

    # Can't push a heavy block and a light block.
    world.update(('move', west))
    world.update(('move', south))
    assert_equal(world.hero.pos, (0, 4))

    world.update(('move', east))
    assert_equal(world.hero.pos, (0, 4))
    assert_equal(world.entity_at((3, 4)), None)

    world.update(('move', west))
    world.update(('move', south))
    assert_equal(world.hero.pos, (0, 5))

    world.update(('move', east))
    show_world(world)
    assert_equal(world.hero.pos, (0, 5))
    assert_equal(world.entity_at((3, 5)), None)
