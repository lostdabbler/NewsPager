#!/bin/bash
# Wait for the system to settle (prevents the 'GPIO busy' error)
sleep 5

# Kill any ghost processes that might be hogging pins
#sudo pkill -9 -f deck_buttons.py
#sudo pkill -9 -f main.py

# Launch the dashboard directly onto the screen
#python3 /home/michael/pi_dashboard/main.py > /dev/tty1 < /dev/tty1

cy-reload
