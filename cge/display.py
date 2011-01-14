import curses
import vec

class Display(object):
    def __init__(self, scr):
        # self.world set after initialization
        self.scr = scr
        self.origin = (0, 0)
        try:
            curses.curs_set(0)
        except:
            pass
        scr.refresh() # refresh right away so first call to stdscr.getch() doesn't overwrite the first draw()

    def refresh(self):
        self.scr.erase()
        self.draw()
        self.scr.refresh()

    def set_origin(self, x, y):
        self.origin_x, self.origin_y = self.origin = (x, y)

    def to_screen(self, pos):
        return vec.add(pos, self.origin)
