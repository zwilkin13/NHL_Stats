from datetime import datetime, timezone, timedelta
import zoneinfo

TEAMS_LIST = {
    "ANA": "Anaheim Ducks",
    "ARI": "Arizona Coyotes",
    "BOS": "Boston Bruins",
    "BUF": "Buffalo Sabres",
    "CGY": "Calgary Flames",
    "CAR": "Carolina Hurricanes",
    "CHI": "Chicago Blackhawks",
    "COL": "Colorado Avalanche",
    "CBJ": "Columbus Blue Jackets",
    "DAL": "Dallas Stars",
    "DET": "Detroit Red Wings",
    "EDM": "Edmonton Oilers",
    "FLA": "Florida Panthers",
    "LAK": "Los Angeles Kings",
    "MIN": "Minnesota Wild",
    "MTL": "Montreal Canadiens",
    "NSH": "Nashville Predators",
    "NJD": "New Jersey Devils",
    "NYI": "New York Islanders",
    "NYR": "New York Rangers",
    "OTT": "Ottawa Senators",
    "PHI": "Philadelphia Flyers",
    "PIT": "Pittsburgh Penguins",
    "SJS": "San Jose Sharks",
    "SEA": "Seattle Kraken",
    "STL": "St. Louis Blues",
    "TBL": "Tampa Bay Lightning",
    "TOR": "Toronto Maple Leafs",
    "VAN": "Vancouver Canucks",
    "VGK": "Vegas Golden Knights",
    "WPG": "Winnipeg Jets"
}

def format_date(date, format="%m/%d/%Y"):
    import datetime
    if isinstance(date, (int, float)):
        dt = datetime.datetime.fromtimestamp(date)
    elif isinstance(date, str):
        try:
            dt = datetime.datetime.fromisoformat(date)
        except ValueError:
            dt = datetime.datetime.strptime(date, "%Y-%m-%d")
    elif isinstance(date, datetime.datetime):
        dt = date
    elif isinstance(date, datetime.date):
        dt = datetime.datetime.combine(date, datetime.time())
    else:
        raise TypeError("Unsupported date type")

    # Format with zero-padded month/day, then remove leading zeros
    formatted = dt.strftime(format)
    # Remove leading zero from month and day
    parts = formatted.split('/')
    if len(parts) == 3:
        parts[0] = str(int(parts[0]))  # month
        parts[1] = str(int(parts[1]))  # day
        formatted = '/'.join(parts)
    return formatted
...

def is_date_string(val):
    import re

    """
    Check if a string value looks like an ISO date format
    """
    if not isinstance(val, str):
        return False
    # Check for ISO date pattern: YYYY-MM-DDTHH:MM:SS.fff or similar
    date_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$'
    return bool(re.match(date_pattern, val))
...

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

def validate_team_abbrev(abbrev):
    if not isinstance(abbrev, str) or len(abbrev) != 3:
        return False
    return abbrev.upper() in TEAMS_LIST

def parse_team_from_abbrev(abbrev, hyphen=False):
    
    team_name = TEAMS_LIST.get(abbrev.upper(), None)
    if hyphen and team_name:
        return team_name.lower().replace(" ", "-")
    return team_name
...

def hyphen_words(s):
    return s.lower().replace(" ", "-")
...