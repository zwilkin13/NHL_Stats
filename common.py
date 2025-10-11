import os
from datetime import datetime, timezone, timedelta
import zoneinfo
from config import TEAMS_LIST, POSITIONS_LIST
from dotenv import load_dotenv
load_dotenv()

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

def hyphen_words(s):
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

def resolve_json_file_path(filename):
    import os
    # If it's already an absolute path or contains path separators, use as-is
    if os.path.isabs(filename) or os.sep in filename or '/' in filename:
        if os.path.exists(filename):
            return filename
        else:
            raise FileNotFoundError(f"File not found: {filename}")
    
    # Check current directory first
    if os.path.exists(filename):
        return filename
    
    # Check json_samples directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_samples_path = os.path.join(script_dir, "json_samples", filename)
    
    if os.path.exists(json_samples_path):
        return json_samples_path
    
    # If not found in either location, raise FileNotFoundError
    raise FileNotFoundError(f"File '{filename}' not found in current directory or json_samples directory")
...

def load_json_file(file_path):
    import json
    import sys
    try:
        with open(file_path, "r") as f:
            file_content = f.read()
            if not file_content.strip():
                raise ValueError("The provided file is empty.")
            return json.loads(file_content)
    except ValueError as e:
        sys.exit(f"Error reading JSON file: {e}")
    except FileNotFoundError:
        sys.exit(f"File not found: {file_path}")
    except json.JSONDecodeError:
        sys.exit(f"Error decoding JSON from file: {file_path}")
    return

    import os, sys
    try:
        print(f"⏳ Updating Azure cookies from azure_cookies.json...")
        file_path = resolve_json_file_path("azure_cookies.json")
        config_path = os.path.join(os.path.dirname(__file__), "config.py")

        with open(config_path, "r") as f:
            lines = f.readlines()

        cookie_objects = load_json_file(file_path)
        cookie_dict = {}
        for cookie_obj in cookie_objects:
            if isinstance(cookie_obj, dict) and 'name' in cookie_obj and 'value' in cookie_obj:
                cookie_dict[cookie_obj['name']] = cookie_obj['value']

        with open(config_path, "w") as f:
            i = 0
            while i < len(lines):
                line = lines[i]
                
                if line.strip().startswith("CookieBase"):
                    f.write(line)
                    i += 1
                    
                    while i < len(lines):
                        line = lines[i]
                        if "cookies=" in line:
                            indent = len(line) - len(line.lstrip())
                            f.write(" " * indent + "cookies={\n")
                            for name, value in cookie_dict.items():
                                escaped_value = value.replace("'", "\\'")
                                f.write(" " * (indent + 4) + f"'{name}': '{escaped_value}',\n")
                            f.write(" " * indent + "}\n")
                            
                            i += 1
                            brace_count = 1
                            while i < len(lines) and brace_count > 0:
                                line = lines[i]
                                brace_count += line.count('{') - line.count('}')
                                i += 1
                            i -= 1
                            break
                        else:
                            f.write(line)
                            i += 1
                else:
                    f.write(line)
                
                i += 1
        print(f"🍪 PDM authentication cookies successfully updated!")
    except Exception as e:
        sys.exit(f"Error updating PDM cookies: {e}")
    return
...

def parse_game_from_data(data):
    return {
        "startTime": format_utc_to_est(data["startTimeUTC"]),
        "broadcasts": ", ".join(f"{b.get('network', '')}" for b in data.get("tvBroadcasts", []) if b.get("network")),
        "venue": data.get("venue", {}).get("default", ""),
        "homeTeam": parse_team_from_data("homeTeam", data),
        "awayTeam": parse_team_from_data("awayTeam", data)
    }
...

def parse_team_from_data(team, data):
    return {
        "id": data[f"{team}"].get("id", 0),
        "abbrev": data[f"{team}"].get("abbrev", ""),
        "name": data[f"{team}"].get("name", {}).get("default", ""),
        "commonName": data[f"{team}"].get("commonName", {}).get("default", ""),
        "record": data[f"{team}"].get("record", "0-0"),
        "lineupUrl": f"{os.getenv("LINEUP_URL")}/{parse_team_from_abbrev(data[f'{team}'].get('abbrev', ''), True)}/line-combinations",
    }
...