import curses, random
from apps.base import BaseApp

class MatrixApp(BaseApp):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.rows, self.cols = stdscr.getmaxyx()
        self.drops = [random.randint(0, self.rows) for _ in range(self.cols)]

    def draw(self):
        # Instead of clear(), we draw "dim" spaces to create a trail
        for i in range(self.cols):
            char = chr(random.randint(33, 126))
            try:
                # Lead character (Bright)
                self.stdscr.addstr(self.drops[i], i, char, curses.color_pair(1) | curses.A_BOLD)
                # Trail character (Delete previous)
                cleanup_row = (self.drops[i] - 1) % self.rows
                self.stdscr.addstr(cleanup_row, i, " ")
            except: pass

            self.drops[i] = (self.drops[i] + 1) % self.rows
            if random.random() > 0.95: self.drops[i] = 0
        self.stdscr.refresh()
