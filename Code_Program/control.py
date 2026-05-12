# control.py - Keyboard-based mode / quit / pause logic
import keyboard

QUIT_KEY  = 'f10'
PAUSE_KEY = 'f9'

MODE_KEYS = {
    'f1': 0,   # Idle - no aim, no click
    'f2': 1,   # Track - aim follows target, no click
    'f3': 2,   # Flick + Click - aim snaps and fires pulse clicks
}

MODE_NAMES = {
    0: "IDLE (Paused)",
    1: "TRACK (Aim Only)",
    2: "FLICK + CLICK (Aim & Fire)",
}

_paused = False


def should_quit():
    """Return True when the quit key is held."""
    return keyboard.is_pressed(QUIT_KEY)


def toggle_pause():
    """Flip the global pause flag (call on key edge, not hold)."""
    global _paused
    _paused = not _paused


def is_paused():
    """Return the current pause state."""
    return _paused


def get_mode(current_mode):
    """Check for mode-switch key presses; return new or current mode."""
    for key, m in MODE_KEYS.items():
        if keyboard.is_pressed(key):
            return m
    return current_mode
