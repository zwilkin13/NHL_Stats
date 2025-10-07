# Main entry point for NHL data processing

import sys
from termcolor import colored
import network as net
import json
from datetime import datetime
from argparse import ArgumentParser
from types import SimpleNamespace
import printer
from common import format_date, parse_date, parse_team_from_abbrev
from spinner import start_spinner, stop_spinner
from exceptions import InsufficientArgsException, InvalidArgsException

SCOREBOARD_URL = "https://api-web.nhle.com/v1/scoreboard"
NEWS_URL = "https://www.nhl.com/news"
LINEUP_URL = "https://www.dailyfaceoff.com/teams"

def load_team_names(home="CHI", away="FLA"):
    print(f"🏒 Loading NHL team names for {home} vs {away}...")

...

def load_todays_games(args=None):
    parser = ArgumentParser(description="Load Todays Games Processor")
    parser.add_argument("command", nargs="?", help="Command to execute (e.g., games, lineups)", type=str, default="games")
    parser.add_argument("date", nargs="?", help="Date for the game (e.g., YYYY-MM-DD or MM/DD/YYYY)", type=parse_date, default=datetime.today())
    parsed_args = parser.parse_args()
    date = parsed_args.date

    if date is None:
        date = datetime.today()

    printer.print_header_table(f"NHL Games", colored(date.strftime('%A, %B %#d %Y'), 'light_blue', attrs=['bold']))

    response = net.network_GET(SCOREBOARD_URL, "now")
    if response.status_code == 200:
        try:
            (stop, thread) = start_spinner("⏳ Parsing... ")
            obj = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))
            games_today = next(
                (games for games in getattr(obj, "gamesByDate", []) if getattr(games, "date", "") == date.strftime("%Y-%m-%d")),
                None
            )
            if games_today is None:
                sys.exit(f"❌ No games found for {date.strftime('%A %m/%d/%Y')}.")
            
            stop_spinner(stop, thread)
            printer.print_games_data(games_today)

        except Exception as e:
            raise e
        finally:
            stop_spinner(stop, thread)
    else:
        print("Error loading today's games.")
...

def load_lineups_for_game(args):
    parser = ArgumentParser(description="Load Lineups for Game Processor")
    parser.add_argument("team", help="Team abbreviation (e.g., TBL)", type=lambda s: s.upper())
    parsed_args = parser.parse_args(args)
    # date = parsed_args.date
    
    # if date is None:
    #     date = datetime.today()

    # date_str = date.strftime("%B-%#d-%Y").lower()
    print(f"🏒 Loading NHL lineups for {parsed_args.team}...")

    team = parse_team_from_abbrev(parsed_args.team, True)

    if not team:
        raise ValueError("Invalid team abbreviation provided.")

    # response = net.network_GET(NEWS_URL, f"{away_team}-{home_team}-game-preview-{date_str}")
    response = net.network_GET(LINEUP_URL, f"{team}/line-combinations")
    # data = response.json()
    if response.status_code == 200:
        data = response.json()
        print("Lineups page loaded successfully.")
    else:
        print("Error loading team lineups.")
...

def is_debugging():
    if hasattr(sys, "orig_argv"):
        if any("debugpy" in arg for arg in sys.orig_argv):
            return True
    return False
...

def perform_debug_action(args):
    # load_todays_games()
    # print_team_lineups(["TBL", "FLA", "CHI", "XXX"])
    pass
...

if __name__== "__main__":
    if is_debugging():
        printer.print_debugger_warning(sys.argv[1:])
        perform_debug_action(sys.argv[1:])
    else:
        try:
            if sys.argv and len(sys.argv) < 2:
                raise InsufficientArgsException(message="No command provided.")
            
            match sys.argv[1]:
                case "games":
                    load_todays_games(sys.argv[2:])

                case "lineups":
                    # load_lineups_for_game(sys.argv[2:])
                    printer.print_team_lineups(sys.argv[2:])

                case _:
                    raise InvalidArgsException(sys.argv[1:], "Unknown command. Please try again.")
        except (Exception, InsufficientArgsException) as e:
            print(f"An error occurred: {e}")
...