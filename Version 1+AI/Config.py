"""Config.py - every setting the game uses lives here.

Game.py, Settings.py and Main.py all read and write settings through this
module, so there is one source of truth instead of values being passed
around between files. Settings are saved to settings.json next to this file
and are loaded again the next time the game starts.
"""
import json
import os

SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")

# Options shown in the Settings screen
GRID_OPTIONS = ["8x8", "16x16", "25x20"]
MINE_OPTIONS = ["Easy", "Medium", "Hard"]
FLAG_OPTIONS = ["On", "Off"]

# Theme name: (main colour, light background colour)
THEMES = {
    "Teal": ("#008080", "#ceeddf"),
    "Ocean Blue": ("#1f5fbf", "#d4e4f7"),
    "Royal Purple": ("#6a3fb5", "#e3d9f3"),
    "Crimson": ("#b3243b", "#f6d9de"),
    "Sunset Orange": ("#d9600b", "#fbe3cf"),
    "Forest Green": ("#2e7d32", "#d9edd9"),
    "Charcoal": ("#37474f", "#dfe4e7"),
}
CUSTOM = "Custom"

USERNAME_MAX = 12

DEFAULTS = {
    "username": "Player",
    "theme": "Teal",
    "customColor": "#008080",
    "gridSize": "16x16",
    "mineLevel": "Medium",
    "flags": "On",
}

_values = dict(DEFAULTS)


# ---------- colour helpers ----------
def _rgb(colour):
    return int(colour[1:3], 16), int(colour[3:5], 16), int(colour[5:7], 16)


def isHexColour(colour):
    return (isinstance(colour, str) and len(colour) == 7 and colour[0] == "#"
            and all(ch in "0123456789abcdefABCDEF" for ch in colour[1:]))


def brightness(colour):
    """Perceived brightness from 0 (black) to 1 (white)."""
    r, g, b = _rgb(colour)
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255


def isTooLight(colour):
    """Headings are drawn in the theme colour on white, and buttons use white
    text on the theme colour, so very light colours would be unreadable."""
    return brightness(colour) > 0.6


def mixWithWhite(colour, amount):
    r, g, b = (round(c + (255 - c) * amount) for c in _rgb(colour))
    return f"#{r:02x}{g:02x}{b:02x}"


# ---------- username ----------
def usernameError(name):
    """Returns None if the name is fine, otherwise a message to show the user."""
    name = name.strip()
    if not name:
        return "Username cannot be empty."
    if len(name) > USERNAME_MAX:
        return f"Username must be {USERNAME_MAX} characters or fewer."
    if not all(ch.isalnum() or ch in " _-" for ch in name):
        return "Use letters, numbers, spaces, _ or - only."
    return None


# ---------- reading and writing settings ----------
def _isValid(key, value):
    if key == "username":
        return isinstance(value, str) and usernameError(value) is None
    if key == "theme":
        return value in THEMES or value == CUSTOM
    if key == "customColor":
        return isHexColour(value) and not isTooLight(value)
    if key == "gridSize":
        return value in GRID_OPTIONS
    if key == "mineLevel":
        return value in MINE_OPTIONS
    if key == "flags":
        return value in FLAG_OPTIONS
    return False


def get(key):
    return _values[key]


def update(**changes):
    """Change several settings at once. Raises ValueError for a bad value so
    mistakes show up straight away instead of being saved."""
    for key, value in changes.items():
        if key not in DEFAULTS or not _isValid(key, value):
            raise ValueError(f"Invalid setting: {key} = {value!r}")
    for key, value in changes.items():
        _values[key] = value.strip() if key == "username" else value


def load():
    """Read settings.json. Anything missing or invalid falls back to its default."""
    _values.clear()
    _values.update(DEFAULTS)
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            saved = json.load(file)
    except (OSError, ValueError):
        return
    if not isinstance(saved, dict):
        return
    for key, value in saved.items():
        if key in DEFAULTS and _isValid(key, value):
            _values[key] = value


def save():
    """Write settings.json. Returns False if the file could not be written."""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(_values, file, indent=4)
        return True
    except OSError:
        return False


def getTheme():
    """The colours the screens should use right now."""
    name = _values["theme"]
    if name == CUSTOM:
        main = _values["customColor"]
        light = mixWithWhite(main, 0.85)
    else:
        main, light = THEMES[name]
    return {"name": name, "main": main, "light": light}


load()
