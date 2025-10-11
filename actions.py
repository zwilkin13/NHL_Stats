"""
Scripts for command line actions.
"""

import os
import sys
import printer
from argparse import ArgumentParser
from datetime import datetime
from termcolor import colored
from registry import command
from network import network_GET, NetworkError
from config import TEAMS_LIST
from common import (
    parse_date,
    parse_team_from_abbrev,
    position_code_to_name,
    validate_team_abbrev
)
from dotenv import load_dotenv
load_dotenv()

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
def load_games_for_day(args=None):
    parser = ArgumentParser(description="Load Games for a Day Processor")
    parser.add_argument("date", nargs="?", help="Date for the game (e.g., YYYY-MM-DD or MM/DD/YYYY)", type=parse_date, default=datetime.today())
    parsed_args = parser.parse_args(args)
    date = parsed_args.date

    if date is None:
        date = datetime.today()

    base_url = os.getenv("NHLE_URL")
    response = network_GET(f"{base_url}", "scoreboard/" + (f"{date.strftime('%Y-%m-%d')}" if date else "now"))
    if response.status_code == 200:
        try:
            data = response.json()
            games = (next(
                (games for games in data.get("gamesByDate", []) if games.get("date") == data.get("focusedDate")),
                None
            ))

            if not games or len(games) == 0:
                sys.exit(f"🏒 There are no NHL games playing on {date.strftime('%A %m/%d/%Y')}.")

            return (
                games["games"],
                lambda: printer.print_games_data(games["games"]),
                lambda: printer.print_header_table(
                    f"NHL Games ({len(games["games"])})",
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

    base_url = os.getenv("NHLE_URL")
    response = network_GET(f"{base_url}", f"roster/{parsed_args.team}/20252026")
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

def send_email(to, subject, body):
    import smtplib
    from email.message import EmailMessage
    _from = os.getenv("EMAIL_FROM")
    _password = os.getenv("EMAIL_PASSWORD")
    _server = os.getenv("EMAIL_SMTP_SERVER")
    _port = os.getenv("EMAIL_SMTP_PORT")

    msg = EmailMessage()
    msg["From"] = "NHL Stats"
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body, subtype='html')

    try:
        with smtplib.SMTP(_server, _port) as server:
            server.starttls()
            server.login(_from, _password)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        sys.exit(f"Failed to send email: {e}")
    pass
...

if __name__ == "__main__":
    import nhl
    # nhl.perform_debug_action(["get", "games"])

    d, p, h = load_games_for_day(["10/11/2025"])
    
    send_email(
        "z.wilkin13@gmail.com",
        "NHL Stats - Player Update!",
        f"{d}"
    )
...