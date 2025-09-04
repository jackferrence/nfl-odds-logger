#!/usr/bin/env python3
"""
NFL Odds Logger - Web Interface
Provides a clean dashboard for viewing odds data with line movement graphs
"""

import os
import json
import glob
import pandas as pd
from datetime import datetime
from flask import Flask, render_template_string, jsonify
import pytz

app = Flask(__name__)

# HTML Template with improved formatting and interactive graphs
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>NFL Odds Logger Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .game-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }
        .game-card.expanded {
            transform: none;
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
        .game-overview {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
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
        .game-details {
            display: none;
            padding: 20px;
            background: #f8f9fa;
            border-top: 1px solid #e9ecef;
        }
        .game-details.expanded {
            display: block;
        }
        .graph-tabs {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 2px solid #e9ecef;
        }
        .graph-tab {
            padding: 12px 24px;
            background: none;
            border: none;
            cursor: pointer;
            font-weight: 500;
            color: #6c757d;
            border-bottom: 2px solid transparent;
            transition: all 0.3s;
        }
        .graph-tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }
        .graph-tab:hover {
            color: #495057;
        }
        .graph-container {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .graph-placeholder {
            text-align: center;
            padding: 40px;
            color: #6c757d;
            font-style: italic;
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
        .expand-icon {
            margin-left: 10px;
            transition: transform 0.3s;
        }
        .expand-icon.expanded {
            transform: rotate(180deg);
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

    <script>
        // Toggle game expansion
        function toggleGame(gameId) {
            const gameCard = document.getElementById(`game-${gameId}`);
            const gameDetails = document.getElementById(`details-${gameId}`);
            const expandIcon = document.getElementById(`expand-${gameId}`);
            
            if (gameDetails.classList.contains('expanded')) {
                gameDetails.classList.remove('expanded');
                gameCard.classList.remove('expanded');
                expandIcon.classList.remove('expanded');
                expandIcon.textContent = '▼';
            } else {
                gameDetails.classList.add('expanded');
                gameCard.classList.add('expanded');
                expandIcon.classList.add('expanded');
                expandIcon.textContent = '▲';
                
                // Load graphs if not already loaded
                if (!gameDetails.dataset.graphsLoaded) {
                    loadGameGraphs(gameId);
                    gameDetails.dataset.graphsLoaded = 'true';
                }
            }
        }

        // Toggle graph tabs
        function showGraphTab(gameId, tabName) {
            // Hide all tabs
            const tabs = document.querySelectorAll(`[data-game="${gameId}"] .graph-tab`);
            const contents = document.querySelectorAll(`[data-game="${gameId}"] .graph-content`);
            
            tabs.forEach(tab => tab.classList.remove('active'));
            contents.forEach(content => content.style.display = 'none');
            
            // Show selected tab
            document.getElementById(`tab-${gameId}-${tabName}`).classList.add('active');
            document.getElementById(`content-${gameId}-${tabName}`).style.display = 'block';
        }

        // Load game graphs
        function loadGameGraphs(gameId) {
            fetch(`/api/game/${gameId}/graphs`)
                .then(response => response.json())
                .then(data => {
                    if (data.spreads) createSpreadChart(gameId, data.spreads);
                    if (data.moneyline) createMoneylineChart(gameId, data.moneyline);
                    if (data.totals) createTotalsChart(gameId, data.totals);
                })
                .catch(error => {
                    console.error('Error loading graphs:', error);
                    document.getElementById(`content-${gameId}-spreads`).innerHTML = 
                        '<div class="graph-placeholder">Error loading line movement data</div>';
                });
        }

        // Create spread chart
        function createSpreadChart(gameId, data) {
            const ctx = document.getElementById(`chart-${gameId}-spreads`);
            if (!ctx) return;

            const datasets = [];
            const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'];
            
            Object.keys(data).forEach((bookmaker, index) => {
                const color = colors[index % colors.length];
                datasets.push({
                    label: bookmaker,
                    data: data[bookmaker].map(point => point.point),
                    borderColor: color,
                    backgroundColor: color + '20',
                    tension: 0.1,
                    pointRadius: 3,
                    pointHoverRadius: 5
                });
            });

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data[Object.keys(data)[0]]?.map(point => point.time) || [],
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Point Spread Movement'
                        },
                        legend: {
                            position: 'top'
                        }
                    },
                    scales: {
                        y: {
                            reverse: true,
                            title: {
                                display: true,
                                text: 'Point Spread'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        }
                    }
                }
            });
        }

        // Create moneyline chart
        function createMoneylineChart(gameId, data) {
            const ctx = document.getElementById(`chart-${gameId}-moneyline`);
            if (!ctx) return;

            const datasets = [];
            const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'];
            
            Object.keys(data).forEach((bookmaker, index) => {
                const color = colors[index % colors.length];
                datasets.push({
                    label: bookmaker,
                    data: data[bookmaker].map(point => point.price),
                    borderColor: color,
                    backgroundColor: color + '20',
                    tension: 0.1,
                    pointRadius: 3,
                    pointHoverRadius: 5
                });
            });

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data[Object.keys(data)[0]]?.map(point => point.time) || [],
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Moneyline Movement'
                        },
                        legend: {
                            position: 'top'
                        }
                    },
                    scales: {
                        y: {
                            title: {
                                display: true,
                                text: 'Odds'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        }
                    }
                }
            });
        }

        // Create totals chart
        function createTotalsChart(gameId, data) {
            const ctx = document.getElementById(`chart-${gameId}-totals`);
            if (!ctx) return;

            const datasets = [];
            const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'];
            
            Object.keys(data).forEach((bookmaker, index) => {
                const color = colors[index % colors.length];
                datasets.push({
                    label: bookmaker,
                    data: data[bookmaker].map(point => point.point),
                    borderColor: color,
                    backgroundColor: color + '20',
                    tension: 0.1,
                    pointRadius: 3,
                    pointHoverRadius: 5
                });
            });

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data[Object.keys(data)[0]]?.map(point => point.time) || [],
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Total Points Movement'
                        },
                        legend: {
                            position: 'top'
                        }
                    },
                    scales: {
                        y: {
                            title: {
                                display: true,
                                text: 'Total Points'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Time'
                            }
                        }
                    }
                }
            });
        }
    </script>
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

def format_time_for_chart(timestamp_str):
    """Format timestamp for chart display"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        local_tz = pytz.timezone('America/New_York')
        local_dt = dt.astimezone(local_tz)
        return local_dt.strftime("%m/%d %H:%M")
    except:
        return timestamp_str

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
        timestamp = row['timestamp']
        
        if game_id not in games:
            games[game_id] = {
                'home_team': home_team,
                'away_team': away_team,
                'commence_time': commence_time,
                'bookmakers': {},
                'historical_data': {}
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
        
        # Store historical data for graphs
        if bookmaker not in games[game_id]['historical_data']:
            games[game_id]['historical_data'][bookmaker] = {}
        
        if market not in games[game_id]['historical_data'][bookmaker]:
            games[game_id]['historical_data'][bookmaker][market] = []
        
        games[game_id]['historical_data'][bookmaker][market].append({
            'timestamp': timestamp,
            'outcome_name': outcome_name,
            'price': price,
            'point': point
        })
    
    return games

def generate_games_html(games):
    """Generate HTML for games display with interactive graphs"""
    if not games:
        return '<div class="no-data">No games data available yet. The logger will start collecting data soon.</div>'
    
    html_parts = []
    
    for game_id, game_data in games.items():
        # Game header
        game_html = f'''
        <div class="game-card" id="game-{game_id}" onclick="toggleGame('{game_id}')">
            <div class="game-header">
                <div class="game-teams">{game_data['away_team']} @ {game_data['home_team']}</div>
                <div class="game-time">
                    {format_game_time(game_data['commence_time'])}
                    <span class="expand-icon" id="expand-{game_id}">▼</span>
                </div>
            </div>
            <div class="game-content">
        '''
        
        # Process each bookmaker for overview
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
        
        game_html += '</div>'  # Close game-content
        
        # Add expandable details section with graphs
        game_html += f'''
        <div class="game-details" id="details-{game_id}" data-game="{game_id}">
            <div class="graph-tabs">
                <button class="graph-tab active" id="tab-{game_id}-spreads" onclick="showGraphTab('{game_id}', 'spreads')">
                    Point Spreads
                </button>
                <button class="graph-tab" id="tab-{game_id}-moneyline" onclick="showGraphTab('{game_id}', 'moneyline')">
                    Moneyline
                </button>
                <button class="graph-tab" id="tab-{game_id}-totals" onclick="showGraphTab('{game_id}', 'totals')">
                    Totals
                </button>
            </div>
            
            <div class="graph-content" id="content-{game_id}-spreads" style="display: block;">
                <div class="graph-container">
                    <canvas id="chart-{game_id}-spreads"></canvas>
                </div>
            </div>
            
            <div class="graph-content" id="content-{game_id}-moneyline" style="display: none;">
                <div class="graph-container">
                    <canvas id="chart-{game_id}-moneyline"></canvas>
                </div>
            </div>
            
            <div class="graph-content" id="content-{game_id}-totals" style="display: none;">
                <div class="graph-container">
                    <canvas id="chart-{game_id}-totals"></canvas>
                </div>
            </div>
        </div>
        '''
        
        game_html += '</div>'  # Close game-card
        html_parts.append(game_html)
    
    return '\n'.join(html_parts)

def get_historical_data_for_game(game_id):
    """Get historical data for a specific game from all CSV files"""
    csv_files = glob.glob("nfl_odds_*.csv")
    if not csv_files:
        return None
    
    all_data = []
    
    for csv_file in sorted(csv_files):
        try:
            df = pd.read_csv(csv_file)
            game_data = df[df['game_id'] == game_id]
            if not game_data.empty:
                all_data.append(game_data)
        except:
            continue
    
    if not all_data:
        return None
    
    # Combine all data and sort by timestamp
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('timestamp')
    
    return combined_df

def organize_graph_data(df, game_id):
    """Organize data for graph display"""
    if df is None or df.empty:
        return None
    
    # Filter for the specific game
    game_data = df[df['game_id'] == game_id]
    if game_data.empty:
        return None
    
    # Organize by market type
    spreads_data = {}
    moneyline_data = {}
    totals_data = {}
    
    for _, row in game_data.iterrows():
        bookmaker = row['bookmaker']
        market = row['market']
        timestamp = row['timestamp']
        outcome_name = row['outcome_name']
        price = row['price']
        point = row['point']
        
        formatted_time = format_time_for_chart(timestamp)
        
        if market == 'spreads':
            if bookmaker not in spreads_data:
                spreads_data[bookmaker] = []
            spreads_data[bookmaker].append({
                'time': formatted_time,
                'point': float(point) if pd.notna(point) and point != "" else None,
                'price': price
            })
        elif market == 'h2h':
            if bookmaker not in moneyline_data:
                moneyline_data[bookmaker] = []
            moneyline_data[bookmaker].append({
                'time': formatted_time,
                'price': price,
                'outcome': outcome_name
            })
        elif market == 'totals':
            if bookmaker not in totals_data:
                totals_data[bookmaker] = []
            totals_data[bookmaker].append({
                'time': formatted_time,
                'point': float(point) if pd.notna(point) and point != "" else None,
                'price': price
            })
    
    return {
        'spreads': spreads_data if spreads_data else None,
        'moneyline': moneyline_data if moneyline_data else None,
        'totals': totals_data if totals_data else None
    }

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

@app.route('/api/game/<game_id>/graphs')
def game_graphs(game_id):
    """API endpoint for game graph data"""
    try:
        # Get historical data for the game
        historical_df = get_historical_data_for_game(game_id)
        
        if historical_df is None:
            return jsonify({'error': 'No data found for this game'})
        
        # Organize data for graphs
        graph_data = organize_graph_data(historical_df, game_id)
        
        return jsonify(graph_data)
    except Exception as e:
        return jsonify({'error': str(e)})

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
