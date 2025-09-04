#!/bin/bash

# Setup cron jobs for NFL Odds Logger - Steady Flow + Peak Bursts
echo "🏈 Setting up cron jobs for NFL Odds Logger (Steady Flow + Peak Bursts)..."

# Get the absolute path to the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_PATH=$(which python3)
LOGGER_SCRIPT="$SCRIPT_DIR/nfl_odds_logger.py"

echo "📍 Script location: $LOGGER_SCRIPT"
echo "🐍 Python path: $PYTHON_PATH"

# Create a temporary file with the cron jobs
TEMP_CRON=$(mktemp)

# Add existing cron jobs (excluding our NFL odds jobs)
crontab -l 2>/dev/null | grep -v "nfl_odds_logger" > "$TEMP_CRON"

# Add our NFL odds logger jobs based on steady flow + peak bursts strategy
echo "# NFL Odds Logger - Steady Flow + Peak Bursts (~115 calls/week)" >> "$TEMP_CRON"

echo "# STEADY BASELINE - Every 2 hours during business hours" >> "$TEMP_CRON"
echo "# Monday-Friday: 8 AM - 10 PM (every 2 hours)" >> "$TEMP_CRON"
for hour in 8 10 12 14 16 18 20; do
    printf "0 %d * * 1-5 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
done

echo "# Saturday: 10 AM - 8 PM (every 2 hours)" >> "$TEMP_CRON"
for hour in 10 12 14 16 18; do
    printf "0 %d * * 6 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
done

echo "# Sunday: 8 AM - 8 PM (every 2 hours)" >> "$TEMP_CRON"
for hour in 8 10 12 14 16 18; do
    printf "0 %d * * 0 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
done

echo "# PEAK BURSTS - High frequency during critical times" >> "$TEMP_CRON"

echo "# Sunday Night/Monday Morning - Openers (every 30 min, 10 PM - 4 AM)" >> "$TEMP_CRON"
printf "0 22 * * 0 %s %s\n" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
printf "30 22 * * 0 %s %s\n" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
printf "0 23 * * 0 %s %s\n" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
printf "30 23 * * 0 %s %s\n" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
printf "0 0 * * 1 %s %s\n" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
printf "30 0 * * 1 %s %s\n" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
printf "0 1 * * 1 %s %s\n" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
printf "30 1 * * 1 %s %s\n" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
printf "0 2 * * 1 %s %s\n" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
printf "30 2 * * 1 %s %s\n" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
printf "0 3 * * 1 %s %s\n" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
printf "30 3 * * 1 %s %s\n" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"

echo "# Wednesday - Injury reports (every 30 min, 1 PM - 9 PM)" >> "$TEMP_CRON"
for hour in 13 14 15 16 17 18 19 20; do
    printf "0 %d * * 3 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
    printf "30 %d * * 3 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
done

echo "# Thursday - Injury reports (every 30 min, 1 PM - 9 PM)" >> "$TEMP_CRON"
for hour in 13 14 15 16 17 18 19 20; do
    printf "0 %d * * 4 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
    printf "30 %d * * 4 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
done

echo "# Friday - Final status (every 30 min, 1 PM - 7 PM)" >> "$TEMP_CRON"
for hour in 13 14 15 16 17 18; do
    printf "0 %d * * 5 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
    printf "30 %d * * 5 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
done

echo "# Saturday - Final status (every 30 min, 1 PM - 7 PM)" >> "$TEMP_CRON"
for hour in 13 14 15 16 17 18; do
    printf "0 %d * * 6 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
    printf "30 %d * * 6 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
done

echo "# Sunday Morning - Public flood (every 30 min, 6 AM - 12 PM)" >> "$TEMP_CRON"
for hour in 6 7 8 9 10 11; do
    printf "0 %d * * 0 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
    printf "30 %d * * 0 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
done

echo "# Sunday Pre-game - Final adjustments (every 15 min, 12 PM - 2 PM)" >> "$TEMP_CRON"
for hour in 12 13; do
    printf "0 %d * * 0 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
    printf "15 %d * * 0 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
    printf "30 %d * * 0 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
    printf "45 %d * * 0 %s %s\n" "$hour" "$PYTHON_PATH" "$LOGGER_SCRIPT" >> "$TEMP_CRON"
done

# Install the new cron jobs
crontab "$TEMP_CRON"

# Clean up
rm "$TEMP_CRON"

echo "✅ Steady Flow + Peak Bursts cron jobs installed successfully!"
echo ""
echo "📅 Schedule:"
echo "   🔄 STEADY BASELINE (49 calls/week):"
echo "      - Mon-Fri: Every 2 hours, 8 AM - 10 PM (7 calls/day)"
echo "      - Saturday: Every 2 hours, 10 AM - 8 PM (5 calls)"
echo "      - Sunday: Every 2 hours, 8 AM - 8 PM (6 calls)"
echo "   🚀 PEAK BURSTS (66 calls/week):"
echo "      - Sun Night/Mon Morning: Every 30 min, 10 PM - 4 AM (11 calls)"
echo "      - Wednesday: Every 30 min, 1 PM - 9 PM (16 calls)"
echo "      - Thursday: Every 30 min, 1 PM - 9 PM (16 calls)"
echo "      - Friday: Every 30 min, 1 PM - 7 PM (12 calls)"
echo "      - Saturday: Every 30 min, 1 PM - 7 PM (12 calls)"
echo "      - Sunday Morning: Every 30 min, 6 AM - 12 PM (12 calls)"
echo "      - Sunday Pre-game: Every 15 min, 12 PM - 2 PM (8 calls)"
echo "   📊 Total: ~115 calls/week = ~460 calls/month"
echo "   ✅ Near 500 limit with steady flow + peak bursts!"
echo "   - Logs to CSV files in: $SCRIPT_DIR"
echo ""
echo "🔧 To view cron jobs: crontab -l"
echo "🔧 To edit cron jobs: crontab -e"
echo "🔧 To remove all cron jobs: crontab -r"
