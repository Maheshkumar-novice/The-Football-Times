from flask import Flask, render_template_string
import requests
from datetime import datetime, timedelta, timezone
import os
import json
import time

app = Flask(__name__)

# Get API token from environment variable
API_TOKEN = os.environ.get('FOOTBALL_API_TOKEN', '')
API_DELAY = int(os.environ.get('FOOTBALL_API_DELAY', '2'))  # delay in seconds between API calls
CACHE_FILE = 'matches_cache.json'
CACHE_DURATION = 300  # 5 minutes in seconds

def is_cache_valid():
    """Check if cache file exists and is less than 5 minutes old"""
    if not os.path.exists(CACHE_FILE):
        print(f"[DEBUG] Cache file {CACHE_FILE} does not exist")
        return False

    cache_time = os.path.getmtime(CACHE_FILE)
    current_time = datetime.now().timestamp()
    age = current_time - cache_time
    is_valid = age < CACHE_DURATION

    print(f"[DEBUG] Cache age: {age:.1f} seconds, valid: {is_valid} (limit: {CACHE_DURATION}s)")
    return is_valid

def load_from_cache():
    """Load data from cache file"""
    try:
        with open(CACHE_FILE, 'r') as f:
            data = json.load(f)
            print(f"[DEBUG] Successfully loaded data from cache")
            return data
    except Exception as e:
        print(f"[DEBUG] Failed to load from cache: {e}")
        return None

def save_to_cache(data):
    """Save data to cache file"""
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f, default=str)
            print(f"[DEBUG] Successfully saved data to cache")
    except Exception as e:
        print(f"[DEBUG] Failed to save to cache: {e}")


def get_premier_league_standings():
    """Get Premier League standings"""
    try:
        time.sleep(API_DELAY)  # configurable delay for rate limiting
        r = requests.get("https://api.football-data.org/v4/competitions/PL/standings",
                         headers={"X-Auth-Token": API_TOKEN})
        if r.status_code == 200:
            data = r.json()
            standings = data.get("standings", [])
            if standings:
                return standings[0].get("table", [])
    except:
        pass
    return []

def get_la_liga_standings():
    """Get La Liga standings"""
    try:
        time.sleep(API_DELAY)  # configurable delay for rate limiting
        r = requests.get("https://api.football-data.org/v4/competitions/PD/standings",
                         headers={"X-Auth-Token": API_TOKEN})
        if r.status_code == 200:
            data = r.json()
            standings = data.get("standings", [])
            if standings:
                return standings[0].get("table", [])
    except:
        pass
    return []

def get_premier_league_scorers():
    """Get Premier League top scorers"""
    try:
        time.sleep(API_DELAY)  # configurable delay for rate limiting
        r = requests.get("https://api.football-data.org/v4/competitions/PL/scorers",
                         headers={"X-Auth-Token": API_TOKEN})
        if r.status_code == 200:
            data = r.json()
            return data.get("scorers", [])
    except:
        pass
    return []

def get_la_liga_scorers():
    """Get La Liga top scorers"""
    try:
        time.sleep(API_DELAY)  # configurable delay for rate limiting
        r = requests.get("https://api.football-data.org/v4/competitions/PD/scorers",
                         headers={"X-Auth-Token": API_TOKEN})
        if r.status_code == 200:
            data = r.json()
            return data.get("scorers", [])
    except:
        pass
    return []

def get_bundesliga_standings():
    """Get Bundesliga standings"""
    try:
        time.sleep(API_DELAY)  # configurable delay for rate limiting
        r = requests.get("https://api.football-data.org/v4/competitions/BL1/standings",
                         headers={"X-Auth-Token": API_TOKEN})
        if r.status_code == 200:
            data = r.json()
            standings = data.get("standings", [])
            if standings:
                return standings[0].get("table", [])
    except:
        pass
    return []

def get_bundesliga_scorers():
    """Get Bundesliga top scorers"""
    try:
        time.sleep(API_DELAY)  # configurable delay for rate limiting
        r = requests.get("https://api.football-data.org/v4/competitions/BL1/scorers",
                         headers={"X-Auth-Token": API_TOKEN})
        if r.status_code == 200:
            data = r.json()
            return data.get("scorers", [])
    except:
        pass
    return []

def get_serie_a_standings():
    """Get Serie A standings"""
    try:
        time.sleep(API_DELAY)  # configurable delay for rate limiting
        r = requests.get("https://api.football-data.org/v4/competitions/SA/standings",
                         headers={"X-Auth-Token": API_TOKEN})
        if r.status_code == 200:
            data = r.json()
            standings = data.get("standings", [])
            if standings:
                return standings[0].get("table", [])
    except:
        pass
    return []

def get_serie_a_scorers():
    """Get Serie A top scorers"""
    try:
        time.sleep(API_DELAY)  # configurable delay for rate limiting
        r = requests.get("https://api.football-data.org/v4/competitions/SA/scorers",
                         headers={"X-Auth-Token": API_TOKEN})
        if r.status_code == 200:
            data = r.json()
            return data.get("scorers", [])
    except:
        pass
    return []

def get_ligue1_standings():
    """Get Ligue 1 standings"""
    try:
        time.sleep(API_DELAY)  # configurable delay for rate limiting
        r = requests.get("https://api.football-data.org/v4/competitions/FL1/standings",
                         headers={"X-Auth-Token": API_TOKEN})
        if r.status_code == 200:
            data = r.json()
            standings = data.get("standings", [])
            if standings:
                return standings[0].get("table", [])
    except:
        pass
    return []

def get_ligue1_scorers():
    """Get Ligue 1 top scorers"""
    try:
        time.sleep(API_DELAY)  # configurable delay for rate limiting
        r = requests.get("https://api.football-data.org/v4/competitions/FL1/scorers",
                         headers={"X-Auth-Token": API_TOKEN})
        if r.status_code == 200:
            data = r.json()
            return data.get("scorers", [])
    except:
        pass
    return []

def get_football_data():
    # Check if we have valid cached data
    print(f"[DEBUG] Checking cache validity...")
    if is_cache_valid():
        cached_data = load_from_cache()
        if cached_data:
            print(f"[DEBUG] Using cached data")
            return cached_data

    print(f"[DEBUG] Cache miss - fetching fresh data from API")
    
    # Get date range (3 days back to today) - using IST
    today_utc = datetime.now(timezone.utc)
    today_ist = today_utc + timedelta(hours=5, minutes=30)
    date_from = (today_ist - timedelta(days=3)).strftime('%Y-%m-%d')
    date_to = today_ist.strftime('%Y-%m-%d')
    current_time_ist = today_ist.strftime('%A, %B %d, %Y at %H:%M')
    date_from_display = (today_ist - timedelta(days=3)).strftime('%B %d')
    date_to_display = today_ist.strftime('%B %d, %Y')

    # Get matches from API
    time.sleep(10)  # 10 second delay for rate limiting
    r = requests.get(f"https://api.football-data.org/v4/matches?dateFrom={date_from}&dateTo={date_to}",
                     headers={"X-Auth-Token": API_TOKEN})
    
    data = r.json()
    matches = data.get("matches", [])
    
    # Get standings and scorers for Premier League and La Liga only
    pl_standings = get_premier_league_standings()
    la_liga_standings = get_la_liga_standings()

    pl_scorers = get_premier_league_scorers()
    la_liga_scorers = get_la_liga_scorers()

    # Competition name mapping for better display
    competition_display_names = {
        "Primera Division": "La Liga",
        "Premier League": "Premier League",
        "Bundesliga": "Bundesliga", 
        "Serie A": "Serie A",
        "Ligue 1": "Ligue 1",
        "UEFA Champions League": "UEFA Champions League"
    }

    # Group by competition (only include major European leagues and Champions League)
    allowed_competitions = {
        "Premier League",
        "Primera Division", 
        "Serie A",
        "Ligue 1",
        "Bundesliga",
        "UEFA Champions League"
    }
    
    leagues = {}
    for m in matches:
        comp_name = m["competition"]["name"]
        area_name = m["area"]["name"]
        
        # Only include allowed competitions
        if comp_name not in allowed_competitions:
            continue
            
        # Use display name if available, otherwise use original name
        display_name = competition_display_names.get(comp_name, comp_name)
        full_name = f"{display_name} ({area_name})"
        
        if full_name not in leagues:
            leagues[full_name] = []
        leagues[full_name].append(m)

    # Define popularity order
    popularity_order = [
        "Premier League",
        "La Liga",
        "Bundesliga", 
        "Serie A",
        "Ligue 1",
        "UEFA Champions League",
        "UEFA Europa League",
        "MLS"
    ]

    def get_sort_key(league_name):
        # Extract competition name (before the bracket)
        comp_name = league_name.split(' (')[0]
        
        # Check if it's in our popularity list
        try:
            index = popularity_order.index(comp_name)
            return (0, index)  # Popular leagues first, ordered by index
        except ValueError:
            # Not in popularity list, sort alphabetically after
            return (1, league_name)

    # Sort leagues by popularity then alphabetically
    sorted_leagues = sorted(leagues.items(), key=lambda x: get_sort_key(x[0]))

    # Process matches for display
    processed_leagues = []
    for comp_full, matches_list in sorted_leagues:
        processed_matches = []
        for m in matches_list:
            h = m["homeTeam"]["shortName"]
            a = m["awayTeam"]["shortName"]
            status = m["status"]
            
            # Convert UTC to IST (UTC+5:30)
            dt_utc = datetime.fromisoformat(m["utcDate"].replace('Z', '+00:00'))
            dt_ist = dt_utc + timedelta(hours=5, minutes=30)
            date_time = dt_ist.strftime('%d-%m %H:%M')
            
            # Status icons
            status_map = {
                "FINISHED": "✅",
                "IN_PLAY": "🔴", 
                "LIVE": "🔴",
                "SCHEDULED": "⏰",
                "POSTPONED": "⏸️",
                "CANCELLED": "❌"
            }
            status_icon = status_map.get(status, "❓")
            
            match_info = {
                "home_team": h,
                "away_team": a,
                "date_time": date_time,
                "datetime_obj": dt_ist,  # Store actual datetime for sorting
                "status": status,
                "status_icon": status_icon,
                "score_home": None,
                "score_away": None
            }
            
            if status == "FINISHED":
                s = m["score"]["fullTime"]
                match_info["score_home"] = s['home']
                match_info["score_away"] = s['away']
            
            processed_matches.append(match_info)
        
        # Sort matches by date/time in descending order (newest first)
        processed_matches.sort(key=lambda x: x["datetime_obj"], reverse=True)
        
        processed_leagues.append({
            "name": comp_full,
            "url": f"https://www.google.com/search?q={comp_full}",
            "count": len(matches_list),
            "matches": processed_matches
        })

    result = {
        "total_matches": len(matches),
        "pl_count": len([m for m in matches if m["competition"]["code"] == "PL"]),
        "date_from": date_from,
        "date_to": date_to,
        "date_from_display": date_from_display,
        "date_to_display": date_to_display,
        "current_time_ist": current_time_ist,
        "leagues": processed_leagues,
        "pl_standings": pl_standings,
        "la_liga_standings": la_liga_standings,
        "pl_scorers": pl_scorers,
        "la_liga_scorers": la_liga_scorers
    }
    
    # Save to cache
    save_to_cache(result)
    
    return result

@app.route('/news')
def index():
    data = get_football_data()
    
    html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>The Football Times</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Cinzel+Decorative:wght@700&family=Uncial+Antiqua&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Cinzel', 'Uncial Antiqua', 'Old English Text MT', 'Times New Roman', serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f1e8;
            color: #2c1810;
            line-height: 1.4;
        }
        .header {
            text-align: center;
            border-bottom: 3px double #000;
            margin-bottom: 20px;
            padding-bottom: 15px;
        }
        .masthead {
            font-family: 'Cinzel Decorative', 'Old English Text MT', 'Uncial Antiqua', serif;
            font-size: 42px;
            font-weight: bold;
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 3px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        .date-line {
            font-family: 'Cinzel', serif;
            font-size: 12px;
            text-transform: uppercase;
            margin: 5px 0 15px 0;
            letter-spacing: 2px;
            font-weight: 600;
        }
        .stats {
            font-size: 14px;
            font-style: italic;
            margin: 10px 0;
        }
        .columns {
            display: block;
            margin-top: 20px;
        }
        
        
        .standings-section {
            background: #fff;
            border: 2px solid #000;
            padding: 15px;
            margin-bottom: 25px;
            break-inside: avoid;
        }
        
        .standings-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }
        
        .standings-table th,
        .standings-table td {
            padding: 6px 8px;
            text-align: left;
            border-bottom: 1px dotted #ccc;
        }
        
        .standings-table th {
            font-family: 'Cinzel', serif;
            font-weight: bold;
            border-bottom: 2px solid #000;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .standings-table .pos {
            text-align: center;
            width: 30px;
        }
        
        .standings-table .team {
            width: 150px;
        }
        
        .standings-table .stats {
            text-align: center;
            width: 40px;
        }
        
        .scorers-section {
            background: #fff;
            border: 2px solid #000;
            padding: 15px;
            margin-bottom: 25px;
            break-inside: avoid;
        }
        
        .scorers-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .scorer-item {
            padding: 8px 0;
            border-bottom: 1px dotted #ccc;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 13px;
        }
        
        .scorer-item:last-child {
            border-bottom: none;
        }
        
        .scorer-info {
            display: flex;
            align-items: center;
        }
        
        .scorer-pos {
            width: 25px;
            font-weight: bold;
            text-align: center;
        }
        
        .scorer-name {
            font-weight: bold;
            margin-right: 10px;
        }
        
        .scorer-team {
            color: #666;
            font-size: 11px;
        }
        
        .scorer-goals {
            font-weight: bold;
            font-size: 14px;
        }
        
        .matches-section {
            background: #fff;
            border: 2px solid #000;
            padding: 15px;
            margin-bottom: 25px;
            break-inside: avoid;
        }
        
        .matches-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .matches-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }
        
        .matches-table th,
        .matches-table td {
            padding: 8px 10px;
            text-align: left;
            border-bottom: 1px dotted #ccc;
        }
        
        .matches-table th {
            font-family: 'Cinzel', serif;
            font-weight: bold;
            border-bottom: 2px solid #000;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .matches-table .match-time {
            text-align: center;
            width: 80px;
            font-family: monospace;
            color: #666;
        }
        
        .matches-table .match-teams {
            font-weight: bold;
        }
        
        .matches-table .match-score {
            text-align: center;
            width: 60px;
            font-weight: bold;
            color: #2c1810;
        }
        
        .matches-table .status-icon {
            text-align: center;
            width: 30px;
        }
        
        
        .section-header {
            font-family: 'Cinzel', 'Uncial Antiqua', 'Old English Text MT', serif;
            font-size: 20px;
            font-weight: bold;
            text-transform: uppercase;
            border-bottom: 2px solid #000;
            padding-bottom: 5px;
            margin-bottom: 15px;
            letter-spacing: 2px;
            text-shadow: 0.5px 0.5px 1px rgba(0,0,0,0.2);
        }
        .match-line {
            font-size: 13px;
            margin: 8px 0;
            padding-left: 15px;
            border-left: 2px solid #ddd;
            font-family: monospace;
        }
        .finished {
            font-weight: bold;
        }
        .time {
            font-weight: normal;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1 class="masthead">The Football Times</h1>
        <div class="date-line">{{ data.current_time_ist }} IST</div>
        <div class="stats">{{ data.total_matches }} total matches reported</div>
    </div>

    <div class="columns">
        
        <!-- Match Results by League -->
        {% for league in data.leagues %}
        {% set all_matches = league.matches %}
        
        {% if all_matches %}
        <div class="matches-section">
            <div class="section-header" style="margin-bottom: 15px;"><a href="{{ league.url }}">{{ league.name }} Results</a></div>
            <table class="matches-table">
                <thead>
                    <tr>
                        <th class="match-time">Time</th>
                        <th class="status-icon"></th>
                        <th class="match-teams">Match</th>
                        <th class="match-score">Score</th>
                    </tr>
                </thead>
                <tbody>
                    {% for match in all_matches %}
                    <tr>
                        <td class="match-time">{{ match.date_time }}</td>
                        <td class="status-icon">{{ match.status_icon }}</td>
                        <td class="match-teams">{{ match.home_team }} vs {{ match.away_team }}</td>
                        <td class="match-score">
                            {% if match.status == 'FINISHED' %}
                                {{ match.score_home }}-{{ match.score_away }}
                            {% else %}
                                vs
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endif %}
        {% endfor %}
        
        <!-- League Tables -->
        {% if data.pl_standings %}
        <div class="standings-section">
            <div class="section-header" style="margin-bottom: 15px;">Premier League Table</div>
            <table class="standings-table">
                <thead>
                    <tr>
                        <th class="pos">Pos</th>
                        <th class="team">Team</th>
                        <th class="stats">P</th>
                        <th class="stats">W</th>
                        <th class="stats">D</th>
                        <th class="stats">L</th>
                        <th class="stats">GF</th>
                        <th class="stats">GA</th>
                        <th class="stats">GD</th>
                        <th class="stats">Pts</th>
                    </tr>
                </thead>
                <tbody>
                    {% for team in data.pl_standings[:5] %}
                    <tr>
                        <td class="pos">{{ team.position }}</td>
                        <td class="team">{{ team.team.shortName }}</td>
                        <td class="stats">{{ team.playedGames }}</td>
                        <td class="stats">{{ team.won }}</td>
                        <td class="stats">{{ team.draw }}</td>
                        <td class="stats">{{ team.lost }}</td>
                        <td class="stats">{{ team.goalsFor }}</td>
                        <td class="stats">{{ team.goalsAgainst }}</td>
                        <td class="stats">{{ team.goalDifference }}</td>
                        <td class="stats"><strong>{{ team.points }}</strong></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endif %}

        {% if data.la_liga_standings %}
        <div class="standings-section">
            <div class="section-header" style="margin-bottom: 15px;">La Liga Table</div>
            <table class="standings-table">
                <thead>
                    <tr>
                        <th class="pos">Pos</th>
                        <th class="team">Team</th>
                        <th class="stats">P</th>
                        <th class="stats">W</th>
                        <th class="stats">D</th>
                        <th class="stats">L</th>
                        <th class="stats">GF</th>
                        <th class="stats">GA</th>
                        <th class="stats">GD</th>
                        <th class="stats">Pts</th>
                    </tr>
                </thead>
                <tbody>
                    {% for team in data.la_liga_standings[:5] %}
                    <tr>
                        <td class="pos">{{ team.position }}</td>
                        <td class="team">{{ team.team.shortName }}</td>
                        <td class="stats">{{ team.playedGames }}</td>
                        <td class="stats">{{ team.won }}</td>
                        <td class="stats">{{ team.draw }}</td>
                        <td class="stats">{{ team.lost }}</td>
                        <td class="stats">{{ team.goalsFor }}</td>
                        <td class="stats">{{ team.goalsAgainst }}</td>
                        <td class="stats">{{ team.goalDifference }}</td>
                        <td class="stats"><strong>{{ team.points }}</strong></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endif %}
        
        <!-- Top Scorers -->
        {% if data.pl_scorers %}
        <div class="scorers-section">
            <div class="section-header" style="margin-bottom: 15px;">Premier League Top Scorers</div>
            <ul class="scorers-list">
                {% for scorer in data.pl_scorers[:5] %}
                <li class="scorer-item">
                    <div class="scorer-info">
                        <div class="scorer-pos">{{ loop.index }}</div>
                        <div>
                            <div class="scorer-name">{{ scorer.player.name }}</div>
                            <div class="scorer-team">{{ scorer.team.shortName }}</div>
                        </div>
                    </div>
                    <div class="scorer-goals">{{ scorer.goals }}</div>
                </li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}

        {% if data.la_liga_scorers %}
        <div class="scorers-section">
            <div class="section-header" style="margin-bottom: 15px;">La Liga Top Scorers</div>
            <ul class="scorers-list">
                {% for scorer in data.la_liga_scorers[:5] %}
                <li class="scorer-item">
                    <div class="scorer-info">
                        <div class="scorer-pos">{{ loop.index }}</div>
                        <div>
                            <div class="scorer-name">{{ scorer.player.name }}</div>
                            <div class="scorer-team">{{ scorer.team.shortName }}</div>
                        </div>
                    </div>
                    <div class="scorer-goals">{{ scorer.goals }}</div>
                </li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
    </div>
    
    <div style="text-align: center; margin-top: 30px; font-size: 10px; color: #888; border-top: 1px solid #ccc; padding-top: 10px;">
        THE FOOTBALL TIMES • Sports Department • Powered by Football-Data.org • All times in IST
    </div>
</body>
</html>
    '''
    
    return render_template_string(html_template, data=data, datetime=datetime)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
