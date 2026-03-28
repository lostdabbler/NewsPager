import curses
import subprocess
from apps.base import BaseApp

class NetworkApp(BaseApp):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.name = "Network Info"

    def get_ip(self, cmd):
        try:
            return subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        except:
            return "Not Connected"

    def draw(self):
        self.stdscr.clear()
        local_ip = self.get_ip("hostname -I | cut -d' ' -f1")
        tail_ip = self.get_ip("tailscale ip -4")

        self.stdscr.addstr(0, 0, " NETWORK ", curses.A_BOLD)
        
        self.stdscr.addstr(2, 0, "LOCAL IP:", curses.A_DIM)
        self.stdscr.addstr(3, 2, local_ip, curses.A_BOLD)
        
        self.stdscr.addstr(5, 0, "TAILSCALE:", curses.A_DIM)
        self.stdscr.addstr(6, 2, tail_ip, curses.A_BOLD)
        
        self.stdscr.refresh()
