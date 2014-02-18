import time
from curses_game.display import Display
from curses_game.terrain_constants import FLOOR

class GameDisplay(Display):
    def __init__(self, *args, **kwargs):
        super(GameDisplay, self).__init__(*args, **kwargs)
        self.set_origin(3, 2)

    def draw(self):
        board_x, board_y = self.world.board_size
        self.show_info()
        self.scr.addstr(0, 0, str(self.world.num_moves))#DEBUG
        for pos, ter in self.world.terrain.items():
            if ter == FLOOR:
                ter = ' '
            x, y = self.to_screen(pos)
            self.scr.addch(y, x, ter)
        for e in self.world.entities:
            if not e.solid:
                continue
            x, y = self.to_screen(e.pos)
            self.scr.addch(y, x, e.display_character)

    def show_bump(self):
        self.refresh()
        time.sleep(.2)

    def show_message(self, message):
        board_x, board_y = self.world.board_size
        self.scr.addstr(self.origin_y + board_y + 2, 0, message)

    def show_info(self):
        info = self.world.info_spaces.get(self.world.hero.pos)
        if info:
            self.show_message(info)
