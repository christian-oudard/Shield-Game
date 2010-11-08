from hero import Hero
from block import Block, HeavyBlock, SlideBlock
from polyomino import BlockPiece

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
