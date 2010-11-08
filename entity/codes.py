from hero import Hero
from block import Block, HeavyBlock
from polyomino import BlockPiece

ENTITY_CODES = {
    '_': None,
    '@': Hero,
    'O': Block,
    'H': HeavyBlock,
    'A': BlockPiece,
    'B': BlockPiece,
    'C': BlockPiece,
    'D': BlockPiece,
}
