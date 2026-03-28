#!/bin/bash
# ~/pi_dashboard/launch_deck.sh

# 1. KILL everything Python and tmux
sudo pkill -9 python3
sudo pkill -9 python
tmux kill-server 2>/dev/null

# 2. EXPORT Terminal settings (Crucial for Curses at boot)
export TERM=linux
export TERMINFO=/lib/terminfo

# 3. LAUNCH main
cd /home/michael/pi_dashboard
python3 main.py
