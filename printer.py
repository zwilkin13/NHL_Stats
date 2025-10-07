import prettytable as pt
from datetime import datetime
from termcolor import colored
from common import (
    format_utc_to_est, 
    validate_team_abbrev,
    parse_team_from_abbrev, 
    hyphen_words
)

LINEUP_URL = "https://www.dailyfaceoff.com/teams"

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

def print_games_data(games):
    for game in getattr(games, "games", []):
        print_game_data(game)
    return True
...

def print_game_data(game):
    table = pt.PrettyTable(border=True, header=True, align="l", min_width=12)
    table.set_style(pt.SINGLE_BORDER)
    table.field_names = ["🏒 Team", "📝 Record", "🌐 Lineup (dailyfaceoff.com)"]
    
    start_time = format_utc_to_est(game.startTimeUTC, '%I:%M %p')
    
    home_abbrev = game.homeTeam.abbrev
    home_team = game.homeTeam.commonName.default
    home_record = game.homeTeam.record if hasattr(game.homeTeam, 'record') else "0-0"
    home_lineup_url = f"{LINEUP_URL}/{parse_team_from_abbrev(home_abbrev, True)}/line-combinations"

    away_team = game.awayTeam.commonName.default
    away_abbrev = game.awayTeam.abbrev
    away_record = game.awayTeam.record if hasattr(game.awayTeam, 'record') else "0-0"
    away_lineup_url = f"{LINEUP_URL}/{parse_team_from_abbrev(away_abbrev, True)}/line-combinations"

    table.title = f"{away_abbrev} @ {home_abbrev} | 🕒 {start_time}"
    table.add_row([home_team, home_record, home_lineup_url])
    table.add_row([away_team, away_record, away_lineup_url])

    print(table)
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
        lineup_url = f"{LINEUP_URL}/{name_hyphen}/line-combinations"
        table.add_row([name, lineup_url])

    print(table)
...