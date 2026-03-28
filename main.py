import curses
import time
import os
from gpiozero import Button
import config
from PIL import Image
import subprocess

def run_cyber_splash(stdscr):
    try:
        max_y, max_x = stdscr.getmaxyx()
        # 1. Load the image and convert to ASCII
        img = Image.open("splash.png").convert('L')
        img = img.resize((max_x, max_y - 4)) # Leave room for text
        
        chars = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]
        
        stdscr.clear()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                pixel = img.getpixel((x, y))
                char = chars[pixel // 26]
                stdscr.addstr(y, x, char, curses.color_pair(1))
        
        # 2. Add some "Michael's Deck" flavor text
        stdscr.addstr(max_y-3, 2, ">> STZ_MAINFRAME BOOT v3.0", curses.A_BOLD)
        stdscr.addstr(max_y-2, 2, f">> IP: {subprocess.getoutput('hostname -I').split()[0]}", curses.A_DIM)
        
        stdscr.refresh()
        time.sleep(2.5) # Let the glory sink in
    except Exception as e:
        # If the image is missing, just show a cool text fallback
        stdscr.erase()
        stdscr.addstr(max_y//2, (max_x-15)//2, "DECK INITIALIZED", curses.A_REVERSE)
        stdscr.refresh()
        time.sleep(1)

# --- SPOTIFY ENV SETUP ---
# Pulls from your .bash_profile (system env) or config.py
os.environ['SPOTIPY_CLIENT_ID'] = os.getenv('SPOTIPY_CLIENT_ID', getattr(config, 'SPOTIPY_CLIENT_ID', ''))
os.environ['SPOTIPY_CLIENT_SECRET'] = os.getenv('SPOTIPY_CLIENT_SECRET', getattr(config, 'SPOTIPY_CLIENT_SECRET', ''))
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'

# --- APP IMPORTS ---
from apps.news import NewsApp
from apps.system import SystemApp
from apps.network import NetworkApp
from apps.matrix import MatrixApp
from apps.clock import ClockApp
from apps.wifi import WifiScannerApp
from apps.quiz import QuizApp
from apps.weather_map import WeatherMapApp
#from apps.spotify import SpotifyApp
from apps.pwn import PwnagotchiApp
from apps.brightness import BrightnessApp
from apps.epub import EpubApp

def main(stdscr):
    # 1. Curses Init
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

# RUN THE SPLASH
    run_cyber_splash(stdscr)

    # 2. Hardware Setup
    # Defined inside main so they can be closed on exit
    btn_swap = Button(config.PIN_SWAP, pull_up=True)
    btn_a = Button(config.PIN_A, pull_up=True)
    btn_b = Button(config.PIN_B, pull_up=True)
    btn_c = Button(config.PIN_C, pull_up=True)
    
    buttons = [btn_swap, btn_a, btn_b, btn_c]

    # 3. App Registry
    apps = [
        ClockApp(stdscr), 
        NewsApp(stdscr), 
        NetworkApp(stdscr), 
        BrightnessApp(stdscr),
        QuizApp(stdscr), 
        SystemApp(stdscr), 
        WeatherMapApp(stdscr),
        WifiScannerApp(stdscr),
        MatrixApp(stdscr),
        EpubApp(stdscr),
        #SpotifyApp(stdscr),
        PwnagotchiApp(stdscr)
    ]

    current_idx = 0
    active_app = apps[current_idx]
    last_swap_time = 0
    last_draw_time = 0

    stdscr.clear()

    try:
        while True:
            now = time.time()

            # --- SWAP LOGIC ---
            if btn_swap.is_pressed:
                if (now - last_swap_time > 0.5):
                    current_idx = (current_idx + 1) % len(apps)
                    active_app = apps[current_idx]
                    
                    stdscr.erase()
                    stdscr.addstr(0, 0, f">> LOADING: {active_app.name.upper()} <<", curses.A_BOLD)
                    stdscr.refresh()
                    
                    try: active_app.activate()
                    except: pass
                    
                    last_swap_time = now
                    last_draw_time = 0 
                    continue 

            # --- INPUT HANDLING (Short vs Long Press on C) ---
            if btn_a.is_pressed:
                active_app.handle_input(0)
                time.sleep(0.2)
                last_draw_time = 0
            
            elif btn_b.is_pressed:
                active_app.handle_input(1)
                time.sleep(0.2)
                last_draw_time = 0

            elif btn_c.is_pressed:
                # Timer for Long Press
                press_start = time.time()
                while btn_c.is_pressed:
                    time.sleep(0.05)
                
                duration = time.time() - press_start
                
                if duration > 1.0: # Long Press
                    if hasattr(active_app, 'action_c_long'):
                        active_app.action_c_long()
                    else:
                        active_app.handle_input(2)
                else: # Short Press
                    active_app.handle_input(2)
                
                last_draw_time = 0

            # --- DRAW LOGIC ---
            refresh_rate = 0.05 if isinstance(active_app, (MatrixApp, ClockApp)) else 1.0
            
            if now - last_draw_time > refresh_rate:
                try:
                    active_app.draw()
                    last_draw_time = now
                except Exception as e:
                    stdscr.addstr(0, 0, f"Error: {str(e)[:20]}", curses.color_pair(2))
                    stdscr.refresh()

            # Keyboard fallback
            ch = stdscr.getch()
            if ch == ord('q'): break
            
            time.sleep(0.01)

    finally:
        # CLEANUP: Crucial to prevent 'GPIO busy' on next run
        for b in buttons:
            b.close()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\n[!] Deck stopped by user.")
    except Exception as e:
        print(f"\n[!] System Crash: {e}")
