#!/bin/bash

# 1. Wait for the Pi to finish booting (Network/Screen drivers)
sleep 10

# 2. Force the terminal type so Curses knows how to draw
export TERM=linux

# 3. Go to the right folder
cd /home/michael/pi_dashboard

# 4. Run the app and log any errors to a file (just in case)
/usr/bin/python3 main.py > dashboard.log 2>&1
