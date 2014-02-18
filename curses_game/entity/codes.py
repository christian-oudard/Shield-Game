from curses_game.entity.hero import Hero
from curses_game.entity.block import Block, HeavyBlock, SlideBlock
from curses_game.entity.polyomino import BlockPiece

ENTITY_CODES = {
    '_': None,
    '@': Hero,
    'O': Block,
    'H': HeavyBlock,
    'S': SlideBlock,
    'A': BlockPiece,
    'B': BlockPiece,
    'C': BlockPiece,
    'D': BlockPiece,
}
