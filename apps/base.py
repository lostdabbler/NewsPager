# ~/pi_dashboard/apps/base.py
import threading
import time

class BaseApp:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.name = "Base"
        self.data = {}
        # Start a background thread if the app needs it
        threading.Thread(target=self._background_loop, daemon=True).start()

    def _background_loop(self):
        """Override this in child apps for background fetching"""
        while True:
            self.update_data()
            time.sleep(self.get_update_interval())

    def update_data(self):
        """The actual network/hardware call"""
        pass

    def get_update_interval(self):
        """How often to fetch data (in seconds)"""
        return 60

    def activate(self):
        self.stdscr.erase()
        self.stdscr.refresh()

    def handle_input(self, btn_idx):
        if btn_idx == 0: self.action_a()
        if btn_idx == 1: self.action_b()
        if btn_idx == 2: self.action_c()

    def action_a(self): pass
    def action_b(self): pass
    def action_c(self): pass
    def draw(self): pass
