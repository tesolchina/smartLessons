#!/usr/bin/env python3

import csv
import requests
from datetime import datetime

def test_hko_parsing():
    """Test current HKO CSV parsing"""
    print("=== Testing Current HKO CSV Parsing ===")
    
    # Test a few stations
    test_stations = [
        ("Central Pier", "https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_0.csv"),
        ("Cheung Chau", "https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_2.csv"),
        ("Waglan Island", "https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_27.csv")
    ]
    
    for station_name, url in test_stations:
        try:
            response = requests.get(url, timeout=10)
            csv_text = response.text
            
            lines = csv_text.strip().split('\n')
            if len(lines) >= 2:
                data_line = lines[-1]
                values = [v.strip() for v in data_line.split(',')]
                
                print(f"\n{station_name}:")
                print(f"  Raw data: {values[:15]}")
                
                # Extract using our logic
                try:
                    speed = float(values[9]) if len(values) > 9 and values[9] else None
                    gust = float(values[10]) if len(values) > 10 and values[10] else None
                    print(f"  Parsed: Speed={speed} km/h, Gust={gust} km/h")
                except (ValueError, IndexError) as e:
                    print(f"  Parse error: {e}")
        except Exception as e:
            print(f"Error fetching {station_name}: {e}")

def analyze_attached_data():
    """Analyze the attached CSV data for signal calculations"""
    print("\n\n=== Analyzing Attached Data ===")
    
    # Read the attached data
    data_file = "/Users/simonwang/Documents/Usage/VibeCoding/letter_writing/data_archive/hko_wind_data_20250907_224309.csv"
    
    timestamps = set()
    signal_analysis = {}
    
    try:
        with open(data_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                timestamp = row['timestamp']
                station_name = row['station_name']
                wind_speed = float(row['wind_speed_kmh'])
                wind_gust = float(row['wind_gust_kmh'])
                
                timestamps.add(timestamp)
                
                if timestamp not in signal_analysis:
                    signal_analysis[timestamp] = {
                        'stations': 0,
                        'signal3_stations': 0,
                        'signal8_stations': 0,
                        'station_data': []
                    }
                
                # Apply our signal calculation rules
                signal_level = 1  # Default
                if wind_speed >= 88:  # Signal 8 threshold
                    signal_level = 8
                    signal_analysis[timestamp]['signal8_stations'] += 1
                elif wind_speed >= 41:  # Signal 3 threshold  
                    signal_level = 3
                    signal_analysis[timestamp]['signal3_stations'] += 1
                
                signal_analysis[timestamp]['stations'] += 1
                signal_analysis[timestamp]['station_data'].append({
                    'station': station_name,
                    'speed': wind_speed,
                    'gust': wind_gust,
                    'signal': signal_level
                })
        
        print(f"Found {len(timestamps)} unique timestamps")
        print(f"Analyzing first few timestamps...")
        
        # Analyze first 3 timestamps
        sorted_timestamps = sorted(timestamps)[:3]
        
        for timestamp in sorted_timestamps:
            data = signal_analysis[timestamp]
            total_stations = data['stations']
            signal3_count = data['signal3_stations'] 
            signal8_count = data['signal8_stations']
            half_stations = total_stations / 2
            
            calculated_signal = 1
            if signal8_count >= half_stations:
                calculated_signal = 8
            elif signal3_count >= half_stations:
                calculated_signal = 3
            
            print(f"\nTimestamp: {timestamp}")
            print(f"  Total stations: {total_stations}")
            print(f"  Signal 3+ stations: {signal3_count} (need {half_stations:.1f} for Signal 3)")
            print(f"  Signal 8+ stations: {signal8_count} (need {half_stations:.1f} for Signal 8)")
            print(f"  Calculated signal: {calculated_signal}")
            
            # Show some high-wind stations
            high_wind_stations = [s for s in data['station_data'] if s['speed'] >= 41][:5]
            if high_wind_stations:
                print(f"  High wind stations (≥41 km/h):")
                for station in high_wind_stations:
                    print(f"    {station['station']}: {station['speed']} km/h (Signal {station['signal']})")
    
    except Exception as e:
        print(f"Error analyzing attached data: {e}")

if __name__ == "__main__":
    test_hko_parsing()
    analyze_attached_data()
