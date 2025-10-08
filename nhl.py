# Main entry point for NHL data processing

import sys
from termcolor import colored
import network as net
import json
from datetime import datetime
from argparse import ArgumentParser
from types import SimpleNamespace
import printer
from common import parse_date, parse_team_from_abbrev
from spinner import start_spinner, stop_spinner
from exceptions import InsufficientArgsException, InvalidArgsException
from registry import (
    get_command,
    get_command_print_title,
    list_available_commands,
    register_module_commands,
    print_help
)

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
    parser.add_argument("date", help="Date for the game (e.g., YYYY-MM-DD)", default=datetime.today(), type=datetime)
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

def perform_debug_action(args):
    # load_todays_games()
    # print_team_lineups(["TBL", "FLA", "CHI", "XXX"])
    pass
...

# Import modules that contain commands
import actions

# Ensure all commands are registered
register_module_commands(actions)

if __name__== "__main__":
    if not hasattr(sys, "orig_argv") and any("debugpy" in arg for arg in sys.orig_argv):
        # printer.print_debugger_warning(sys.argv[0:])
        # perform_debug_action(sys.argv[1:])
        cmdf = get_command("get", "games")
        results = cmdf([])
        print("✅ Success!")
        pass
    else:
        try:
            
            if '-h' in sys.argv or '--help' in sys.argv:
                help_args = [arg for arg in sys.argv[1:] if arg not in ['-h', '--help']]
                print_help(help_args)
                sys.exit(0)
            
            if sys.argv and len(sys.argv) < 3:
                print("❓ Please specify which action you wish to perform")
                print_help([])
                sys.exit(0)

            action = sys.argv[1].lower()
            method = sys.argv[2].lower()
            raw_args = sys.argv[3:]

            # Get the command function dynamically
            command_function = get_command(action, method)

            if not command_function:
                print(f"❌ Unknown command '{action} {method}'")
                print("💡 Available commands:")
                available_commands = list_available_commands()
                for cmd, sub_cmds in available_commands.items():
                    print(f"   {cmd}: [{', '.join(sub_cmds)}]")
                sys.exit(0)
        
            (results, _printer, _header) = command_function(raw_args)
            print("✅ Success!")
            
            if _header: _header()
            if _printer: 
                _printer(results)
            else:
                print(results)
        except Exception as e:
            print(f"❌ Error executing command '{action} {method}': {e}")
        except SystemExit as e:
            if e.code == 0:
                pass
            elif e.code == 1:
                print(f"❌ Unknown command '{action} {method}' was entered. Please try again.")
            else:
                print(f"❌ {action.capitalize()} {method} exited!\n   {e}")
...