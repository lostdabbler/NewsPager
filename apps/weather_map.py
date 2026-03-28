# ~/pi_dashboard/apps/weather_map.py
import requests
import curses
import config
from apps.base import BaseApp

class WeatherMapApp(BaseApp):
    def __init__(self, stdscr):
        self.map_data = "Initialising Radar..."
        super().__init__(stdscr)
        self.name = "Weather Radar"

    def update_data(self):
        """Background Thread: Fetch the detailed ASCII weather condition"""
        try:
            # ?0 = current condition only, ?n = narrow version (good for small screens)
            # Use format=v2 or just the URL without format for full ASCII art
            url = f"https://wttr.in/{config.LOCATION}?0&n&T"
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                self.map_data = res.text
        except:
            self.map_data = "DATA_LINK_FAILURE: Check Network"

    def get_update_interval(self):
        return 900 # Refresh every 15 minutes

    def draw(self):
        self.stdscr.erase()
        # No header needed, the wttr.in art is its own header
        
        # We split the map_data into lines and print them
        lines = self.map_data.split('\n')
        for i, line in enumerate(lines):
            if i < curses.LINES - 1:
                # Use COLOR_PAIR(1) for that green phosphor look
                self.stdscr.addstr(i, 0, line[:curses.COLS-1], curses.color_pair(1))
        
        self.stdscr.refresh()
