import os, sys
from dotenv import load_dotenv
load_dotenv()

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "html_templates")

def send(to, subject, body):
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

def format_team_roster(players_data, team_name="Team Roster"):
    from string import Template
    
    # Generate player rows HTML
    player_rows_html = ""
    for player in players_data:
        player_rows_html += f"""
            <tr>
                <td style="text-align: center;">{player.get('number', '')}</td>
                <td>{player.get('name', '')}</td>
                <td>{player.get('line', '')}</td>
                <td>{player.get('position', '')}</td>
            </tr>"""
    
    # Read and populate template
    with open(f"{TEMPLATES_DIR}/team_roster.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    template = Template(html_content)
    html_content = template.safe_substitute(
        player_rows=player_rows_html,
        team_name=team_name
    )
    
    return html_content
...