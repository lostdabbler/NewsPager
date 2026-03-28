# ~/pi_dashboard/apps/clock.py
import time
import curses
from apps.base import BaseApp

class ClockApp(BaseApp):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.name = "Mainframe"

    def draw(self):
        self.stdscr.erase()
        max_y, max_x = self.stdscr.getmaxyx()
        
        # 1. Draw Cyber-Border
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.border()
        self.stdscr.addstr(0, 2, " [ DECK: ONLINE ] ", curses.A_BOLD)
        self.stdscr.addstr(max_y-1, max_x-15, " v3.0-STABLE ", curses.A_DIM)
        
        # 2. Get Time Strings
        t_str = time.strftime("%H:%M:%S")
        d_str = time.strftime("%A, %d %b %Y")
        
        # 3. Center and Draw the Clock
        # We use large block-ish text for the time
        time_y = max_y // 2 - 1
        time_x = (max_x // 2) - (len(t_str) // 2)
        
        self.stdscr.addstr(time_y, time_x, t_str, curses.A_BOLD | curses.A_REVERSE)
        self.stdscr.addstr(time_y + 2, (max_x // 2) - (len(d_str) // 2), d_str, curses.A_DIM)
        
        # 4. Small System Info Corners
        self.stdscr.addstr(2, 2, "SYS_LNK: ESTABLISHED", curses.A_DIM)
        self.stdscr.addstr(3, 2, "LOC: 32.92° S, 151.77° E", curses.A_DIM) # Newcastle coordinates
        
        self.stdscr.attroff(curses.color_pair(1))
        self.stdscr.refresh()
