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
from config import NHLE_URL, LINEUP_URL, TEAMS_LIST
from common import (
    parse_date,
    parse_team_from_abbrev,
    position_code_to_name,
    validate_team_abbrev
)

# Gets lineups for a game
@command(action="get", method="lineups",
         print_title="NHL Lineups",
         help_text="Load NHL lineups for a specific team and date.",
         addtl_help_text="Fetches and displays the lineup combinations for the specified team on the given date.",
         args_help="<team> <date?>",
         options_help=[
             "<team>    Abbreviation for team (i.e. TBL).", 
             "<date?>   Date in YYYY-MM-DD or MM/DD/YYYY format. Defaults to today if not provided."])
def load_lineups_for_game(args):
    raise NotImplementedError("This function is not yet implemented.")
    # parser = ArgumentParser(description="Load Lineups for Game Processor")
    # parser.add_argument("team", help="Abbreviation for team (i.e. TBL)", type=str,)
    # parser.add_argument("date", nargs="?", help="Date for the game (e.g., YYYY-MM-DD or MM/DD/YYYY)", type=parse_date, default=datetime.today())
    # parsed_args = parser.parse_args(args)

    # date = parsed_args.date
    # if date is None:
    #     date = datetime.today()

    # team = parse_team_from_abbrev(parsed_args.team, True)
    # if not team:
    #     sys.exit("Invalid team abbreviation provided.")

    # # response = net.network_GET(NEWS_URL, f"{away_team}-{home_team}-game-preview-{date_str}")
    # response = network_GET(LINEUP_URL, f"{team}/line-combinations")
    # if response.status_code == 200:
    #     # data = response.json()
    #     print("Lineups page loaded successfully.")
    # else:
    #     sys.exit("Error loading team lineups.")
...

# Gets games for a day
@command(action="get", method="games",
         print_title="NHL Games",
         help_text="Load NHL games for a specific day.",
         addtl_help_text="Fetches and displays NHL games scheduled for the specified date.",
         args_help="<date?>",
         options_help=["<date?>   Date in YYYY-MM-DD or MM/DD/YYYY format. Defaults to today if not provided."])
def load_games_for_day(args):
    parser = ArgumentParser(description="Load Games for a Day Processor")
    parser.add_argument("date", nargs="?", help="Date for the game (e.g., YYYY-MM-DD or MM/DD/YYYY)", type=parse_date, default=datetime.today())
    parsed_args = parser.parse_args(args)

    date = parsed_args.date
    if date is None:
        date = datetime.today()

    response = network_GET(f"{NHLE_URL}", "scoreboard/now")
    if response.status_code == 200:
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
                lambda: printer.print_games_data(games_today),
                lambda: printer.print_header_table(
                    "NHL Games",
                    colored(date.strftime('%A, %B %#d %Y'), 'light_blue', attrs=['bold'])
                )
            )
        except (Exception, NetworkError) as e:
            raise e
    else:
        sys.exit("Error loading today's games.")
...

@command(action="list", method="roster",
         print_title="NHL Team Roster",
         help_text="Load NHL team roster.",
         addtl_help_text="Fetches and displays the roster for the specified NHL team.",
         args_help="<team>",
         options_help=["<team>   Abbreviation for the NHL team (i.e. TBL)"])
def list_roster_for_team(args):
    parser = ArgumentParser(description="List Roster for Team Processor")
    parser.add_argument("team", help="Abbreviation for team(s) (i.e. TBL)", type=str)
    parser.add_argument("--forward", "-f", help="Return forwards only", action="store_true", default=False)
    parser.add_argument("--defense", "-d", help="Return defensemen only", action="store_true", default=False)
    parser.add_argument("--goalie", "-g", help="Return goalies only", action="store_true", default=False)
    parsed_args = parser.parse_args(args)

    if not validate_team_abbrev(parsed_args.team):
        sys.exit(f"Invalid team abbreviation provided. [{parsed_args.team}]")

    response = network_GET(f"{NHLE_URL}", f"roster/{parsed_args.team}/20252026")
    if response.status_code == 200:
        data = response.json()

        forwards = []
        defensemen = []
        goalies = []
        roster = []
        
        for forward in data.get("forwards", []):
            forwards.append(extract_player_info(forward, "Forward"))

        for defense in data.get("defensemen", []):
            defensemen.append(extract_player_info(defense, "Defenseman"))

        for goalie in data.get("goalies", []):
            goalies.append(extract_player_info(goalie, "Goalie"))

        if parsed_args.forward or parsed_args.defense or parsed_args.goalie:
            if parsed_args.forward: roster.extend(forwards)
            if parsed_args.defense: roster.extend(defensemen)
            if parsed_args.goalie: roster.extend(goalies)
        else: 
            roster = forwards + defensemen + goalies

        return (
            roster,
            lambda: printer.print_roster_data(parsed_args.team, roster),
            None
        )
    else:
        sys.exit("Error loading team roster.")
...

def extract_player_info(player, line):
    first_name = player.get("firstName", {}).get("default", "")
    last_name = player.get("lastName", {}).get("default", "")
    return {
        "id": player.get("id", ""),
        "name": f"{first_name} {last_name}",
        "number": player.get("sweaterNumber", ""),
        "line": line,
        "position": position_code_to_name(player.get("positionCode", ""))
    }
...

@command(action="list", method="teams",
         print_title="NHL Teams",
         help_text="Full list of all NHL teams and their abbreviations.",
         addtl_help_text="Fetches and displays the list of NHL teams.")
def list_available_teams(args=None):
    return (
        TEAMS_LIST,
        lambda: printer.print_teams_list(TEAMS_LIST),
        None
    )
...


if __name__ == "__main__":
    import sys, registry
    args = []
    try:
        cmd = registry.get_command("list", "teams")
        (r, p, h) = cmd(args)
        if h: h()
        if p: p()
        else: print(r)
    except Exception as e:
        print(f"Error retrieving command: {e}")
...