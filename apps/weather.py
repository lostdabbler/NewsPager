# ~/pi_dashboard/apps/weather.py
import requests
import curses
from apps.base import BaseApp
import config

class WeatherApp(BaseApp):
    def update_data(self):
        try:
            res = requests.get(f"https://wttr.in/{config.LOCATION}?format=3", timeout=5)
            if res.status_code == 200:
                self.data['report'] = res.text.strip()
        except:
            self.data['report'] = "Offline / Connection Error"

    def get_update_interval(self):
        return 300 # Update weather every 5 minutes

    def draw(self):
        self.stdscr.erase()
        self.stdscr.addstr(0, 0, " WEATHER ", curses.A_BOLD)
        # Display the cached data instantly
        report = self.data.get('report', "Initialising...")
        self.stdscr.addstr(2, 0, report)
        self.stdscr.refresh()
