# ~/pi_dashboard/apps/pwn.py
import requests
import curses
from requests.auth import HTTPBasicAuth
from apps.base import BaseApp

class PwnagotchiApp(BaseApp):
    def __init__(self, stdscr):
        self.status = {
            "face": "(⇀‿↼)",
            "status": "Initializing...",
            "pwned": "0",
            "level": "0"
        }
        # Use the credentials you set in /etc/pwnagotchi/config.toml
        self.auth = HTTPBasicAuth('admin', 'admin') 
        super().__init__(stdscr)
        self.name = "Pwny"

    def update_data(self):
        """Authenticated Background Fetch"""
        try:
            # We hit the local API
            r = requests.get(
                "http://127.0.0.1:8080/api/v1/status", 
                auth=self.auth, 
                timeout=2
            )
            if r.status_code == 200:
                data = r.json()
                self.status["face"] = data.get("face", "(•‿•)")
                self.status["status"] = data.get("status", "Idling")
                self.status["pwned"] = str(data.get("pwned_run", 0))
                self.status["level"] = str(data.get("lvl", 1))
            elif r.status_code == 401:
                self.status["status"] = "AUTH ERROR: Check config.toml"
        except Exception:
            self.status["status"] = "OFFLINE: Service Stopped"

    def draw(self):
        self.stdscr.erase()
        max_y, max_x = self.stdscr.getmaxyx()

        # Border
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.border()
        
        # Draw Face
        face = self.status["face"]
        self.stdscr.addstr(max_y//2 - 1, (max_x//2) - (len(face)//2), face, curses.A_BOLD)

        # Draw Status
        status_msg = self.status["status"][:max_x-6]
        self.stdscr.addstr(max_y//2 + 1, (max_x//2) - (len(status_msg)//2), status_msg)

        # Stats Line
        stats = f"P: {self.status['pwned']} L: {self.status['level']}"
        self.stdscr.addstr(max_y - 2, 2, stats, curses.A_DIM)
        
        self.stdscr.attroff(curses.color_pair(1))
        self.stdscr.refresh()
