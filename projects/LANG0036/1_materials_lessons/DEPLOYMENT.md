# Hong Kong Wind Monitor - Railway Deployment Guide

## Quick Deploy to Railway

### Option 1: One-Click Deploy
1. Click the Railway deploy button in README.md
2. Connect your GitHub account
3. The app will automatically deploy and start monitoring

### Option 2: Manual Deployment

#### Step 1: Prepare Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Create new project
railway init
```

#### Step 2: Configure Environment
```bash
# Set Python runtime (optional - defaults to 3.11)
railway variables set PYTHON_VERSION=3.11

# The app runs on the PORT provided by Railway automatically
```

#### Step 3: Deploy
```bash
# Deploy current directory
railway up

# Get your deployment URL
railway status
```

## File Structure for Railway

```
├── app.py                 # Main Flask application (entry point)
├── Procfile              # Tells Railway to use Gunicorn
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── dashboard.html    # Main dashboard
│   └── about.html        # Information page
└── README.md            # Documentation
```

## Railway Configuration Files

### Procfile
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 30
```

### requirements.txt
```
flask==3.0.0
requests==2.31.0
pandas>=1.3.0
gunicorn==21.2.0
```

## Automatic Features

Railway will automatically:
- ✅ Detect Python runtime
- ✅ Install dependencies from requirements.txt
- ✅ Run the Procfile web command
- ✅ Provide HTTPS SSL certificate
- ✅ Auto-scale based on traffic
- ✅ Provide deployment URL

## Monitoring & Scaling

### Railway Dashboard
- **Logs**: View real-time application logs
- **Metrics**: Monitor CPU, memory, requests
- **Deployments**: Rollback if needed
- **Variables**: Manage environment settings

### Performance Settings
```yaml
# railway.json (optional)
{
  "deploy": {
    "healthcheckPath": "/",
    "healthcheckTimeout": 10,
    "restartPolicyType": "always"
  }
}
```

## Production Considerations

### Resource Usage
- **Memory**: ~100MB base + monitoring threads
- **CPU**: Low usage, spikes every 10 minutes during data fetching
- **Network**: 30 HTTP requests every 10 minutes to HKO servers
- **Storage**: Minimal (no persistent data storage)

### Scaling
- **Single Instance**: Sufficient for public use
- **Multiple Workers**: Already configured (2 Gunicorn workers)
- **Traffic Handling**: Can serve thousands of concurrent users

## Troubleshooting

### Common Issues

**1. Build Fails**
```bash
# Check Python version compatibility
railway logs --deployment

# Verify requirements.txt format
pip install -r requirements.txt
```

**2. App Won't Start**
```bash
# Check Procfile syntax
railway logs

# Test locally first
python app.py
```

**3. Data Not Loading**
```bash
# Check HKO API connectivity
railway logs | grep "Error"

# Verify WFS endpoint accessibility
curl "https://portal.csdi.gov.hk/geoportal/csdi-climatedata-ws/api/v1/query/dataset/ds_latest_10min_wind?f=GeoJSON"
```

### Environment Variables (Optional)
```bash
# Custom update interval (default: 600 seconds)
railway variables set UPDATE_INTERVAL=600

# Debug mode (default: False)
railway variables set FLASK_DEBUG=false
```

## Custom Domain Setup

### Using Railway Custom Domains
1. Go to Railway project dashboard
2. Navigate to Settings > Domains
3. Add your custom domain
4. Update DNS records as instructed
5. SSL certificate will be automatically provisioned

Example DNS records:
```
CNAME: hk-wind-monitor.yourdomain.com → your-app.railway.app
```

## Backup & Recovery

### Database
No database required - all data is fetched in real-time

### Code Backup
- Source code should be in Git repository
- Railway automatically keeps deployment history
- Easy rollback through Railway dashboard

## Monitoring Production

### Health Checks
The app includes built-in health monitoring:
- **Endpoint**: `/` returns HTTP 200 when healthy
- **API Status**: `/api/wind-data` shows data freshness
- **Error Logging**: Comprehensive console output

### Alerts Setup
Configure Railway project notifications for:
- Deployment failures
- High error rates
- Resource usage spikes
- Downtime incidents

## Cost Optimization

### Railway Pricing
- **Hobby Plan**: Free tier available
- **Pro Plan**: Pay per usage
- **Resource Limits**: Monitor memory and CPU usage

### Optimization Tips
```python
# In app.py - already implemented
- Efficient HTTP requests with timeouts
- Background threads instead of cron jobs
- Minimal memory footprint
- Graceful error handling
```

## Go Live Checklist

- [ ] Deploy successfully to Railway
- [ ] Test dashboard loads correctly
- [ ] Verify real-time data updates every 10 minutes  
- [ ] Check `/about` page displays properly
- [ ] Test API endpoint `/api/wind-data` returns valid JSON
- [ ] Confirm mobile responsiveness
- [ ] Set up monitoring/alerts
- [ ] Share URL with intended users

## Support

For Railway-specific issues:
- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Railway Support**: help@railway.app

For app functionality:
- Check console logs via `railway logs`
- Test API endpoints directly
- Verify HKO data source availability

---

**🚀 Your Hong Kong Wind Monitor will be live at: `https://your-app.railway.app`**

## Data Integrity Notice (Production)

- A parsing defect produced uniform 9.0 km/h speeds in earlier builds. The collector was corrected on 2025-09-08 09:55 HKT.
- From that time onward, CSV logs are reliable. Treat data collected before that timestamp as incorrect in downstream analysis and UIs.
