import os
import prettytable as pt
from termcolor import colored
from common import (
    validate_team_abbrev,
    parse_team_from_abbrev, 
    hyphen_words,
    parse_game_from_data
)
from dotenv import load_dotenv
load_dotenv()


def print_debugger_warning(args):
    orange = (255, 167, 0)
    print(colored("\n````````````````````````````````````````````````````````````````", orange))
    print(colored(f"⚠️  WARNING: You are running in debug mode!  ⚠️", orange, attrs=["bold"]))
    print(colored(f"   Args: {args[1:]}", orange, attrs=["bold"]))
    print(colored(f"`````````````````````````````````````````````````````````````````", orange))
    return
...

def print_header_table(title="NHL Stats", subtitle=""):
    table = pt.PrettyTable(border=True, header=True, align="c")
    table.set_style(pt.SINGLE_BORDER)
    table.field_names = [title]
    table.add_row([subtitle])
    print(table)
    return
...

def print_games_data(data):
    for game_data in data:
        print_game_data(parse_game_from_data(game_data))
    return True
...

def print_game_data(game):
    table = pt.PrettyTable(border=True, header=True, align="l", min_width=12, min_table_width=120)
    table.set_style(pt.SINGLE_BORDER)
    
    start_time = game["startTime"]

    home = game["homeTeam"]
    away = game["awayTeam"]

    home_abbrev = home["abbrev"]
    home_name = home["name"]
    home_common_name = home["commonName"]
    home_record = home["record"]
    home_lineup_url = home["lineupUrl"]

    away_abbrev = away["abbrev"]
    away_name = away["name"]
    away_common_name = away["commonName"]
    away_record = away["record"]
    away_lineup_url = away["lineupUrl"]

    table.title = f"({away_abbrev}) {away_name} @ ({home_abbrev}) {home_name} | 🕒 {start_time} | 📺 {game['broadcasts']}"
    table.field_names = ["🏒 Team", "📝 Record", "🌐 Lineup (dailyfaceoff.com)"]
    table.add_row([home_name, home_record, home_lineup_url])
    table.add_row([away_name, away_record, away_lineup_url])

    print(table)
    return
...


def print_roster_data(team_abbrv, roster):
    table = pt.PrettyTable(border=True, header=True, align="l")
    table.set_style(pt.SINGLE_BORDER)
    team_name = parse_team_from_abbrev(team_abbrv)
    table.title = f"🏒 {team_name} Roster"
    table.field_names = ["#", "Player", "Line", "Position", "id"]

    for player in roster:
        table.add_row([
            player.get("number", ""), 
            player.get("name", ""),
            player.get("line", ""),
            player.get("position", ""),
            player.get("id", "")])

    print(table)
    return
...

def print_team_lineups(teams=[]):
    table = pt.PrettyTable(border=True, header=True, align="l")
    table.set_style(pt.SINGLE_BORDER)
    table.title = "NHL Game Lineups"
    table.field_names = ["🏒 Team", "🌐 Lineup (dailyfaceoff.com)"]

    for t in teams:
        if validate_team_abbrev(t) is False:
            table.add_row([colored(f"{t} ❌", "red", attrs=["bold"]), colored("Invalid Team", "red", attrs=["bold"])])
            continue
        name = parse_team_from_abbrev(t)
        name_hyphen = hyphen_words(name)
        lineup_url = f"{os.getenv("LINEUP_URL")}/{name_hyphen}/line-combinations"
        table.add_row([name, lineup_url])

    print(table)
    return
...

def print_teams_list(teams):
    teams = sorted(teams.items())
    table = pt.PrettyTable(border=True, header=True, align="l")
    table.set_style(pt.SINGLE_BORDER)
    table.title = "🏒 NHL Teams"
    table.field_names = ["Abbrev.", "Team Name"]

    for abbrev, name in teams:
        table.add_row([abbrev, name])

    print(table)
    return
...


if __name__ == "__main__":
    import nhl
    nhl.perform_debug_action(["get", "games", "2025-10-11"])
...

