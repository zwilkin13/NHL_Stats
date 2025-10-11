"""
Data file for NHL Stats application.
Contains constants like team info and position mappings.
"""

TEAMS_LIST = {
    "ANA": {"name": "Anaheim Ducks", "colors": {"primary": "#F47A38", "secondary": "#111111", "font": "#FFFFFF"}},
    "ARI": {"name": "Arizona Coyotes", "colors": {"primary": "#8C2633", "secondary": "#E2D6B5", "font": "#FFFFFF"}},
    "BOS": {"name": "Boston Bruins", "colors": {"primary": "#FFB81C", "secondary": "#FCB514", "font": "#FFFFFF"}},
    "BUF": {"name": "Buffalo Sabres", "colors": {"primary": "#003087", "secondary": "#FCB514", "font": "#FFFFFF"}},
    "CGY": {"name": "Calgary Flames", "colors": {"primary": "#b72b35", "secondary": "#F1BE48", "font": "#FFFFFF"}},
    "CAR": {"name": "Carolina Hurricanes", "colors": {"primary": "#CE1126", "secondary": "#111111", "font": "#FFFFFF"}},
    "CHI": {"name": "Chicago Blackhawks", "colors": {"primary": "#CF0A2C", "secondary": "#111111", "font": "#FFFFFF"}},
    "COL": {"name": "Colorado Avalanche", "colors": {"primary": "#6F263D", "secondary": "#236192", "font": "#FFFFFF"}},
    "CBJ": {"name": "Columbus Blue Jackets", "colors": {"primary": "#002654", "secondary": "#CE1126", "font": "#FFFFFF"}},
    "DAL": {"name": "Dallas Stars", "colors": {"primary": "#006847", "secondary": "#8F8F8C", "font": "#FFFFFF"}},
    "DET": {"name": "Detroit Red Wings", "colors": {"primary": "#CE1126", "secondary": "#CE1126", "font": "#FFFFFF"}},
    "EDM": {"name": "Edmonton Oilers", "colors": {"primary": "#041E42", "secondary": "#FF4C00", "font": "#FFFFFF"}},
    "FLA": {"name": "Florida Panthers", "colors": {"primary": "#c8102E", "secondary": "#041e42", "font": "#FFFFFF"}},
    "LAK": {"name": "Los Angeles Kings", "colors": {"primary": "#111111", "secondary": "#a2aaad", "font": "#FFFFFF"}},
    "MIN": {"name": "Minnesota Wild", "colors": {"primary": "#154734", "secondary": "#C51230", "font": "#eee3c7"}},
    "MTL": {"name": "Montreal Canadiens", "colors": {"primary": "#c51230", "secondary": "#192168", "font": "#FFFFFF"}},
    "NSH": {"name": "Nashville Predators", "colors": {"primary": "#FFB81C", "secondary": "#041e42", "font": "#FFFFFF"}},
    "NJD": {"name": "New Jersey Devils", "colors": {"primary": "#CE1126", "secondary": "#111111", "font": "#FFFFFF"}},
    "NYI": {"name": "New York Islanders", "colors": {"primary": "#00539B", "secondary": "#F47920", "font": "#FFFFFF"}},
    "NYR": {"name": "New York Rangers", "colors": {"primary": "#0038A8", "secondary": "#CE1125", "font": "#FFFFFF"}},
    "OTT": {"name": "Ottawa Senators", "colors": {"primary": "#DA1A32", "secondary": "#111111", "font": "#FFFFFF"}},
    "PHI": {"name": "Philadelphia Flyers", "colors": {"primary": "#F74902", "secondary": "#000000", "font": "#FFFFFF"}},
    "PIT": {"name": "Pittsburgh Penguins", "colors": {"primary": "#000000", "secondary": "#FCB514", "font": "#FFFFFF"}},
    "SJS": {"name": "San Jose Sharks", "colors": {"primary": "#006D75", "secondary": "#EA7200", "font": "white"}},
    "SEA": {"name": "Seattle Kraken", "colors": {"primary": "#001628", "secondary": "#E9072B", "font": "#99D9D9"}},
    "STL": {"name": "St. Louis Blues", "colors": {"primary": "#002f87", "secondary": "#FCB514", "font": "#FFFFFF"}},
    "TBL": {"name": "Tampa Bay Lightning", "colors": {"primary": "#002868", "secondary": "#000000", "font": "#FFFFFF"}},
    "TOR": {"name": "Toronto Maple Leafs", "colors": {"primary": "#003E7E", "secondary": "#003E7E", "font": "#FFFFFF"}},
    "VAN": {"name": "Vancouver Canucks", "colors": {"primary": "#001f5c", "secondary": "#021B2C", "font": "#FFFFFF"}},
    "VGK": {"name": "Vegas Golden Knights", "colors": {"primary": "#b4975a", "secondary": "#333F42", "font": "#FFFFFF"}},
    "WPG": {"name": "Winnipeg Jets", "colors": {"primary": "#004B87", "secondary": "#A4C8E1", "font": "#FFFFFF"}},
    "WSH": {"name": "Washington Capitals", "colors": {"primary": "#041E41", "secondary": "#CF0A2C", "font": "#FFFFFF"}}
}

POSITIONS_LIST = {
    "C": "Center",
    "L": "Left Wing",
    "LW": "Left Wing",
    "R": "Right Wing",
    "RW": "Right Wing",
    "D": "Defenseman",
    "G": "Goaltender"
}
