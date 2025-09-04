# NFL Odds Logger - Steady Flow + Peak Bursts

A Python script that fetches NFL odds from The Odds API with steady baseline monitoring plus ramped-up frequency during peak betting hours.

## 🎯 Steady Flow + Peak Bursts Strategy

- **~115 calls per week** = ~460 calls/month (near 500 limit)
- **Steady baseline** - Never more than 2 hours between checks
- **Peak bursts** - High frequency during critical times

## 📅 Schedule

### 🔄 Steady Baseline (49 calls/week)
- **Monday-Friday**: Every 2 hours, 8 AM - 10 PM (7 calls/day)
- **Saturday**: Every 2 hours, 10 AM - 8 PM (5 calls)
- **Sunday**: Every 2 hours, 8 AM - 8 PM (6 calls)

### 🚀 Peak Bursts (66 calls/week)
- **Sunday Night/Monday Morning**: Every 30 min, 10 PM - 4 AM (11 calls)
- **Wednesday**: Every 30 min, 1 PM - 9 PM (16 calls)
- **Thursday**: Every 30 min, 1 PM - 9 PM (16 calls)
- **Friday**: Every 30 min, 1 PM - 7 PM (12 calls)
- **Saturday**: Every 30 min, 1 PM - 7 PM (12 calls)
- **Sunday Morning**: Every 30 min, 6 AM - 12 PM (12 calls)
- **Sunday Pre-game**: Every 15 min, 12 PM - 2 PM (8 calls)

## 🚀 Quick Start

### Option 1: Steady Flow Scheduler (Recommended)
```bash
cd linemovement
./start_scheduler.sh
```

### Option 2: Steady Flow Cron Jobs
```bash
cd linemovement
chmod +x setup_cron.sh
./setup_cron.sh
```

### Option 3: Manual Run
```bash
cd linemovement
python3 nfl_odds_logger.py
```

## 📊 Usage Tracking

Monitor your API usage:
```bash
python3 api_usage_tracker.py
```

This shows:
- Current month usage
- Remaining calls
- Usage percentage
- Calls by hour pattern
- Daily budget recommendations

## 📁 Output

- **CSV Files**: `nfl_odds_YYYY-MM-DD.csv`
- **Usage Data**: `api_usage.json`
- **Logs**: Console output with timestamps

## ⚙️ Configuration

Edit `nfl_odds_logger.py` to modify:
- API key
- Sport (currently NFL)
- Markets (h2h, spreads, totals)
- Odds format (American/Decimal)

## 🔧 Dependencies

```bash
pip3 install -r requirements.txt
```

## 📈 Expected Usage

- **Steady Flow + Peak Bursts**: ~115 calls/week = ~460 calls/month
- **Safety Margin**: 40 calls remaining
- **Maximum Coverage**: Steady monitoring + peak bursts
- **Strategic Focus**: Continuous flow with ramped-up frequency during peak times

## ⚠️ Important Notes

- API key is included in the script (replace with your own)
- Data is saved locally in CSV format
- Usage is automatically tracked
- Script runs continuously when using scheduler
- Press Ctrl+C to stop the scheduler

## 🏈 Data Structure

Each CSV row contains:
- timestamp, game_id, commence_time
- home_team, away_team
- bookmaker, market, outcome_name
- price, point

Perfect for analyzing line movements and betting patterns!

Update
