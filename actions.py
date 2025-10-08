"""
Scripts for command line actions.
"""

import json
import sys
import printer
from argparse import ArgumentParser
from datetime import datetime
from types import SimpleNamespace
from termcolor import colored
from registry import command
from network import network_GET, NetworkError
from config import SCOREBOARD_URL, LINEUP_URL
from common import parse_date
from exceptions import InsufficientArgsException, InvalidArgsException

# Gets games for a day
@command(action="get", method="games",
         print_title="NHL Games",
         help_text="Load NHL games for a specific day.",
         addtl_help_text="Fetches and displays NHL games scheduled for the specified date.",
         args_help="<date> (optional) - Date in YYYY-MM-DD or MM/DD/YYYY format. Defaults to today if not provided."
)
def load_games_for_day(args):
    parser = ArgumentParser(description="Load Games for a Day Processor")
    parser.add_argument("date", nargs="?", help="Date for the game (e.g., YYYY-MM-DD or MM/DD/YYYY)", type=parse_date, default=datetime.today())
    parsed_args = parser.parse_args(args)
    date = parsed_args.date

    if date is None:
        date = datetime.today()

    response = network_GET(SCOREBOARD_URL, "now")
    if response.status_code == 200:
        # printer.print_header_table()
        try:
            obj = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))
            games_today = next(
                (games for games in getattr(obj, "gamesByDate", []) if getattr(games, "date", "") == date.strftime("%Y-%m-%d")),
                None
            )
            if games_today is None:
                sys.exit(f"❌ No games found for {date.strftime('%A %m/%d/%Y')}.")
            
            return (
                games_today,
                printer.print_games_data,
                lambda: printer.print_header_table(
                    "NHL Games",
                    colored(date.strftime('%A, %B %#d %Y'), 'light_blue', attrs=['bold'])
                )
                # colored(date.strftime('%A, %B %#d %Y'), 'light_blue', attrs=['bold'])
            )
        except (Exception, NetworkError) as e:
            raise e
    else:
        sys.exit("Error loading today's games.")
...