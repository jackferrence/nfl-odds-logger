# 🚀 Railway Deployment Checklist

## ✅ **Critical Setup Steps**

### 1. **Environment Variables**
Make sure these are set in Railway:
- `ODDS_API_KEY` = Your Odds API key

### 2. **Procfile Configuration**
Current Procfile should be:
```
web: python app.py
```

This runs both the scheduler AND web interface.

### 3. **Files Structure**
Ensure these files exist:
- `app.py` - Main entry point (scheduler + web)
- `schedule_odds.py` - Scheduler logic
- `nfl_odds_logger.py` - API calls and CSV creation
- `web_interface.py` - Web dashboard
- `requirements.txt` - Dependencies

## 🧪 **Testing Steps**

### **Step 1: Test API Manually**
```bash
# Run this to test API and CSV creation
python test_api.py
```

### **Step 2: Check Railway Logs**
1. Go to Railway dashboard
2. Click on your project
3. Go to "Deployments" tab
4. Click on latest deployment
5. Check logs for:
   - ✅ "Starting both scheduler and web interface"
   - ✅ "API Key found"
   - ✅ "Steady Flow + Peak Bursts Schedule set up"
   - ✅ "Running NFL odds logger..."

### **Step 3: Verify CSV Creation**
1. Check Railway logs for "Data saved to nfl_odds_YYYY-MM-DD.csv"
2. The CSV file should be created in the Railway environment

## 📊 **Schedule Overview**

The scheduler runs:
- **Steady Baseline**: Every 2 hours during business hours
- **Peak Bursts**: Every 30 minutes during critical times
- **Total**: ~115 calls/week = ~460 calls/month

## 🔍 **Troubleshooting**

### **If API isn't working:**
1. Check `ODDS_API_KEY` environment variable
2. Run `python test_api.py` to test manually
3. Check Railway logs for errors

### **If scheduler isn't running:**
1. Verify Procfile is `web: python app.py`
2. Check Railway logs for scheduler startup
3. Look for "Starting odds logger scheduler" message

### **If CSV files aren't being created:**
1. Check API response in logs
2. Verify file permissions in Railway
3. Look for "Data saved to" messages

## 📈 **Monitoring**

### **Check API Usage:**
```bash
python api_usage_tracker.py
```

### **View CSV Files:**
- Go to web dashboard
- Click "Data Files" tab
- Download files to verify data

## 🎯 **Success Indicators**

✅ **API Working**: Logs show "Fetched data for X games"  
✅ **CSV Created**: Logs show "Data saved to nfl_odds_YYYY-MM-DD.csv"  
✅ **Scheduler Running**: Logs show "Starting odds logger scheduler"  
✅ **Web Interface**: Dashboard accessible at Railway URL  
✅ **Data Collection**: CSV files accumulating over time  

## 🚨 **Emergency Contacts**

If something breaks:
1. Check Railway logs first
2. Run `python test_api.py` to isolate issues
3. Verify environment variables
4. Check API key validity
