from __future__ import print_function

from nose.tools import with_setup, assert_equal

from textwrap import dedent

from main import load_level

def setup():
    global log
    import log as _log
    _log.write = print
    log = _log

@with_setup(setup)
def test_load_level():
    world = load_level(dedent(
        '''
        3, 1
        ..$
        @__
        '''))
    assert_equal(world.level_completed, False)
    assert_equal(world.num_moves, 0)
    assert_equal(world.history, [])
    assert_equal(world.info_spaces, {})
    assert_equal(world.board_size, (3, 1))
    assert_equal(world.terrain, {(0, 0): '.', (1, 0): '.', (2, 0): '$'})

    assert_equal(len(world.entities), 9) # The hero and 8 shield pieces.
    hero = world.hero
    assert_equal(hero.pos, (0, 0))
    assert_equal(len(hero.shield_pieces), 8)
    assert hero in world.entities

@with_setup(setup)
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