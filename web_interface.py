#!/usr/bin/env python3
"""
Web Interface for NFL Odds Logger
Simple Flask app to view odds data and usage stats
"""

from flask import Flask, render_template_string, jsonify, request
import pandas as pd
import os
import json
from datetime import datetime, timedelta
import glob

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>NFL Odds Logger Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: #f5f5f5; 
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            padding: 20px; 
            border-radius: 8px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
        }
        .header { 
            text-align: center; 
            margin-bottom: 30px; 
            color: #333; 
        }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }
        .stat-card { 
            background: #f8f9fa; 
            padding: 20px; 
            border-radius: 8px; 
            text-align: center; 
        }
        .stat-value { 
            font-size: 2em; 
            font-weight: bold; 
            color: #007bff; 
        }
        .stat-label { 
            color: #666; 
            margin-top: 5px; 
        }
        .table-container { 
            overflow-x: auto; 
            margin-top: 20px; 
        }
        table { 
            width: 100%; 
            border-collapse: collapse; 
        }
        th, td { 
            padding: 12px; 
            text-align: left; 
            border-bottom: 1px solid #ddd; 
        }
        th { 
            background: #f8f9fa; 
            font-weight: 600; 
        }
        .refresh-btn { 
            background: #007bff; 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 5px; 
            cursor: pointer; 
            margin-bottom: 20px; 
        }
        .refresh-btn:hover { 
            background: #0056b3; 
        }
        .status { 
            padding: 10px; 
            border-radius: 5px; 
            margin-bottom: 20px; 
        }
        .status.running { 
            background: #d4edda; 
            color: #155724; 
            border: 1px solid #c3e6cb; 
        }
        .status.stopped { 
            background: #f8d7da; 
            color: #721c24; 
            border: 1px solid #f5c6cb; 
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
                <div class="stat-value">{{ total_picks }}</div>
                <div class="stat-label">Total Picks</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ api_calls }}</div>
                <div class="stat-label">API Calls This Month</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ remaining_calls }}</div>
                <div class="stat-label">Remaining Calls</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ usage_percent }}%</div>
                <div class="stat-label">Usage</div>
            </div>
        </div>
        
        <h3>Recent Odds Data</h3>
        <div class="table-container">
            {{ table_html|safe }}
        </div>
        
        <h3>Download Data</h3>
        <p>
            <a href="/download/latest" class="refresh-btn" style="text-decoration: none; display: inline-block;">
                📥 Download Latest CSV
            </a>
        </p>
    </div>
</body>
</html>
"""

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
            
            return {
                "calls": len(current_month_calls),
                "limit": data["monthly_limit"],
                "remaining": data["monthly_limit"] - len(current_month_calls),
                "usage_percent": (len(current_month_calls) / data["monthly_limit"]) * 100
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
            total_picks = len(df)
            
            # Get recent data (last 50 rows)
            recent_df = df.tail(50)
            
            # Create HTML table
            table_html = recent_df.to_html(
                classes="table", 
                table_id="odds-table",
                escape=False,
                index=False
            )
            
            last_update = datetime.fromtimestamp(os.path.getctime(latest_file)).strftime("%Y-%m-%d %H:%M:%S")
            
        except Exception as e:
            total_picks = 0
            table_html = f"<p>Error reading data: {str(e)}</p>"
            last_update = "Unknown"
    else:
        total_picks = 0
        table_html = "<p>No data available yet. The logger will start collecting data soon.</p>"
        last_update = "No data"
    
    # Get usage stats
    usage_stats = get_usage_stats()
    
    return render_template_string(HTML_TEMPLATE,
        total_picks=total_picks,
        api_calls=usage_stats["calls"],
        remaining_calls=usage_stats["remaining"],
        usage_percent=f"{usage_stats['usage_percent']:.1f}",
        table_html=table_html,
        last_update=last_update
    )

@app.route('/api/stats')
def api_stats():
    """API endpoint for stats"""
    latest_file = get_latest_csv_file()
    usage_stats = get_usage_stats()
    
    stats = {
        "total_picks": 0,
        "api_calls": usage_stats["calls"],
        "remaining_calls": usage_stats["remaining"],
        "usage_percent": usage_stats["usage_percent"],
        "last_update": "No data"
    }
    
    if latest_file:
        try:
            df = pd.read_csv(latest_file)
            stats["total_picks"] = len(df)
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
    except ImportError:
        print("Installing required packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flask", "pandas"])
    
    print("🌐 Starting web interface...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
