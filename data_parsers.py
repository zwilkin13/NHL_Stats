
import os, datetime
from data import TEAMS_LIST
from common import format_utc_to_est

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

def parse_game_from_data(data):
    return {
        "startTime": format_utc_to_est(data["startTimeUTC"]),
        "broadcasts": ", ".join(f"{b.get('network', '')}" for b in data.get("tvBroadcasts", []) if b.get("network")),
        "venue": data.get("venue", {}).get("default", ""),
        "homeTeam": parse_team_from_data("homeTeam", data),
        "awayTeam": parse_team_from_data("awayTeam", data)
    }
...

def parse_team_from_abbrev(abbrev, hyphen=False):
    team_name = TEAMS_LIST.get(abbrev.upper(), None)["name"]
    if hyphen and team_name:
        return team_name.lower().replace(" ", "-")
    return team_name
...

def parse_team_from_abbrev_full(abbrev):
    team = TEAMS_LIST.get(abbrev.upper(), None)
    if team:
        return {
            "name": team["name"],
            "primaryColor": team["colors"]["primary"],
            "secondaryColor": team["colors"]["secondary"],
            "fontColor": team["colors"]["font"],
        }
    return None

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
