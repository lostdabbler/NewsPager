# ~/pi_dashboard/apps/spotify.py
import curses
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from apps.base import BaseApp

class SpotifyApp(BaseApp):
    def __init__(self, stdscr):
        # You'll need to set these in your environment or config
        scope = "user-modify-playback-state user-read-currently-playing"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=False))
        redirect_uri="http://127.0.0.1:8888/callback", # Must match dashboard
        open_browser=False
        
        self.track_name = "No Media"
        self.artist = ""
        self.is_playing = False
        super().__init__(stdscr)
        self.name = "Spotify"

    def update_data(self):
        """Background Thread: Keep track of what's playing"""
        try:
            current = self.sp.current_playback()
            if current and current['item']:
                self.track_name = current['item']['name']
                self.artist = current['item']['artists'][0]['name']
                self.is_playing = current['is_playing']
            else:
                self.track_name = "Nothing Playing"
        except:
            self.track_name = "Auth Error"

    def get_update_interval(self):
        return 5 # Refresh metadata every 5 seconds

    def action_a(self): # Button A: Back
        try: self.sp.previous_track()
        except: pass

    def action_b(self): # Button B: Forward
        try: self.sp.next_track()
        except: pass

    def action_c(self): # Button C: Play/Pause Toggle
        try:
            if self.is_playing: self.sp.pause_playback()
            else: self.sp.start_playback()
            self.update_data() # Force refresh
        except: pass

    def action_c_long(self):
        """Toggle Shuffle mode on Long Press"""
        try:
            # Check current shuffle state
            current = self.sp.current_playback()
            new_state = not current['shuffle_state']
            self.sp.shuffle(new_state)
            
            # Brief visual feedback
            self.stdscr.addstr(1, 1, f" SHUFFLE: {'ON' if new_state else 'OFF'} ", curses.A_REVERSE)
            self.stdscr.refresh()
            time.sleep(0.5)
        except:
            pass

    def draw(self):
        self.stdscr.erase()
        max_y, max_x = self.stdscr.getmaxyx()

        # Visualizer-style border
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.border()
        
        # Track Info
        status_icon = "▶" if self.is_playing else "II"
        self.stdscr.addstr(2, 2, f"{status_icon} NOW PLAYING", curses.A_BOLD)
        
        # Truncate strings to fit screen
        display_track = self.track_name[:max_x-6]
        display_artist = self.artist[:max_x-6]
        
        self.stdscr.addstr(4, 2, display_track, curses.color_pair(1))
        self.stdscr.addstr(5, 2, display_artist, curses.A_DIM)

        # Controls Legend
        self.stdscr.addstr(max_y-2, 2, "A:<< | B:>> | C:PLAY/PAUSE", curses.A_DIM)
        
        self.stdscr.attroff(curses.color_pair(1))
        self.stdscr.refresh()
