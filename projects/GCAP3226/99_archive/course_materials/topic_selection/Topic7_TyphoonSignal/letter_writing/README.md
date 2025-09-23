# Hong Kong Real-Time Wind Monitor 🌪️

A real-time dashboard for monitoring typhoon conditions across Hong Kong, providing Signal 3 and Signal 8 assessments based on official Hong Kong Observatory criteria.

## 🎯 Features

- **Real-time Wind Monitoring**: 30 weather stations updated every 10 minutes
- **Official HKO Criteria**: Signal 3 (41-62 km/h) and Signal 8 (63-117 km/h) assessment
- **Live Dashboard**: Color-coded table showing all station readings
- **Public Information**: Comprehensive data sources and methodology explanation
- **Mobile Responsive**: Works on all devices
- **Cloud Deployment**: Ready for Railway.app deployment

## 📊 Signal Criteria

Based on Hong Kong Observatory's official criteria:

- **Signal No. 3 (Strong Wind)**: When **half or more stations** record sustained winds of **41-62 km/h**
- **Signal No. 8 (Gale/Storm)**: When **half or more stations** record sustained winds of **63-117 km/h**

## 🌐 Data Sources

- **Primary**: Hong Kong Observatory Web Feature Service (WFS)
- **Endpoint**: `portal.csdi.gov.hk/geoportal/csdi-climatedata-ws/`
- **Update Frequency**: Every 10 minutes
- **Coverage**: 30 weather stations across Hong Kong Territory

## 🚀 Railway Deployment

### One-Click Deploy
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/deploy)

### Manual Deployment

1. **Clone/Download** this repository
2. **Connect to Railway**: 
   ```bash
   railway login
   railway init
   ```
3. **Deploy**:
   ```bash
   railway up
   ```

The app will automatically:
- Install Python dependencies from `requirements.txt`
- Start the Gunicorn web server
- Begin real-time wind data monitoring
- Serve the dashboard at your Railway URL

### Environment Variables
No environment variables required - the app uses default settings suitable for Railway deployment.

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- pip package manager

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit `http://localhost:5000` to see the dashboard.

### Project Structure
```
├── app.py                 # Main Flask application
├── templates/
│   ├── dashboard.html     # Real-time wind dashboard
│   └── about.html         # Public information page
├── requirements.txt       # Python dependencies
├── Procfile              # Railway deployment config
├── package.json          # Project metadata
└── README.md             # This file
```

## 📱 API Endpoints

### GET `/`
Main dashboard with real-time wind monitoring table

### GET `/api/wind-data`
JSON API returning current wind data:
```json
{
  "stations": [...],
  "overall_signal": 3,
  "signal_reason": "15/30 stations ≥ 41 km/h",
  "total_stations": 30,
  "signal8_stations": 2,
  "signal3_stations": 15,
  "last_update": "2025-01-08T12:30:00Z",
  "criteria": {
    "signal_3_range": "41-62 km/h",
    "signal_8_range": "63-117 km/h", 
    "threshold_rule": "Half or more stations must meet sustained wind criteria"
  }
}
```

### GET `/about`
Public information page explaining data sources and methodology

## ⚠️ Important Disclaimers

- **For informational purposes only**
- **Not official HKO warnings** - always refer to official sources
- Emergency: **999**
- HKO Hotline: **1878 200**
- Official site: **www.hko.gov.hk**

### Data integrity notice
- Historical logs prior to 2025-09-08 09:55 HKT were affected by a parsing artifact (uniform 9.0 km/h values).
- The collector was fixed and verified at 2025-09-08 09:55 HKT. From that time onward, collected data are considered correct.
- Treat earlier rows as unreliable for analysis; use post-fix data for comparisons.

## 🔧 Technical Details

- **Backend**: Python Flask with background monitoring threads
- **Frontend**: Vanilla HTML5/CSS3/JavaScript with auto-refresh
- **Data Processing**: Real-time parsing of HKO WFS GeoJSON and CSV data
- **Deployment**: Gunicorn WSGI server optimized for Railway
- **Update Cycle**: 10-minute intervals synchronized with HKO data

## 📋 Features Overview

### Dashboard View
- 🌪️ **Signal Status Indicator**: Large, color-coded current signal level
- 📊 **Statistics Cards**: Total stations, Signal 3+ count, Signal 8+ count
- 📋 **Detailed Table**: All 30 stations with wind speeds, locations, signal levels
- 🕒 **Real-time Updates**: Auto-refresh every 10 minutes
- 📱 **Mobile Responsive**: Optimized for all screen sizes

### Public Information
- 📖 **Methodology Explanation**: How signal levels are calculated
- 🗂️ **Data Sources**: Detailed information about HKO data feeds
- ⚙️ **Technical Specs**: Update frequency, coordinate systems, etc.
- ⚠️ **Safety Information**: Emergency contacts and official warning sources

## 🌏 Geographic Coverage

Weather stations include:
- **Urban**: Central Pier, Kai Tak, King's Park, North Point
- **Airport**: Chek Lap Kok (HKIA)
- **Islands**: Cheung Chau, Lamma Island, Waglan Island
- **Rural**: Tai Po, Sha Tin, Sai Kung, Tuen Mun
- **Elevated**: Tate's Cairn, Ngong Ping

## 🔄 Monitoring Process

1. **Initialization**: Fetch all weather station locations from HKO WFS
2. **Data Collection**: Every 10 minutes, query each station's wind measurements
3. **Signal Assessment**: Apply HKO criteria (half or more stations threshold)
4. **Dashboard Update**: Refresh all displays with latest data
5. **Continuous Loop**: Repeat every 10 minutes

## 📈 Use Cases

- **Public Awareness**: Real-time typhoon condition monitoring
- **Media**: Data visualization for weather reporting  
- **Emergency Planning**: Understanding current wind distribution
- **Educational**: Demonstrating meteorological data processing
- **Research**: Historical pattern analysis (with data logging)

## 🤝 Contributing

This is a public service project. For meteorological data accuracy or official warnings, please contact Hong Kong Observatory directly.

## 📄 License

MIT License - Feel free to fork, modify, and deploy for public benefit.

---

**🌪️ Stay Safe! For official typhoon warnings, always refer to Hong Kong Observatory (www.hko.gov.hk)**
