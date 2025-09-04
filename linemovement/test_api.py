#!/usr/bin/env python3
"""
Test script to verify API is working and creating CSV files
"""

import os
import sys
import subprocess
from datetime import datetime

def test_api():
    """Test the API and CSV creation"""
    print("🧪 Testing NFL Odds Logger API...")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.environ.get('ODDS_API_KEY')
    if not api_key:
        print("❌ ERROR: ODDS_API_KEY environment variable not set!")
        print("Please set your API key in Railway environment variables")
        return False
    
    print(f"✅ API Key found: {api_key[:8]}...")
    
    # Run the odds logger
    print("🔄 Running odds logger...")
    try:
        result = subprocess.run([sys.executable, "nfl_odds_logger.py"], 
                               capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        print("📋 STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("📋 STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Odds logger completed successfully!")
        else:
            print(f"❌ Odds logger failed with return code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running odds logger: {e}")
        return False
    
    # Check for CSV file creation
    print("\n📁 Checking for CSV files...")
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    if csv_files:
        print(f"✅ Found {len(csv_files)} CSV file(s):")
        for csv_file in csv_files:
            file_size = os.path.getsize(csv_file)
            file_time = datetime.fromtimestamp(os.path.getctime(csv_file))
            print(f"   📄 {csv_file} ({file_size:,} bytes, created {file_time.strftime('%Y-%m-%d %H:%M:%S')})")
    else:
        print("❌ No CSV files found!")
        return False
    
    # Check API usage
    print("\n📊 Checking API usage...")
    try:
        result = subprocess.run([sys.executable, "api_usage_tracker.py"], 
                               capture_output=True, text=True, cwd=os.path.dirname(__file__))
        print(result.stdout)
    except Exception as e:
        print(f"⚠️ Could not check API usage: {e}")
    
    print("\n🎉 Test completed!")
    return True

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
