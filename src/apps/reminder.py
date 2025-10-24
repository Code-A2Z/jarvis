"""
File: reminder.py
Author: Sohum Seth
Feature: Simple Reminder Feature for Jarvis
Description:
This module allows Jarvis to set a reminder at a specific time.
"""

import datetime
import time

def setReminder():
    """
    Ask the user for a time and message, then alert them at the scheduled time.
    """
    reminder_time = input("Enter reminder time (HH:MM, 24-hour format): ")
    reminder_message = input("Enter reminder message: ")
    print(f"✅ Reminder set for {reminder_time}: {reminder_message}")

    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == reminder_time:
            print(f"⏰ Reminder: {reminder_message}")
            break
        time.sleep(30)

if __name__ == "__main__":
    setReminder()
