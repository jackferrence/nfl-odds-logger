import requests
import csv
import os
from datetime import datetime, timedelta
import json

# -------------------------
# CONFIG
# -------------------------
API_KEY = "2acee0032b65084c9ec4431cfecbbff5"  # <-- replace with your Odds API key
SPORT = "americanfootball_nfl"
REGION = "us"  # "us", "uk", "au", "eu"
MARKETS = "h2h,spreads,totals"  # moneyline, spreads, totals
ODDS_FORMAT = "american"  # "american" or "decimal"
DATE_FORMAT = "%Y-%m-%d"

# -------------------------
# FUNCTIONS
# -------------------------
def fetch_odds():
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds/"
    params = {
        "apiKey": API_KEY,
        "regions": REGION,
        "markets": MARKETS,
        "oddsFormat": ODDS_FORMAT,
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return None

    return response.json()


def record_api_usage():
    """Record API usage for tracking"""
    usage_file = "api_usage.json"
    
    if os.path.exists(usage_file):
        with open(usage_file, 'r') as f:
            data = json.load(f)
    else:
        data = {"calls": [], "monthly_limit": 500}
    
    now = datetime.now()
    data["calls"].append({
        "timestamp": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "hour": now.hour
    })
    
    # Clean up old calls (older than 2 months)
    cutoff = now - timedelta(days=60)
    data["calls"] = [
        call for call in data["calls"] 
        if datetime.fromisoformat(call["timestamp"]) > cutoff
    ]
    
    with open(usage_file, 'w') as f:
        json.dump(data, f, indent=2)

def save_to_csv(data):
    """Save odds data to CSV file"""
    if not data:
        print("❌ No data to save")
        return
    
    # Create filename with current date
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"nfl_odds_{today}.csv"
    
    # Check if file exists to determine if we need headers
    file_exists = os.path.exists(filename)
    
    # Save to daily CSV file
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['timestamp', 'game_id', 'commence_time', 'home_team', 'away_team', 
                     'bookmaker', 'market', 'outcome_name', 'price', 'point']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        for game in data:
            for bookmaker in game['bookmakers']:
                for market in bookmaker['markets']:
                    for outcome in market['outcomes']:
                        writer.writerow({
                            'timestamp': datetime.now().isoformat(),
                            'game_id': game['id'],
                            'commence_time': game['commence_time'],
                            'home_team': game['home_team'],
                            'away_team': game['away_team'],
                            'bookmaker': bookmaker['key'],
                            'market': market['key'],
                            'outcome_name': outcome['name'],
                            'price': outcome['price'],
                            'point': outcome.get('point', '')
                        })
    
    print(f"✅ Data saved to {filename}")




# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    print("🏈 NFL Odds Logger")
    print("=" * 40)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check API key
    api_key = os.environ.get('ODDS_API_KEY')
    if not api_key:
        print("❌ ERROR: ODDS_API_KEY environment variable not set!")
        print("Please set your API key in Railway environment variables")
        exit(1)
    
    print(f"✅ API Key found: {api_key[:8]}...")
    
    # Fetch odds data
    print("🔄 Fetching NFL odds from API...")
    odds_data = fetch_odds()
    
    if odds_data:
        print(f"✅ Fetched data for {len(odds_data)} games")
        save_to_csv(odds_data)
        record_api_usage()  # Track API usage
        print("✅ Data collection completed successfully!")
        
        # Show usage stats
        try:
            from api_usage_tracker import get_usage_stats
            stats = get_usage_stats()
            print(f"📊 API Usage: {stats['current_month']}/{stats['monthly_limit']} calls ({stats['usage_percentage']:.1f}%)")
        except Exception as e:
            print(f"⚠️ Could not display usage stats: {e}")
    else:
        print("❌ Failed to fetch odds data")
        exit(1)
    
    print(f"🕐 Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
