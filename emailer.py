import os, sys
from dotenv import load_dotenv
from spinner import start_spinner, stop_spinner
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
        e, t = start_spinner(f"✉️ Sending email to {to}... ")
        with smtplib.SMTP(_server, _port) as server:
            server.starttls()
            server.login(_from, _password)
            server.send_message(msg)
        stop_spinner(e, t)
        print(f"✅ Email sent successfully to {to}.")
    except Exception as e:
        sys.exit(f"Failed to send email: {e}")
    pass
...

class formatter:
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
...
