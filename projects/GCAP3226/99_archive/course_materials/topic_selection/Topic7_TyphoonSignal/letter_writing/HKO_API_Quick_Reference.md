# HKO API Quick Reference

## 🚨 Essential APIs for Typhoon Monitoring

### Current Warnings
```bash
curl "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&lang=en"
```

### Weather Stations List
```bash
curl "https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/wfs_weather-station.geojson"
```

### Wind Data (Replace {ID} with 0-29)
```bash
curl "https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_{ID}.csv"
```

## 🎯 Key Station IDs
- 0: Central Pier
- 1: Chek Lap Kok
- 2: Cheung Chau  
- 3: Cheung Chau Beach
- 10: Ngong Ping (mountain, highest winds)
- 28: Waglan Island (exposed)

## 📊 Data Parsing
**CSV Columns (Wind Data)**:
- 9: Wind Speed (km/h)
- 10: Wind Gust (km/h)
- 8: Direction
- 7: Station Name

## 🌀 Signal Levels
- TC1: <41 km/h
- TC3: 41-62 km/h  
- TC8: 63-117 km/h
- TC10: >117 km/h
