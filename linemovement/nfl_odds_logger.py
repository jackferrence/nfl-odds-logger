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
    # Create filename for today
    today = datetime.now().strftime(DATE_FORMAT)
    filename = f"nfl_odds_{today}.csv"

    # Ensure file exists, otherwise create header
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            # Write header once
            writer.writerow([
                "timestamp", "game_id", "commence_time", "home_team", "away_team",
                "bookmaker", "market", "outcome_name", "price", "point"
            ])

        timestamp = datetime.now().isoformat()

        for game in data:
            game_id = game.get("id")
            commence_time = game.get("commence_time")
            home_team = game.get("home_team")
            away_team = game.get("away_team")

            for book in game.get("bookmakers", []):
                bookmaker = book.get("title")

                for market in book.get("markets", []):
                    market_key = market.get("key")

                    for outcome in market.get("outcomes", []):
                        writer.writerow([
                            timestamp,
                            game_id,
                            commence_time,
                            home_team,
                            away_team,
                            bookmaker,
                            market_key,
                            outcome.get("name"),
                            outcome.get("price"),
                            outcome.get("point"),
                        ])


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    print("Fetching NFL odds...")

    odds_data = fetch_odds()
    if odds_data:
        save_to_csv(odds_data)
        record_api_usage()  # Track API usage
        print("✅ Odds appended to today's CSV.")
        
        # Show usage stats
        try:
            from api_usage_tracker import get_usage_stats
            stats = get_usage_stats()
            print(f"📊 API Usage: {stats['current_month']}/{stats['monthly_limit']} calls ({stats['usage_percentage']:.1f}%)")
        except:
            pass
