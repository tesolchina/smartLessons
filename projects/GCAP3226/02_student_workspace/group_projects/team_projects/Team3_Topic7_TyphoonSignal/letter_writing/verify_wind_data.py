#!/usr/bin/env python3
"""
Verify wind data accuracy by comparing provided data with current HKO API data
"""
import requests
import json
from datetime import datetime

def get_current_hko_data():
    """Fetch current wind data from our live API"""
    try:
        response = requests.get("https://question-no8.hkbu.me/api/wind-data", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API returned status {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return None

def categorize_signal(wind_speed):
    """Determine signal level based on wind speed"""
    if wind_speed >= 63:
        return "SIGNAL 8"
    elif wind_speed >= 41:
        return "SIGNAL 3"
    else:
        return "Normal"

def main():
    print("🔍 Verifying Wind Data Accuracy")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Your provided data (updated)
    provided_data = {
        "Central Pier": {"speed": 38.0, "gust": 65.0, "signal": "Normal"},
        "Chek Lap Kok": {"speed": 58.0, "gust": 81.0, "signal": "SIGNAL 3"},
        "Cheung Chau": {"speed": 95.0, "gust": 123.0, "signal": "SIGNAL 8"},
        "Cheung Chau Beach": {"speed": 56.0, "gust": 86.0, "signal": "SIGNAL 3"},
        "Green Island": {"speed": 52.0, "gust": 92.0, "signal": "SIGNAL 3"},
        "Hong Kong Sea School": {"speed": 19.0, "gust": 69.0, "signal": "Normal"},
        "Kai Tak": {"speed": 39.0, "gust": 74.0, "signal": "Normal"},
        "King's Park": {"speed": 27.0, "gust": 60.0, "signal": "Normal"},
        "Lamma Island": {"speed": 50.0, "gust": 78.0, "signal": "SIGNAL 3"},
        "Lau Fau Shan": {"speed": 34.0, "gust": 58.0, "signal": "Normal"},
        "Ngong Ping": {"speed": 62.0, "gust": 117.0, "signal": "SIGNAL 3"},
        "North Point": {"speed": 12.0, "gust": 45.0, "signal": "Normal"},
        "Peng Chau": {"speed": 43.0, "gust": 69.0, "signal": "SIGNAL 3"},
        "Sai Kung": {"speed": 45.0, "gust": 70.0, "signal": "SIGNAL 3"},
        "Sha Chau": {"speed": 57.0, "gust": 84.0, "signal": "SIGNAL 3"},
        "Sha Tin": {"speed": 26.0, "gust": 63.0, "signal": "Normal"},
        "Shek Kong": {"speed": 19.0, "gust": 51.0, "signal": "Normal"},
        "Stanley": {"speed": 55.0, "gust": 76.0, "signal": "SIGNAL 3"},
        "Star Ferry": {"speed": 44.0, "gust": 69.0, "signal": "SIGNAL 3"},
        "Ta Kwu Ling": {"speed": 24.0, "gust": 59.0, "signal": "Normal"},
        "Tai Mei Tuk": {"speed": 45.0, "gust": 74.0, "signal": "SIGNAL 3"},
        "Tai Po Kau": {"speed": 37.0, "gust": 89.0, "signal": "Normal"},
        "Tap Mun": {"speed": 75.0, "gust": 94.0, "signal": "SIGNAL 8"},
        "Tate's Cairn": {"speed": 45.0, "gust": 95.0, "signal": "SIGNAL 3"},
        "Tseung Kwan O": {"speed": 31.0, "gust": 60.0, "signal": "Normal"},
        "Tsing Yi": {"speed": 15.0, "gust": 42.0, "signal": "Normal"},
        "Tuen Mun": {"speed": 36.0, "gust": 74.0, "signal": "Normal"},
        "Waglan Island": {"speed": 72.0, "gust": 85.0, "signal": "SIGNAL 8"},
        "Wetland Park": {"speed": 14.0, "gust": 34.0, "signal": "Normal"},
        "Wong Chuk Hang": {"speed": 30.0, "gust": 77.0, "signal": "Normal"}
    }
    
    # Fetch current data
    current_data = get_current_hko_data()
    if not current_data:
        print("❌ Could not fetch current data for comparison")
        return
    
    print(f"📊 Comparison Results (Total: {len(provided_data)} stations)")
    print()
    
    matches = 0
    mismatches = 0
    missing = 0
    
    print("Station Name".ljust(20) + "Provided".ljust(15) + "Current".ljust(15) + "Status")
    print("-" * 70)
    
    for station_name, provided in provided_data.items():
        # Find matching station in current data
        current_station = None
        for station in current_data.get('stations', []):
            if station.get('station_name') == station_name:
                current_station = station
                break
        
        if not current_station:
            print(f"{station_name:<20}{'Missing':<15}{'N/A':<15}❌ Not found")
            missing += 1
            continue
        
        current_speed = current_station.get('last_wind_speed', 0)
        current_gust = current_station.get('last_wind_gust', 0)
        current_signal = categorize_signal(current_speed)
        
        provided_speed = provided['speed']
        provided_gust = provided['gust']
        
        # Check if speeds are close (within 10 km/h tolerance for real-time variation)
        speed_close = abs(current_speed - provided_speed) <= 10
        gust_close = abs(current_gust - provided_gust) <= 15
        signal_match = current_signal == provided['signal']
        
        if speed_close and gust_close and signal_match:
            status = "✅ Match"
            matches += 1
        else:
            status = "❌ Differ"
            mismatches += 1
        
        provided_str = f"{provided_speed:.0f}/{provided_gust:.0f}"
        current_str = f"{current_speed:.0f}/{current_gust:.0f}"
        
        print(f"{station_name:<20}{provided_str:<15}{current_str:<15}{status}")
    
    print("-" * 70)
    print(f"📈 Summary:")
    print(f"  ✅ Matches: {matches}")
    print(f"  ❌ Differences: {mismatches}")
    print(f"  ❓ Missing: {missing}")
    print()
    
    if matches > mismatches:
        print("🎯 Overall: Data appears to be ACCURATE (most stations match)")
    else:
        print("⚠️ Overall: Data may be OUTDATED or from different time")
    
    # Check overall signal calculation
    current_overall = current_data.get('overall_signal', 'Unknown')
    print(f"\n🌀 Overall Signal: {current_overall}")
    print(f"📝 Signal Reason: {current_data.get('signal_reason', 'N/A')}")
    
    # Count signal levels from provided data
    signal_counts = {"Normal": 0, "SIGNAL 3": 0, "SIGNAL 8": 0}
    for data in provided_data.values():
        signal_counts[data['signal']] += 1
    
    print(f"\n📊 Your Data Signal Distribution:")
    print(f"  Normal: {signal_counts['Normal']} stations")
    print(f"  SIGNAL 3: {signal_counts['SIGNAL 3']} stations") 
    print(f"  SIGNAL 8: {signal_counts['SIGNAL 8']} stations")
    
    if signal_counts['SIGNAL 3'] + signal_counts['SIGNAL 8'] >= 15:
        expected_signal = "SIGNAL 8" if signal_counts['SIGNAL 8'] >= 15 else "SIGNAL 3"
        print(f"  Expected overall signal: {expected_signal}")
    else:
        print(f"  Expected overall signal: weaker than Signal 3 (only {signal_counts['SIGNAL 3'] + signal_counts['SIGNAL 8']}/30 stations ≥ 41 km/h)")

if __name__ == "__main__":
    main()
