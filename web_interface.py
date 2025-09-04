#!/usr/bin/env python3
"""
NFL Odds Logger - Web Interface
Provides a clean dashboard for viewing odds data
"""

import os
import json
import glob
import pandas as pd
from datetime import datetime
from flask import Flask, render_template_string, jsonify
import pytz

app = Flask(__name__)

# HTML Template with improved formatting
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>NFL Odds Logger Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        .header h1 { 
            font-size: 2.5rem; 
            margin-bottom: 10px; 
        }
        .header p { 
            font-size: 1.1rem; 
            opacity: 0.9; 
        }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px; 
            margin-bottom: 30px; 
        }
        .stat-card { 
            background: white; 
            padding: 25px; 
            border-radius: 10px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            border-left: 4px solid #667eea;
        }
        .stat-value { 
            font-size: 2rem; 
            font-weight: bold; 
            color: #667eea; 
            margin-bottom: 5px; 
        }
        .stat-label { 
            color: #666; 
            font-size: 0.9rem; 
            text-transform: uppercase; 
            letter-spacing: 0.5px; 
        }
        .status { 
            padding: 15px 20px; 
            border-radius: 8px; 
            margin-bottom: 30px; 
            font-weight: 500;
        }
        .status.running { 
            background: #d4edda; 
            color: #155724; 
            border: 1px solid #c3e6cb; 
        }
        .refresh-btn { 
            background: #667eea; 
            color: white; 
            border: none; 
            padding: 12px 24px; 
            border-radius: 6px; 
            cursor: pointer; 
            margin-bottom: 30px; 
            font-size: 1rem;
            transition: background 0.3s;
        }
        .refresh-btn:hover { 
            background: #5a6fd8; 
        }
        .games-container {
            display: grid;
            gap: 25px;
            margin-bottom: 30px;
        }
        .game-card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .game-header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .game-teams {
            font-size: 1.3rem;
            font-weight: bold;
        }
        .game-time {
            font-size: 0.9rem;
            opacity: 0.8;
        }
        .game-content {
            padding: 20px;
        }
        .bet-type-section {
            margin-bottom: 25px;
        }
        .bet-type-title {
            font-size: 1.1rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #ecf0f1;
        }
        .bookmakers-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        .bookmaker-card {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            border-left: 3px solid #667eea;
        }
        .bookmaker-name {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .odds-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #e9ecef;
        }
        .odds-row:last-child {
            border-bottom: none;
        }
        .team-name {
            font-weight: 500;
            color: #495057;
        }
        .odds-value {
            font-weight: bold;
            color: #667eea;
        }
        .point-value {
            color: #6c757d;
            font-size: 0.9rem;
        }
        .last-updated {
            text-align: center;
            color: #6c757d;
            font-size: 0.9rem;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
        }
        .no-data {
            text-align: center;
            padding: 40px;
            color: #6c757d;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏈 NFL Odds Logger Dashboard</h1>
            <p>Real-time odds tracking and line movement analysis</p>
        </div>
        
        <div class="status running">
            ✅ Service is running - Last updated: {{ last_update }}
        </div>
        
        <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Data</button>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{{ total_games }}</div>
                <div class="stat-label">Active Games</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ total_odds }}</div>
                <div class="stat-label">Total Odds</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ api_calls }}</div>
                <div class="stat-label">API Calls This Month</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ remaining_calls }}</div>
                <div class="stat-label">Remaining Calls</div>
            </div>
        </div>
        
        <div class="games-container">
            {{ games_html|safe }}
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="/download/latest" class="refresh-btn" style="text-decoration: none; display: inline-block;">
                📥 Download Latest CSV
            </a>
        </div>
    </div>
</body>
</html>
"""

def format_timestamp(timestamp_str):
    """Convert ISO timestamp to readable format"""
    try:
        # Parse the timestamp
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        # Convert to local timezone (you can change this)
        local_tz = pytz.timezone('America/New_York')
        local_dt = dt.astimezone(local_tz)
        return local_dt.strftime("%B %d, %Y at %I:%M %p ET")
    except:
        return timestamp_str

def format_game_time(commence_time):
    """Format game start time"""
    try:
        # Parse the commence time
        dt = datetime.fromisoformat(commence_time.replace('Z', '+00:00'))
        # Convert to local timezone
        local_tz = pytz.timezone('America/New_York')
        local_dt = dt.astimezone(local_tz)
        return local_dt.strftime("%A, %B %d at %I:%M %p ET")
    except:
        return commence_time

def organize_data_by_games(df):
    """Organize odds data by games"""
    games = {}
    
    for _, row in df.iterrows():
        game_id = row['game_id']
        home_team = row['home_team']
        away_team = row['away_team']
        commence_time = row['commence_time']
        bookmaker = row['bookmaker']
        market = row['market']
        outcome_name = row['outcome_name']
        price = row['price']
        point = row['point']
        
        if game_id not in games:
            games[game_id] = {
                'home_team': home_team,
                'away_team': away_team,
                'commence_time': commence_time,
                'bookmakers': {}
            }
        
        if bookmaker not in games[game_id]['bookmakers']:
            games[game_id]['bookmakers'][bookmaker] = {}
        
        if market not in games[game_id]['bookmakers'][bookmaker]:
            games[game_id]['bookmakers'][bookmaker][market] = []
        
        games[game_id]['bookmakers'][bookmaker][market].append({
            'outcome_name': outcome_name,
            'price': price,
            'point': point
        })
    
    return games

def generate_games_html(games):
    """Generate HTML for games display"""
    if not games:
        return '<div class="no-data">No games data available yet. The logger will start collecting data soon.</div>'
    
    html_parts = []
    
    for game_id, game_data in games.items():
        # Game header
        game_html = f'''
        <div class="game-card">
            <div class="game-header">
                <div class="game-teams">{game_data['away_team']} @ {game_data['home_team']}</div>
                <div class="game-time">{format_game_time(game_data['commence_time'])}</div>
            </div>
            <div class="game-content">
        '''
        
        # Process each bookmaker
        for bookmaker, markets in game_data['bookmakers'].items():
            for market, odds in markets.items():
                # Market title
                market_title = market.upper()
                if market == 'h2h':
                    market_title = 'MONEYLINE'
                elif market == 'spreads':
                    market_title = 'POINT SPREAD'
                elif market == 'totals':
                    market_title = 'TOTAL POINTS'
                
                game_html += f'<div class="bet-type-section">'
                game_html += f'<div class="bet-type-title">{market_title}</div>'
                game_html += f'<div class="bookmakers-grid">'
                
                # Bookmaker card
                game_html += f'<div class="bookmaker-card">'
                game_html += f'<div class="bookmaker-name">{bookmaker}</div>'
                
                for odd in odds:
                    team_name = odd['outcome_name']
                    price = odd['price']
                    point = odd['point']
                    
                    # Format price
                    if price > 0:
                        price_display = f"+{price}"
                    else:
                        price_display = str(price)
                    
                    # Format point (for spreads/totals)
                    point_display = ""
                    if pd.notna(point) and point != "":
                        if market == 'totals':
                            point_display = f"O/U {point}"
                        else:
                            point_display = f"({point})"
                    
                    game_html += f'''
                    <div class="odds-row">
                        <span class="team-name">{team_name}</span>
                        <div>
                            <span class="odds-value">{price_display}</span>
                            <span class="point-value">{point_display}</span>
                        </div>
                    </div>
                    '''
                
                game_html += '</div>'  # Close bookmaker-card
                game_html += '</div>'  # Close bookmakers-grid
                game_html += '</div>'  # Close bet-type-section
        
        game_html += '</div></div>'  # Close game-content and game-card
        html_parts.append(game_html)
    
    return '\n'.join(html_parts)

def get_latest_csv_file():
    """Get the most recent CSV file"""
    csv_files = glob.glob("nfl_odds_*.csv")
    if not csv_files:
        return None
    return max(csv_files, key=os.path.getctime)

def get_usage_stats():
    """Get API usage statistics"""
    try:
        if os.path.exists("api_usage.json"):
            with open("api_usage.json", "r") as f:
                data = json.load(f)
            
            now = datetime.now()
            current_month = now.strftime("%Y-%m")
            
            current_month_calls = [
                call for call in data["calls"]
                if call["date"].startswith(current_month)
            ]
            
            calls_this_month = len(current_month_calls)
            remaining = 500 - calls_this_month
            usage_percent = (calls_this_month / 500) * 100
            
            return {
                "calls": calls_this_month,
                "limit": 500,
                "remaining": remaining,
                "usage_percent": usage_percent
            }
    except:
        pass
    
    return {"calls": 0, "limit": 500, "remaining": 500, "usage_percent": 0}

@app.route('/')
def dashboard():
    """Main dashboard"""
    # Get latest CSV file
    latest_file = get_latest_csv_file()
    
    if latest_file:
        try:
            # Read the latest CSV
            df = pd.read_csv(latest_file)
            
            # Organize data by games
            games = organize_data_by_games(df)
            
            # Generate games HTML
            games_html = generate_games_html(games)
            
            # Calculate stats
            total_games = len(games)
            total_odds = len(df)
            
            last_update = format_timestamp(datetime.fromtimestamp(os.path.getctime(latest_file)).isoformat())
            
        except Exception as e:
            total_games = 0
            total_odds = 0
            games_html = f'<div class="no-data">Error reading data: {str(e)}</div>'
            last_update = "Unknown"
    else:
        total_games = 0
        total_odds = 0
        games_html = '<div class="no-data">No data available yet. The logger will start collecting data soon.</div>'
        last_update = "No data"
    
    # Get usage stats
    usage_stats = get_usage_stats()
    
    return render_template_string(HTML_TEMPLATE,
        total_games=total_games,
        total_odds=total_odds,
        api_calls=usage_stats["calls"],
        remaining_calls=usage_stats["remaining"],
        games_html=games_html,
        last_update=last_update
    )

@app.route('/api/stats')
def api_stats():
    """API endpoint for stats"""
    latest_file = get_latest_csv_file()
    usage_stats = get_usage_stats()
    
    stats = {
        "total_games": 0,
        "total_odds": 0,
        "api_calls": usage_stats["calls"],
        "remaining_calls": usage_stats["remaining"],
        "usage_percent": usage_stats["usage_percent"],
        "last_update": "No data"
    }
    
    if latest_file:
        try:
            df = pd.read_csv(latest_file)
            games = organize_data_by_games(df)
            stats["total_games"] = len(games)
            stats["total_odds"] = len(df)
            stats["last_update"] = datetime.fromtimestamp(os.path.getctime(latest_file)).isoformat()
        except:
            pass
    
    return jsonify(stats)

@app.route('/download/latest')
def download_latest():
    """Download the latest CSV file"""
    latest_file = get_latest_csv_file()
    if latest_file:
        from flask import send_file
        return send_file(latest_file, as_attachment=True)
    else:
        return "No data available", 404

if __name__ == '__main__':
    # Install required packages
    import subprocess
    import sys
    
    try:
        import flask
        import pandas
        import pytz
    except ImportError:
        print("Installing required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flask", "pandas", "pytz"])
    
    print("🌐 Starting web interface...")
    # Use Railway's PORT environment variable, default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    print(f"📊 Dashboard will be available at: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
