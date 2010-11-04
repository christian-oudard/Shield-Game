from nose.tools import assert_equal

from textwrap import dedent

from main import load_level

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
