from datetime import datetime, timezone, timedelta
import zoneinfo
from config import TEAMS_LIST, POSITIONS_LIST

def parse_date(date_string):
    if not date_string:
        return datetime.today()
    
    try:
        # Try ISO format first (YYYY-MM-DD)
        return datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        try:
            # Try MM/DD/YYYY format
            return datetime.strptime(date_string, "%m/%d/%Y")
        except ValueError:
            try:
                # Try M/D/YYYY format (without leading zeros)
                return datetime.strptime(date_string, "%m/%d/%Y")
            except ValueError:
                try:
                    # Try M/D/YY format (without leading zeros, 2-digit year)
                    return datetime.strptime(date_string, "%m/%d/%y")
                except ValueError:
                    raise ValueError(f"Invalid date format: {date_string}. Use YYYY-MM-DD, MM/DD/YYYY, or M/D/YY")
...

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

def hyphen_words(s=str):
    return s.lower().replace(" ", "-")
...

def validate_team_abbrev(abbrev):
    if not isinstance(abbrev, str) or len(abbrev) != 3:
        return False
    return abbrev.upper() in TEAMS_LIST
...

def parse_team_from_abbrev(abbrev, hyphen=False):
    team_name = TEAMS_LIST.get(abbrev.upper(), None)
    if hyphen and team_name:
        return team_name.lower().replace(" ", "-")
    return team_name
...

def position_code_to_name(code):
    return POSITIONS_LIST.get(code.upper(), "Unknown")
...