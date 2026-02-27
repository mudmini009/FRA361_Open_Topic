#keyboard-based mode/quit logic
# control.py
import keyboard

QUIT_KEY = 'z'
MODE_KEYS = {'x': 0, 'c': 1, 'v': 2}

def should_quit():
    return keyboard.is_pressed(QUIT_KEY)

def get_mode(current_mode):
    for key, m in MODE_KEYS.items():
        if keyboard.is_pressed(key):
            return m
    return current_mode
