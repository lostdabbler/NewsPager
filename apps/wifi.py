# ~/pi_dashboard/apps/wifi.py
import subprocess
import re
import curses
from apps.base import BaseApp

class WifiScannerApp(BaseApp):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.name = "WiFi Scan"
        self.networks = []
        self.view_mode = 0 # 0: List, 1: Bars, 2: Radar
        self.scan()

    def scan(self):
        try:
            # -q hides header, -s is for scan
            cmd = "sudo iwlist wlan0 scan | grep -E 'ESSID|Quality'"
            output = subprocess.check_output(cmd, shell=True).decode('utf-8')
            names = re.findall(r'ESSID:"(.*)"', output)
            qualities = re.findall(r'Quality=(\d+)/70', output)
            
            self.networks = []
            for name, qual in zip(names, qualities):
                if name.strip():
                    self.networks.append({'ssid': name, 'strength': int(qual)})
            self.networks.sort(key=lambda x: x['strength'], reverse=True)
        except:
            self.networks = [{"ssid": "Interface Busy", "strength": 0}]

    def handle_input(self, btn):
        if btn == 0: self.scan()             # Button A: Refresh
        if btn == 2: self.view_mode = (self.view_mode + 1) % 3 # Button C: View

    def draw(self):
        self.stdscr.erase()
        max_y, max_x = self.stdscr.getmaxyx()
        self.stdscr.addstr(0, 0, " WIFI RADAR ", curses.A_BOLD)

        if self.view_mode == 0: # LIST VIEW
            for i, net in enumerate(self.networks[:max_y-4]):
                self.stdscr.addstr(i+2, 0, f"{net['strength']:2d}", curses.color_pair(1))
                self.stdscr.addstr(i+2, 4, f"| {net['ssid'][:max_x-6]}")

        elif self.view_mode == 1: # BAR VIEW
            for i, net in enumerate(self.networks[:5]):
                bar_len = int((net['strength'] / 70) * (max_x - 15))
                bar = "█" * bar_len
                self.stdscr.addstr((i*2)+2, 0, f"{net['ssid'][:10]:<10}")
                self.stdscr.addstr((i*2)+2, 11, f"{bar}", curses.color_pair(1))

        elif self.view_mode == 2: # RADAR / SIGNAL METER
            if self.networks:
                best = self.networks[0]
                self.stdscr.addstr(2, 0, "STRONGEST SIGNAL:", curses.A_DIM)
                self.stdscr.addstr(3, 2, best['ssid'].upper(), curses.A_BOLD)
                # Big vertical bars
                level = int((best['strength'] / 70) * 5)
                for j in range(5):
                    char = "┃" if j < level else " "
                    self.stdscr.addstr(5, 5 + (j*2), char, curses.A_BOLD | curses.color_pair(1))

        self.stdscr.refresh()
