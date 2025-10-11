import zoneinfo
from datetime import datetime, timezone, timedelta
from data import TEAMS_LIST, POSITIONS_LIST

# Common Utility Functions

def format_utc_to_est(dt, format="%m/%d/%Y %I:%M %p"):
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except ValueError:
            dt = parse_date(dt)
    try:
        eastern = zoneinfo.ZoneInfo("America/New_York")
    except (ImportError, KeyError):
        try:
            import pytz
            eastern = pytz.timezone("America/New_York")
        except ImportError:
            eastern = timezone(timedelta(hours=-5))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    dt_est = dt.astimezone(eastern)
    return dt_est.strftime(format)
...

def hyphen_words(s):
    return s.lower().replace(" ", "-")
...

def hex_to_rgb(hex_color):
    """Convert hex color string to an (R, G, B) tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
...


# Custom NHL Utility Functions

def validate_team_abbrev(abbrev):
    if not isinstance(abbrev, str) or len(abbrev) != 3:
        return False
    return abbrev.upper() in TEAMS_LIST.keys()
...

def position_code_to_name(code):
    return POSITIONS_LIST.get(code.upper(), "Unknown")
...