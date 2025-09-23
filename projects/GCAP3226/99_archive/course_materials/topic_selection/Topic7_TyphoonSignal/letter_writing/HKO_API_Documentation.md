# Hong Kong Observatory (HKO) API Documentation

## Overview
This document provides comprehensive information about Hong Kong Observatory's public APIs used for real-time weather monitoring, typhoon warnings, and wind data collection.

---

## 🌀 Typhoon Warning APIs

### 1. Warning Summary API
**URL**: `https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&lang=en`

**Method**: GET  
**Response Format**: JSON

**Description**: Returns current active weather warnings including typhoon signals.

**Example Response**:
```json
{
  "WTS": {
    "name": "Thunderstorm Warning",
    "code": "WTS",
    "actionCode": "EXTEND",
    "issueTime": "2025-09-07T09:53:00+08:00",
    "expireTime": "2025-09-08T05:00:00+08:00",
    "updateTime": "2025-09-07T22:30:00+08:00"
  },
  "WTCSGNL": {
    "name": "Tropical Cyclone Warning Signal",
    "code": "TC8SE",
    "actionCode": "ISSUE",
    "type": "No. 8 Southeast Gale or Storm Signal",
    "issueTime": "2025-09-07T21:20:00+08:00",
    "updateTime": "2025-09-07T21:20:00+08:00"
  }
}
```

**Key Fields**:
- `name`: Warning type name
- `code`: Warning code (e.g., TC8SE for Signal 8 Southeast)
- `actionCode`: Action taken (ISSUE, EXTEND, CANCEL)
- `type`: Detailed warning description
- `issueTime`: When warning was issued (HKT)
- `updateTime`: Last update time (HKT)

---

## 🌬️ Wind Data APIs

### 2. Weather Station Features (WFS)
**URL**: `https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/wfs_weather-station.geojson`

**Method**: GET  
**Response Format**: GeoJSON

**Description**: Returns all weather station locations and their CSV data URLs.

**Example Response**:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "Name": "Central Pier",
        "dataURL": "https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_0.csv"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [114.1558333, 22.2888889]
      }
    }
  ]
}
```

### 3. Individual Station Wind Data
**URL Pattern**: `https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_{station_id}.csv`

**Method**: GET  
**Response Format**: CSV

**Description**: 10-minute wind data for individual weather stations.

**URL Examples**:
- Central Pier: `latest_10min_wind_csdi_0.csv`
- Chek Lap Kok: `latest_10min_wind_csdi_1.csv`
- Cheung Chau: `latest_10min_wind_csdi_2.csv`
- Ngong Ping: `latest_10min_wind_csdi_10.csv`

**CSV Format**:
```csv
Date time (Year),Date time (Month),Date time (Day),Date time (Hour),Date time (Minute),Date time (Second),Date time (Time Zone),Automatic Weather Station,10-Minute Mean Wind Direction(Compass points),10-Minute Mean Speed(km/hour),10-Minute Maximum Gust(km/hour),...
2025,9,8,2,20,,UTC+8,Central Pier,East,27,41,...
```

**Key Columns**:
- Columns 0-6: Date/time components and timezone
- Column 7: Station name
- Column 8: Wind direction (compass points)
- **Column 9: Wind speed (km/h)** ⭐
- **Column 10: Wind gust (km/h)** ⭐

---

## 🌡️ Other Weather Data APIs

### 4. Weather Forecast
**URL**: `https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=en`

**Method**: GET  
**Response Format**: JSON

**Description**: Current weather forecast and conditions.

**Example Response**:
```json
{
  "generalSituation": "",
  "tcInfo": "",
  "fireDangerWarning": "",
  "forecastPeriod": "Weather forecast for today",
  "forecastDesc": "Strong to gale force southeasterly winds, up to storm force on high ground. Cloudy to overcast with squally heavy showers and thunderstorms.",
  "outlook": "Still showery on Tuesday...",
  "updateTime": "2025-09-08T02:45:00+08:00"
}
```

### 5. Temperature Data
**URL**: `https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/latest_1min_temperature.csv`

**Method**: GET  
**Response Format**: CSV

**Description**: Latest 1-minute temperature readings from all stations.

**CSV Format**:
```csv
Date time,Automatic Weather Station,Air Temperature(degree Celsius)
202509080220,Chek Lap Kok,26.4
202509080220,Cheung Chau,24.8
```

---

## 📊 Station Coverage

### Major Weather Stations (30 Total)
| Station Name | Location Type | Typical Wind Exposure |
|--------------|---------------|----------------------|
| Central Pier | Urban/Coastal | High |
| Chek Lap Kok | Airport/Open | Very High |
| Cheung Chau | Island/Coastal | High |
| Cheung Chau Beach | Beach/Open | Very High |
| Green Island | Island/Open | Very High |
| Ngong Ping | Mountain/Exposed | Extreme |
| Waglan Island | Island/Exposed | Extreme |
| King's Park | Urban/Sheltered | Moderate |
| Sha Tin | Urban/Valley | Low-Moderate |
| Wetland Park | Rural/Open | Moderate |

---

## 🔧 API Usage Patterns

### Rate Limiting
- **No official rate limits documented**
- **Recommended**: 1 request per minute per endpoint
- **Our usage**: 10-minute intervals for continuous monitoring

### Data Freshness
- **Wind data**: Updated every 10 minutes
- **Warning data**: Updated as needed (event-driven)
- **Temperature**: Updated every minute

### Reliability
- **Generally stable** but can have brief outages
- **Backup strategy**: Store historical data locally
- **Error handling**: Implement retries with exponential backoff

---

## 📈 Integration Examples

### Python Usage Example
```python
import requests
import json

# Get current typhoon warnings
def get_hko_warnings():
    url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
    params = {"dataType": "warnsum", "lang": "en"}
    
    response = requests.get(url, params=params)
    return response.json()

# Get wind data for specific station
def get_station_wind_data(station_id):
    url = f"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_{station_id}.csv"
    
    response = requests.get(url)
    lines = response.text.strip().split('\n')
    
    # Parse CSV data
    if len(lines) > 1:
        data = lines[1].split(',')
        return {
            'station': data[7],
            'wind_speed': float(data[9]) if data[9] else None,
            'wind_gust': float(data[10]) if data[10] else None,
            'direction': data[8]
        }
    return None
```

### cURL Examples
```bash
# Get current warnings
curl -s "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&lang=en" | jq '.'

# Get wind data for Central Pier (station 0)
curl -s "https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_0.csv"

# Get all weather stations
curl -s "https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/wfs_weather-station.geojson" | jq '.features[].properties.Name'
```

---

## ⚠️ Important Notes

### Data Quality
- **Missing data**: Some stations may report null/empty values
- **Parsing**: CSV format includes multilingual headers (EN/TC/SC)
- **Coordinates**: Use longitude, latitude format (GeoJSON standard)

### Timezone
- **All times in HKT (UTC+8)** unless specified
- **Format**: ISO 8601 (e.g., "2025-09-07T21:20:00+08:00")

### Signal Codes
| Signal Code | Meaning | Wind Speed Range |
|-------------|---------|------------------|
| TC1 | No. 1 Standby | <41 km/h |
| TC3 | No. 3 Strong Wind | 41-62 km/h |
| TC8NE | No. 8 Northeast Gale | 63-117 km/h |
| TC8SE | No. 8 Southeast Gale | 63-117 km/h |
| TC8SW | No. 8 Southwest Gale | 63-117 km/h |
| TC8NW | No. 8 Northwest Gale | 63-117 km/h |
| TC9 | No. 9 Increasing Gale | 88-117 km/h |
| TC10 | No. 10 Hurricane | >117 km/h |

---

## 🔗 Related Resources

- **HKO Open Data**: https://www.hko.gov.hk/en/abouthko/opendata_intro.htm
- **Weather Station Map**: https://www.hko.gov.hk/en/wxinfo/aws/aws.shtml
- **Typhoon Warnings**: https://www.hko.gov.hk/en/wservice/warning/tcwarn.htm

---

*Last Updated: September 8, 2025*  
*For questions: simonwang@hkbu.edu.hk*
