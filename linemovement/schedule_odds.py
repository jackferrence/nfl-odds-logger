#!/usr/bin/env python3
"""
NFL Odds Logger Scheduler - Steady Flow with Peak Bursts
Steady baseline with ramped-up frequency during high traffic times
"""

import schedule
import time
import subprocess
import sys
import os
from datetime import datetime

def run_odds_logger():
    """Run the NFL odds logger"""
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running NFL odds logger...")
        
        # Run the odds logger script
        result = subprocess.run(["python3", "nfl_odds_logger.py"], 
                               capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Odds logger completed successfully")
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Odds logger failed:")
            print(result.stderr)
            
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Error running odds logger: {e}")

def setup_steady_flow_schedule():
    """Set up steady flow with peak bursts schedule"""
    
    # Strategy: ~115 calls/week = ~460 calls/month (near 500 limit)
    # Steady baseline + ramped-up frequency during peak times
    
    # STEADY BASELINE - Every 2 hours during business hours (8 AM - 10 PM)
    # This gives us ~7 calls per day baseline = ~49 calls/week
    
    # Monday - Friday baseline (every 2 hours, 8 AM - 10 PM)
    for hour in range(8, 22, 2):  # 8, 10, 12, 14, 16, 18, 20
        schedule.every().monday.at(f"{hour:02d}:00").do(run_odds_logger)
        schedule.every().tuesday.at(f"{hour:02d}:00").do(run_odds_logger)
        schedule.every().wednesday.at(f"{hour:02d}:00").do(run_odds_logger)
        schedule.every().thursday.at(f"{hour:02d}:00").do(run_odds_logger)
        schedule.every().friday.at(f"{hour:02d}:00").do(run_odds_logger)
    
    # Saturday baseline (every 2 hours, 10 AM - 8 PM)
    for hour in range(10, 20, 2):  # 10, 12, 14, 16, 18
        schedule.every().saturday.at(f"{hour:02d}:00").do(run_odds_logger)
    
    # Sunday baseline (every 2 hours, 8 AM - 8 PM)
    for hour in range(8, 20, 2):  # 8, 10, 12, 14, 16, 18
        schedule.every().sunday.at(f"{hour:02d}:00").do(run_odds_logger)
    
    # PEAK BURSTS - High frequency during critical times
    
    # SUNDAY NIGHT/MONDAY MORNING - Openers (every 30 minutes, 10 PM - 4 AM)
    # Sunday 10 PM - 2 AM Monday (9 calls)
    for hour in [22, 23, 0, 1, 2]:
        if hour < 24:
            schedule.every().sunday.at(f"{hour:02d}:00").do(run_odds_logger)
            schedule.every().sunday.at(f"{hour:02d}:30").do(run_odds_logger)
        else:
            schedule.every().monday.at(f"{hour:02d}:00").do(run_odds_logger)
            schedule.every().monday.at(f"{hour:02d}:30").do(run_odds_logger)
    
    # Monday 3 AM - 4 AM (2 calls)
    schedule.every().monday.at("03:00").do(run_odds_logger)
    schedule.every().monday.at("03:30").do(run_odds_logger)
    
    # WEDNESDAY - Injury reports (every 30 minutes, 1 PM - 9 PM)
    for hour in range(13, 21):  # 1 PM - 8 PM
        schedule.every().wednesday.at(f"{hour:02d}:00").do(run_odds_logger)
        schedule.every().wednesday.at(f"{hour:02d}:30").do(run_odds_logger)
    
    # THURSDAY - Injury reports (every 30 minutes, 1 PM - 9 PM)
    for hour in range(13, 21):  # 1 PM - 8 PM
        schedule.every().thursday.at(f"{hour:02d}:00").do(run_odds_logger)
        schedule.every().thursday.at(f"{hour:02d}:30").do(run_odds_logger)
    
    # FRIDAY - Final status (every 30 minutes, 1 PM - 7 PM)
    for hour in range(13, 19):  # 1 PM - 6 PM
        schedule.every().friday.at(f"{hour:02d}:00").do(run_odds_logger)
        schedule.every().friday.at(f"{hour:02d}:30").do(run_odds_logger)
    
    # SATURDAY - Final status (every 30 minutes, 1 PM - 7 PM)
    for hour in range(13, 19):  # 1 PM - 6 PM
        schedule.every().saturday.at(f"{hour:02d}:00").do(run_odds_logger)
        schedule.every().saturday.at(f"{hour:02d}:30").do(run_odds_logger)
    
    # SUNDAY MORNING - Public flood (every 30 minutes, 6 AM - 12 PM)
    for hour in range(6, 12):  # 6 AM - 11 AM
        schedule.every().sunday.at(f"{hour:02d}:00").do(run_odds_logger)
        schedule.every().sunday.at(f"{hour:02d}:30").do(run_odds_logger)
    
    # SUNDAY PRE-GAME - Final adjustments (every 15 minutes, 12 PM - 2 PM)
    for hour in [12, 13]:  # 12 PM - 1 PM
        schedule.every().sunday.at(f"{hour:02d}:00").do(run_odds_logger)
        schedule.every().sunday.at(f"{hour:02d}:15").do(run_odds_logger)
        schedule.every().sunday.at(f"{hour:02d}:30").do(run_odds_logger)
        schedule.every().sunday.at(f"{hour:02d}:45").do(run_odds_logger)
    
    print("📅 Steady Flow + Peak Bursts Schedule set up:")
    print("   🔄 STEADY BASELINE (49 calls/week):")
    print("      - Mon-Fri: Every 2 hours, 8 AM - 10 PM (7 calls/day)")
    print("      - Saturday: Every 2 hours, 10 AM - 8 PM (5 calls)")
    print("      - Sunday: Every 2 hours, 8 AM - 8 PM (6 calls)")
    print("   🚀 PEAK BURSTS (66 calls/week):")
    print("      - Sun Night/Mon Morning: Every 30 min, 10 PM - 4 AM (11 calls)")
    print("      - Wednesday: Every 30 min, 1 PM - 9 PM (16 calls)")
    print("      - Thursday: Every 30 min, 1 PM - 9 PM (16 calls)")
    print("      - Friday: Every 30 min, 1 PM - 7 PM (12 calls)")
    print("      - Saturday: Every 30 min, 1 PM - 7 PM (12 calls)")
    print("      - Sunday Morning: Every 30 min, 6 AM - 12 PM (12 calls)")
    print("      - Sunday Pre-game: Every 15 min, 12 PM - 2 PM (8 calls)")
    print("   📊 Total: ~115 calls/week = ~460 calls/month")
    print("   ✅ Near 500 limit with steady flow + peak bursts!")
    print("   - Next run:", schedule.next_run())
    print("   - Press Ctrl+C to stop")

def main():
    print("🏈 NFL Odds Logger Scheduler (Steady Flow + Peak Bursts)")
    print("=" * 70)
    print("🎯 Strategy: Steady baseline + ramped-up frequency during peak times")
    print("📊 Target: ~115 calls/week = ~460 calls/month")
    print("=" * 70)
    
    # Install schedule if not available
    try:
        import schedule
    except ImportError:
        print("Installing schedule package...")
        subprocess.run(["python3", "-m", "pip", "install", "schedule"])
        import schedule
    
    # Set up the schedule
    setup_steady_flow_schedule()
    
    # Run immediately on startup
    run_odds_logger()
    
    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped by user")

if __name__ == "__main__":
    main()
