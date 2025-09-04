# 🚀 Railway Deployment Guide

Deploy your NFL Odds Logger to Railway for 24/7 operation that bypasses school WiFi restrictions.

## 📋 Prerequisites

1. **GitHub Account** (free)
2. **Railway Account** (free)
3. **Your code** (already ready!)

## 🚀 Step-by-Step Deployment

### 1. Push to GitHub

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit - NFL Odds Logger"

# Create GitHub repository (go to github.com and create new repo)
# Then push your code
git remote add origin https://github.com/YOUR_USERNAME/nfl-odds-logger.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Railway

1. **Go to [railway.app](https://railway.app)**
2. **Sign up with GitHub**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your `nfl-odds-logger` repository**
6. **Railway will automatically detect Python and deploy!**

### 3. Configure Environment

Railway will automatically:
- ✅ Install Python dependencies
- ✅ Run `python3 app.py`
- ✅ Start both scheduler and web interface
- ✅ Give you a public URL

### 4. Access Your Dashboard

Once deployed, Railway will give you a URL like:
`https://nfl-odds-logger-production.up.railway.app`

## 📊 What You Get

### **Web Dashboard**
- 📈 Real-time odds data
- 📊 API usage tracking
- 📥 Download CSV files
- 📱 Mobile-friendly interface

### **24/7 Operation**
- ⏰ Runs your 115 calls/week schedule
- 🌐 Bypasses school WiFi restrictions
- 💾 Stores data in Railway's file system
- 🔄 Automatic restarts if it crashes

### **Usage Tracking**
- 📊 Shows API calls this month
- ⚠️ Warns when approaching 500 limit
- 📈 Usage percentage display

## 💰 Cost Breakdown

**Railway Free Tier:**
- 500 hours/month
- Your usage: ~15-20 minutes/month
- **Remaining: 480+ hours**
- **Cost: $0/month**

## 🔧 Monitoring

### **Check Status**
- Visit your Railway dashboard
- View logs in real-time
- Monitor resource usage

### **View Data**
- Access web dashboard anytime
- Download CSV files
- Check API usage stats

## 🛠️ Troubleshooting

### **If Deployment Fails**
1. Check Railway logs
2. Ensure all files are committed to GitHub
3. Verify `requirements.txt` is correct

### **If Scheduler Stops**
1. Railway will auto-restart
2. Check logs for errors
3. Verify API key is correct

### **If Web Interface Doesn't Load**
1. Check Railway logs
2. Ensure port 5000 is exposed
3. Wait a few minutes for deployment

## 🎯 Benefits

✅ **24/7 Operation** - No laptop required
✅ **Bypasses School WiFi** - Cloud server has full access
✅ **Web Dashboard** - View data from anywhere
✅ **Automatic Backups** - Data stored in cloud
✅ **Free Tier** - No cost for your usage level
✅ **Easy Updates** - Just push to GitHub

## 📱 Access from Anywhere

Once deployed, you can:
- View odds data on your phone
- Download CSV files
- Monitor API usage
- Check if the service is running

Perfect for students with restricted WiFi! 🎓
