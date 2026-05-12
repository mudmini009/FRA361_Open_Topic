# control.py — Keyboard-based mode / quit / pause logic
import keyboard

# ─── Key Bindings ──────────────────────────────────
QUIT_KEY  = 'z'
PAUSE_KEY = 'f9'

MODE_KEYS = {
    'x': 0,   # Idle   — no aim, no click
    'c': 1,   # Track  — aim follows target, no click
    'v': 2,   # Flick + Click — aim snaps and fires
}

MODE_NAMES = {
    0: "IDLE (Paused)",
    1: "TRACK (Aim Only)",
    2: "FLICK + CLICK (Aim & Fire)",
}

# ─── Internal State ───────────────────────────────
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
    for key, mode in MODE_KEYS.items():
        if keyboard.is_pressed(key):
            return mode
    return current_mode
