#!/usr/bin/env python3
"""
NFL Odds Logger - Web Interface Only
Serves the web dashboard without running the background scheduler
"""

import os
import sys
import subprocess

def main():
    print("🏈 NFL Odds Logger - Web Interface Only")
    print("=" * 50)
    print("🌐 Starting web interface...")
    print("📊 Dashboard will read from existing CSV files")
    print("⏰ No background API calls - just viewing stored data")
    print("=" * 50)
    
    # Install dependencies
    print("📦 Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Start web interface
    try:
        from web_interface import app
        # Use Railway's PORT environment variable, default to 5000 for local development
        port = int(os.environ.get('PORT', 5000))
        print(f"📊 Dashboard will be available at: http://localhost:{port}")
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"❌ Web interface error: {e}")

if __name__ == "__main__":
    main()
