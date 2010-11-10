from __future__ import print_function

from nose.tools import assert_equal, assert_raises

import os
from textwrap import dedent
from StringIO import StringIO

from main import load_level, save_replay, load_replay
from move_shortcuts import *
from entity.polyomino import Piece
from entity.block import Block, HeavyBlock, SlideBlock

class MockDisplay(object):
    def show_bump(self):
        pass

def make_world(level_data):
    world = load_level(dedent(level_data))
    world.display = MockDisplay()
    return world

def show_world(world):
    lines = []
    height = max(y for x, y in world.terrain.keys()) + 1
    width = max(x for x, y in world.terrain.keys()) + 1
    for y in range(height):
        line = []
        for x in range(width):
            c = ' '
            pos = (x, y)
            c = world.terrain.get(pos, c)
            entity = world.entity_at(pos)
            if entity:
                c = entity.display_character
            line.append(c)
        lines.append(''.join(line))
    return '\n'.join(lines)

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
        note one. with an exclamation! and stuff.

        !i 2, 2
        note two
        ''')
    assert_equal(world.board_size, (3, 3))
    assert_equal(world.terrain[(1, 1)], 'i')
    assert_equal(world.terrain[(2, 2)], 'i')
    assert_equal(
        world.info_spaces,
        {
            (1, 1): 'note one. with an exclamation! and stuff.',
            (2, 2): 'note two',
        },
    )

def test_load_level_whitespace():
    # Respect leading whitespace in game levels.
    # Ignore terrain in the entity layer.
    world = make_world(
        '''
         ####
        ##..#
        #..##
        ####
         ####
        ##..#
        #@.##
        ####
        ''')
    assert_equal(
        show_world(world),
        dedent(
            '''\
             ####
            ##..#
            #@.##
            #### ''')
    )

def test_load_level_illegal_terrain():
    # Don't allow undefined terrain types.
    assert_raises(KeyError, lambda: make_world(
        '''
        K
        @
        '''))

def test_load_level_illegal_entities():
    # Don't allow undefined entity types.
    assert_raises(KeyError, lambda: make_world(
        '''
        ..
        @K
        '''))

def test_load_level_info_wrong_square():
    assert_raises(AssertionError, lambda: make_world(
        '''
        .
        @

        !i 0, 0
        this note is for a square with no info marker
        '''))

def test_load_level_sanity():
    assert_raises(AssertionError, lambda: make_world(
        '''
        #.
        @_
        '''))

def test_solve_all_game_levels():
    all_levels = []
    for dirpath, dirnames, filenames in os.walk('levels'):
        for filename in filenames:
            if filename.startswith('.'):
                continue
            if filename.endswith('.solution'):
                continue

            # Load the level, and make sure there are no errors.
            assert filename not in all_levels
            all_levels.append(filename)

            file_path = os.path.join(dirpath, filename)
            with open(file_path) as f:
                level_string = f.read()
            world = make_world(level_string)

            # Replay the solution, and ensure that it solves the level.
            with open(file_path + '.solution') as f:
                replay = load_replay(f)
            try:
                for i, move in enumerate(replay):
                    assert world.update(move), 'Solution bumped on move #%d' % (i + 1)
                assert world.level_completed, 'Level not completed'
            except AssertionError:
                print(move)
                print(show_world(world))
                raise
    # Check that all levels are listed in the level sequence.
    with open('sequence') as f:
        sequence = f.read()
    sequence_levels = []
    for line in sequence.splitlines():
        if line.strip() and not line.startswith('#'):
            sequence_levels.append(line)

    for level in sequence_levels:
        assert level in all_levels, 'Unknown level listed in level sequence: %s' % level
    for level in all_levels:
        assert level in sequence_levels, 'Level missing from sequence: %s' % level

def test_undo():
    world = make_world(
        '''
        ....$
        @_O__
        ''')
    world.undo()
    assert_equal(
        show_world(world),
        '@.O.$',
    )
    world.update(('move', east))
    world.update(('move', east))
    assert_equal(
        show_world(world),
        '..@O$',
    )
    world.undo()
    assert_equal(
        show_world(world),
        '.@O.$',
    )
    world.undo()
    world.undo() # Try to undo past the beginning.
    assert_equal(
        show_world(world),
        '@.O.$',
    )

def test_restart():
    world = make_world(
        '''
        ....$
        @____
        ''')
    assert_equal(
        show_world(world),
        '@...$',
    )
    world.restart()
    assert_equal(
        show_world(world),
        '@...$',
    )
    world.update(('move', east))
    world.update(('move', east))
    assert_equal(
        show_world(world),
        '..@.$',
    )
    world.restart()
    assert_equal(
        show_world(world),
        '@...$',
    )

def test_save_load_replay():
    replay = [
        ('move', north),
        ('move', south),
        ('move', east),
        ('move', west),
        ('move', northeast),
        ('move', southeast),
        ('move', southwest),
        ('move', northwest),
        ('move', center),
        ('shield', north),
        ('shield', south),
        ('shield', east),
        ('shield', west),
        ('shield', northeast),
        ('shield', southeast),
        ('shield', southwest),
        ('shield', northwest),
        ('shield', center),
    ]
    f = StringIO()
    save_replay(replay, f)
    f.seek(0)
    assert_equal(
        f.buf,
        dedent(
            '''\
            mn
            ms
            me
            mw
            mne
            mse
            msw
            mnw
            mc
            sn
            ss
            se
            sw
            sne
            sse
            ssw
            snw
            sc
            ''')
    )
    new_replay = load_replay(f)
    assert_equal(replay, new_replay)

def test_move_command_goal():
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
    assert_equal(world.hero.pos, (0, 5))
    assert_equal(world.entity_at((3, 5)), None)

def test_slide_block():
    # A slide block slides until it hits something when it is pushed.
    world = make_world(
        '''
        .....
        @S___
        ''')
    block = world.entity_at((1, 0))
    assert isinstance(block, SlideBlock)
    assert_equal(
        show_world(world),
        '@S...',
    )
    world.update(('move', east))
    assert_equal(block.pos, (4, 0))
    assert_equal(
        show_world(world),
        '.@..S',
    )

def test_slide_block_push():
    # A slide block does not push other blocks during its slide.
    world = make_world(
        '''
        ......
        @S__O_
        ''')
    assert_equal(
        show_world(world),
        '@S..O.',
    )
    world.update(('move', east))
    assert_equal(
        show_world(world),
        '.@.SO.',
    )

def test_slide_block_transmit_push():
    # A slide block does push other blocks before it starts sliding.
    world = make_world(
        '''
        ....
        @SO_
        ''')
    assert_equal(
        show_world(world),
        '@SO.',
    )
    world.update(('move', east))
    assert_equal(
        show_world(world),
        '.@SO',
    )

def test_slide_block_get_pushed():
    # A slide block will continue when pushed by another block.
    world = make_world(
        '''
        ......
        @OS___
        ''')
    assert_equal(
        show_world(world),
        '@OS...',
    )
    world.update(('move', east))
    assert_equal(
        show_world(world),
        '.@O..S',
    )

def test_slide_block_water():
    # A slide block reacts normally when pushed into water.
    world = make_world(
        '''
        ..~
        @S_
        ''')
    block = world.entity_at((1, 0))
    assert_equal(
        show_world(world),
        '@S~',
    )
    world.update(('move', east))
    assert_equal(
        show_world(world),
        '.@.',
    )
    assert_equal(block.pos, (2, 0))
    assert_equal(block.solid, False)

def test_slide_block_water():
    # A slide block reacts normally when sliding into water.
    world = make_world(
        '''
        ...~
        @S__
        ''')
    assert_equal(
        show_world(world),
        '@S.~',
    )
    world.update(('move', east))
    assert_equal(
        show_world(world),
        '.@..',
    )

def test_slide_carom():
    # A slide block will transfer momentum to another slide block.
    world = make_world(
        '''
        ......
        @S__S_
        ''')
    assert_equal(
        show_world(world),
        '@S..S.',
    )
    world.update(('move', east))
    assert_equal(
        show_world(world),
        '.@.S.S',
    )

def test_slide_carom_multiple():
    # A slide block will transfer momentum to another slide block.
    world = make_world(
        '''
        ........
        @S__SS__
        ''')
    assert_equal(
        show_world(world),
        '@S..SS..',
    )
    world.update(('move', east))
    assert_equal(
        show_world(world),
        '.@.SS..S',
    )

def test_slide_block_push_multiple_left():
    # Regression test: Push a slide block in a row with a normal block twice.
    world = make_world(
        '''
        .....
        @SO__
        ''')
    assert_equal(
        show_world(world),
        '@SO..',
    )
    world.update(('move', east))
    world.update(('move', east))
    assert_equal(
        show_world(world),
        '..@SO',
    )

def test_slide_block_bump():
    # Push a slide block into a wall.
    world = make_world(
        '''
        ..#
        @S_
        ''')
    assert_equal(
        show_world(world),
        '@S#',
    )
    world.update(('move', east))
    assert_equal(
        show_world(world),
        '@S#',
    )

def test_polyomino_push_loop():
    world = make_world(
        '''
        ....
        ....
        ....
        AA_O
        @___
        ____
        ''')
    assert_equal(
        show_world(world),
        dedent(
            '''\
            AA.O
            @...
            ....''')
    )
    world.update(('shield', east))
    assert_equal(
        show_world(world),
        dedent(
            '''\
            AA.O
            @...
            ....''')
    )

    world = make_world(
        '''
        .....
        .....
        .....
        _____
        A@A_O
        _____
        ''')
    assert_equal(
        show_world(world),
        dedent(
            '''\
            .....
            A@A.O
            .....''')
    )
    world.update(('shield', east))
    assert_equal(
        show_world(world),
        dedent(
            '''\
            .....
            A@A.O
            .....''')
    )
