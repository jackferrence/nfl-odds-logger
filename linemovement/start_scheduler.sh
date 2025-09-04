#!/bin/bash

# NFL Odds Logger Scheduler Launcher - Steady Flow + Peak Bursts
echo "🏈 Starting NFL Odds Logger Scheduler (Steady Flow + Peak Bursts)..."

# Navigate to the script directory
cd "$(dirname "$0")"

# Install dependencies if needed
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Start the steady flow scheduler
echo "🚀 Starting steady flow scheduler..."
python3 schedule_odds_steady_flow.py
