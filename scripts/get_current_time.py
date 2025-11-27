"""
Get current time and save to session_time.txt for tracking.
This file is gitignored and used for accurate time tracking in commits.
"""

from datetime import datetime
from pathlib import Path

def get_current_time():
    """Get current time in HH:MM format."""
    return datetime.now().strftime("%H:%M")

def save_session_start():
    """Save session start time."""
    time_file = Path("session_time.txt")
    current = get_current_time()

    with open(time_file, 'w', encoding='utf-8') as f:
        f.write(f"Session Start: {current}\n")
        f.write(f"Last Update: {current}\n")

    print(f"📅 Session started at {current}")
    return current

def update_time():
    """Update last update time."""
    time_file = Path("session_time.txt")
    current = get_current_time()

    if time_file.exists():
        with open(time_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Keep session start, update last update
        with open(time_file, 'w', encoding='utf-8') as f:
            f.write(lines[0])  # Session Start
            f.write(f"Last Update: {current}\n")
    else:
        save_session_start()

    print(f"⏰ Current time: {current}")
    return current

def get_session_times():
    """Get session start and current time."""
    time_file = Path("session_time.txt")

    if not time_file.exists():
        return save_session_start(), get_current_time()

    with open(time_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start = lines[0].split(": ")[1].strip() if len(lines) > 0 else get_current_time()
    current = get_current_time()

    # Update last update time
    with open(time_file, 'w', encoding='utf-8') as f:
        f.write(f"Session Start: {start}\n")
        f.write(f"Last Update: {current}\n")

    return start, current

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "start":
        save_session_start()
    elif len(sys.argv) > 1 and sys.argv[1] == "get":
        start, current = get_session_times()
        print(f"Session: {start} - {current}")
    else:
        update_time()
