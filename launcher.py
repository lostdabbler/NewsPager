# ~/pi_dashboard/launcher.py
import time
import os
import sys
from gpiozero import Button

start_btn = Button(17, pull_up=True)

os.system('clear')
print("\n" * 5)
print(" " * 10 + "=========================")
print(" " * 10 + "    CYBERDECK  ONLINE    ")
print(" " * 10 + "=========================")
print("\n" * 2)
print(" " * 10 + "  [ PRESS BUTTON 1 ]     ")
print(" " * 10 + "      TO LAUNCH          ")

start_btn.wait_for_press()

print("Launching System...")
time.sleep(1)

# FIX: Set the working directory to the dashboard folder so imports work
os.chdir("/home/michael/pi_dashboard")

# FIX: Use sys.executable and pass the script path as the first argument in the list
os.execv(sys.executable, ["python3", "main.py"])
