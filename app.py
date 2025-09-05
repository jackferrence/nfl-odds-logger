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

# Add virtual environment to Python path
venv_path = '/opt/venv'
if os.path.exists(venv_path):
    sys.path.insert(0, f'{venv_path}/lib/python3.11/site-packages')
    print(f"🐍 Added virtual environment to Python path: {venv_path}")

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
    
    # Debug virtual environment
    venv_path = '/opt/venv'
    if os.path.exists(venv_path):
        print(f"✅ Virtual environment found at: {venv_path}")
        site_packages = f'{venv_path}/lib/python3.11/site-packages'
        if os.path.exists(site_packages):
            print(f"✅ Site packages found at: {site_packages}")
            # List installed packages
            try:
                import pkg_resources
                installed_packages = [d.project_name for d in pkg_resources.working_set]
                print(f"📦 Installed packages: {installed_packages[:10]}...")  # Show first 10
            except:
                print("⚠️ Could not list installed packages")
        else:
            print(f"❌ Site packages not found at: {site_packages}")
    else:
        print(f"❌ Virtual environment not found at: {venv_path}")
    
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
