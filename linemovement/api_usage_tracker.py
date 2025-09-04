#!/usr/bin/env python3
"""
API Usage Tracker for The Odds API
Monitors API calls to stay under 500/month limit
"""

import os
import json
from datetime import datetime, timedelta

USAGE_FILE = "api_usage.json"

def load_usage_data():
    """Load usage data from file"""
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, 'r') as f:
            return json.load(f)
    return {"calls": [], "monthly_limit": 500}

def save_usage_data(data):
    """Save usage data to file"""
    with open(USAGE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def record_api_call():
    """Record an API call"""
    data = load_usage_data()
    now = datetime.now()
    
    # Add this call
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
    
    save_usage_data(data)
    return data

def get_current_month_usage():
    """Get usage for current month"""
    data = load_usage_data()
    now = datetime.now()
    current_month = now.strftime("%Y-%m")
    
    current_month_calls = [
        call for call in data["calls"]
        if call["date"].startswith(current_month)
    ]
    
    return len(current_month_calls)

def get_usage_stats():
    """Get comprehensive usage statistics"""
    data = load_usage_data()
    now = datetime.now()
    
    # Current month
    current_month = now.strftime("%Y-%m")
    current_month_calls = [
        call for call in data["calls"]
        if call["date"].startswith(current_month)
    ]
    
    # Last 7 days
    week_ago = now - timedelta(days=7)
    week_calls = [
        call for call in data["calls"]
        if datetime.fromisoformat(call["timestamp"]) > week_ago
    ]
    
    # Calls by hour (for pattern analysis)
    hour_counts = {}
    for call in current_month_calls:
        hour = call["hour"]
        hour_counts[hour] = hour_counts.get(hour, 0) + 1
    
    return {
        "current_month": len(current_month_calls),
        "last_7_days": len(week_calls),
        "monthly_limit": data["monthly_limit"],
        "remaining_calls": data["monthly_limit"] - len(current_month_calls),
        "usage_percentage": (len(current_month_calls) / data["monthly_limit"]) * 100,
        "calls_by_hour": hour_counts,
        "days_remaining_in_month": (datetime(now.year, now.month + 1, 1) - now).days
    }

def print_usage_report():
    """Print a detailed usage report"""
    stats = get_usage_stats()
    
    print("📊 API Usage Report")
    print("=" * 40)
    print(f"Current Month Calls: {stats['current_month']}")
    print(f"Monthly Limit: {stats['monthly_limit']}")
    print(f"Remaining Calls: {stats['remaining_calls']}")
    print(f"Usage: {stats['usage_percentage']:.1f}%")
    print(f"Days Remaining: {stats['days_remaining_in_month']}")
    print()
    
    if stats['remaining_calls'] > 0:
        daily_budget = stats['remaining_calls'] / max(stats['days_remaining_in_month'], 1)
        print(f"💡 Daily Budget: {daily_budget:.1f} calls/day")
    
    print("\n🕐 Calls by Hour (Current Month):")
    for hour in sorted(stats['calls_by_hour'].keys()):
        count = stats['calls_by_hour'][hour]
        bar = "█" * min(count, 20)
        print(f"  {hour:2d}:00 - {count:2d} calls {bar}")
    
    print(f"\n📈 Last 7 Days: {stats['last_7_days']} calls")
    
    # Warnings
    if stats['usage_percentage'] > 80:
        print("\n⚠️  WARNING: You're using over 80% of your monthly limit!")
    elif stats['usage_percentage'] > 60:
        print("\n⚠️  CAUTION: You're using over 60% of your monthly limit")
    else:
        print("\n✅ Usage is within safe limits")

if __name__ == "__main__":
    # Record this check as an API call (optional)
    # record_api_call()
    
    print_usage_report()
