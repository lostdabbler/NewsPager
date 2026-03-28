# ~/pi_dashboard/apps/system.py
import psutil
import curses
from apps.base import BaseApp

class SystemApp(BaseApp):
    def draw(self):
        self.stdscr.clear()
        # Header
        self.stdscr.addstr(0, 0, "SYSTEM STATUS", curses.A_BOLD)
        
        # CPU
        cpu = psutil.cpu_percent()
        self.stdscr.addstr(2, 0, f"CPU Usage: {cpu}%")
        # Draw a little bar chart
        bars = "|" * int(cpu / 5)
        self.stdscr.addstr(3, 0, f"[{bars:<20}]")

        # RAM
        ram = psutil.virtual_memory()
        self.stdscr.addstr(5, 0, f"RAM: {ram.percent}%")
        self.stdscr.addstr(6, 0, f"Used: {ram.used // 1024 // 1024} MB")
        
        # Disk
        disk = psutil.disk_usage('/')
        self.stdscr.addstr(8, 0, f"Disk: {disk.percent}%")

        # Instructions
        self.stdscr.addstr(10, 0, "system is on and displaying text", curses.A_DIM)
        self.stdscr.refresh()
