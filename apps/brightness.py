import curses
from gpiozero import PWMOutputDevice
from apps.base import BaseApp

# GPIO 18 is the standard backlight pin for Adafruit 2.2" HATs
# We use a global variable so the brightness stays set when you switch apps
backlight = PWMOutputDevice(18, initial_value=1.0)

class BrightnessApp(BaseApp):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.name = "Brightness"
        # Start at 100% (1.0)
        self.current_level = backlight.value

    def update_brightness(self):
        # Clamp value between 0.1 (so you don't go pitch black) and 1.0
        self.current_level = max(0.1, min(1.0, self.current_level))
        backlight.value = self.current_level
        self.draw()

    def action_a(self):
        # Button A: Decrease Brightness
        self.current_level -= 0.1
        self.update_brightness()

    def action_b(self):
        # Button B: Increase Brightness
        self.current_level += 0.1
        self.update_brightness()

    def draw(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "SCREEN BRIGHTNESS", curses.A_BOLD)
        
        # Draw a visual bar: [**********-----]
        percent = int(self.current_level * 100)
        bars = int(self.current_level * 15)
        visual_bar = "=" * bars + "-" * (15 - bars)
        
        self.stdscr.addstr(2, 0, f"[{visual_bar}] {percent}%")
        self.stdscr.addstr(4, 0, "Btn A: Darker")
        self.stdscr.addstr(5, 0, "Btn B: Brighter")
        self.stdscr.refresh()
