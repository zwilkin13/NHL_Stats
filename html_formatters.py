"""
HTML formatters for email content.
"""
import os
from data_parsers import parse_game_from_data

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "html_templates")

# Formats the team roster into an HTML table for email
def format_team_roster(players_data, team):
    from string import Template
    
    # Generate player rows HTML
    player_rows_html = ""
    for i, player in enumerate(players_data, start=1):
        player_rows_html += f"""
            <tr>
                <td style="text-align: center;{'padding-top: 10px;' if i == 1 else ''}">{player.get('number', '')}</td>
                <td style="text-align: left;{'padding-top: 10px;' if i == 1 else ''}">{player.get('name', '')}</td>
                <td style="text-align: left;{'padding-top: 10px;' if i == 1 else ''}">{player.get('position', '')}</td>
            </tr>"""
    
    table_header = f"""
        <h2 style="margin-top:0px;padding-top:15px;padding-bottom:10px;text-align:center;
            color:{team["fontColor"]};
            background-color:{team["primaryColor"]};
            border-bottom: 2px solid {team["secondaryColor"]};">
                {team["name"]}
        </h2>"""

    # Read and populate template
    with open(f"{TEMPLATES_DIR}/team_roster.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    template = Template(html_content)
    html_content = template.safe_substitute(
        player_rows=player_rows_html,
        table_header=table_header,
        team_name=team["name"]
    )
    
    return html_content
...

# Formats the games schedule into an HTML table for email
def format_gameschedule(games_data, header):
    from string import Template

    # Game separator
    separator = """<hr style="border: 0; height: 1px; background: #b9b9b9; margin: 20px 30px;">"""
    
    # Row Header
    row_header = """
        <tr>
            <th style="text-align: left;padding: 0px 0px 2px 0px;border-bottom: 1px solid black;">🏒 Team</th>
            <th style="text-align: center;padding: 0px 5px 2px 0px;border-bottom: 1px solid black;">📝 Record</th>
            <th style="text-align: center;padding: 0px 0px 2px 0px;border-bottom: 1px solid black;">🌐 Lineup (dailyfaceoff.com)</th>
        </tr>
    """

    # Generate game tables HTML
    game_tables_html = ""
    for i, game in enumerate(games_data, start=1):
        game = parse_game_from_data(game)
        start_time = game["startTime"]
        away = game["awayTeam"]
        home = game["homeTeam"]

        table_header = f"""
            <tr>
                <td colspan="3">
                    <h3 style="text-align: center;margin: 0px;">({away['abbrev']}) {away["name"]} @ ({home['abbrev']}) {home["name"]}</h3>
                    <h4 style="text-align: center;margin: 0px 0px 15px 0px;font-weight: 550;">🕒 {start_time} | 📺 {game['broadcasts']}</h4>
                </td>
            </tr>
        """
        away_row = f"""
            <tr>
                <td style="text-align: left;">{away["name"]}</td>
                <td style="text-align: center;">{away["record"]}</td>
                <td style="text-align: center;"><a style="font-weight:bold;" href="{away["lineupUrl"]}">Click Here</a></td>
            </tr>
        """
        home_row = f"""
            <tr>
                <td style="text-align: left;">{home["name"]}</td>
                <td style="text-align: center;">{home["record"]}</td>
                <td style="text-align: center;"><a style="font-weight:bold;" href="{home["lineupUrl"]}">Click Here</a></td>
            </tr>
        """
        game_tables_html += f"""
            <table style="border-spacing:0;width:100%;">
                <tbody>
                    <colgroup>
                        <col style="width:40%">
                    </colgroup>
                    {table_header}
                    {row_header}
                    {away_row}
                    {home_row}
                </tbody>
            </table>
            {separator if i != len(games_data) else ""}
        """
    
    # Read and populate template
    with open(f"{TEMPLATES_DIR}/days_games.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    template = Template(html_content)
    html_content = template.safe_substitute(
        main_header=header,
        game_tables=game_tables_html
    )
    
    return html_content
...