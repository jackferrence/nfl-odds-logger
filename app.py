#!/usr/bin/env python3
"""
NFL Odds Logger - Combined App
Runs both the scheduler and web interface
"""

import threading
import time
import subprocess
import sys
import os
from datetime import datetime

def run_scheduler():
    """Run the odds logger scheduler in background"""
    print("🔄 Starting odds logger scheduler...")
    try:
        # Import and run the scheduler
        from schedule_odds import main as scheduler_main
        scheduler_main()
    except Exception as e:
        print(f"❌ Scheduler error: {e}")

def run_web_interface():
    """Run the web interface"""
    print("🌐 Starting web interface...")
    try:
        from web_interface import app
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"❌ Web interface error: {e}")

def main():
    print("🏈 NFL Odds Logger - Railway Deployment")
    print("=" * 50)
    print("🚀 Starting both scheduler and web interface...")
    port = os.environ.get('PORT', 5000)
    print(f"📊 Web dashboard: http://localhost:{port}")
    print("⏰ Scheduler: Running in background")
    print("=" * 50)
    
    # Change to linemovement directory where the code is
    os.chdir('linemovement')
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Start scheduler in background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Give scheduler a moment to start
    time.sleep(2)
    
    # Start web interface (this will block)
    run_web_interface()

if __name__ == "__main__":
    main()
