#!/usr/bin/env python3
"""
Hong Kong Real-Time Wind Monitoring Dashboard
==============================================
Web application for monitoring typhoon Signal 3 and Signal 8 conditions
Based on Hong Kong Observatory criteria and real-time 10-minute wind data

Credits: 
- Dr Simon Wang, Lecturer and Innovation Officer, the Language Centre, HKBU
- With help from GitHub Copilot agent
- Email: simonwang@hkbu.edu.hk

Data Source: Hong Kong Observatory WFS Service
Deployment: Railway.app

Research Note: We raise concern over an earlier than usual announcement 
of the decision to keep Signal 8 until 11 AM on 9 September 2025.
"""

import os
import json
import threading
import time
import requests
import csv
from datetime import datetime, timezone, timedelta
from flask import Flask, render_template, jsonify, send_file
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

app = Flask(__name__)

class HKWindMonitor:
    """Real-time Hong Kong wind monitoring system"""
    
    def __init__(self):
        # Use the correct WFS endpoint from HKO
        self.wfs_url = "https://portal.csdi.gov.hk/server/services/common/hko_rcd_1634953844424_88011/MapServer/WFSServer?service=wfs&request=GetFeature&typenames=latest_10min_wind&outputFormat=geojson"

        # HKO official warning API
        self.hko_warning_url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&lang=en"

        # Runtime state
        self.stations = []
        self.wind_data = {}
        self.last_update = None
        self.is_running = True
        # The collector service now writes to data_archive/hk_wind_log_YYYYMMDD.csv
        # The web service will read from this file.
        self.log_dir = "data_archive"
        self.csv_filename_pattern = os.path.join(self.log_dir, "hk_wind_log_{}.csv")
        # Legacy attribute to satisfy older helper methods; web app no longer writes CSV directly
        self.csv_filename = os.path.join(self.log_dir, "hk_wind_log_unused.csv")
        # Ensure data directory exists in all environments
        try:
            os.makedirs(self.log_dir, exist_ok=True)
        except Exception:
            pass
        self._thread_started = False
        self._thread_lock = threading.Lock()
        self.history = []  # store per-update match/mismatch records within window

        # This is no longer needed as the web service reads, not writes.
        # self.init_csv_file()

        # Demo stations for fallback
        self.demo_stations = [
            {"name": "Central Pier", "lat": 22.2889, "lon": 114.1558},
            {"name": "Chek Lap Kok", "lat": 22.3094, "lon": 113.9219},
            {"name": "Cheung Chau", "lat": 22.2011, "lon": 114.0267},
            {"name": "Green Island", "lat": 22.2850, "lon": 114.1128},
            {"name": "Kai Tak", "lat": 22.3097, "lon": 114.2133},
            {"name": "King's Park", "lat": 22.3119, "lon": 114.1728},
            {"name": "Lamma Island", "lat": 22.2261, "lon": 114.1086},
            {"name": "North Point", "lat": 22.2944, "lon": 114.1997},
            {"name": "Sai Kung", "lat": 22.3756, "lon": 114.2744},
            {"name": "Stanley", "lat": 22.2142, "lon": 114.2186},
            {"name": "Star Ferry", "lat": 22.2930, "lon": 114.1684},
            {"name": "Tsing Yi", "lat": 22.3442, "lon": 114.1100},
            {"name": "Tuen Mun", "lat": 22.3858, "lon": 113.9642},
            {"name": "Waglan Island", "lat": 22.1822, "lon": 114.3033},
            {"name": "Wong Chuk Hang", "lat": 22.2478, "lon": 114.1736},
            {"name": "Sha Tin", "lat": 22.4025, "lon": 114.2100},
            {"name": "Tai Po", "lat": 22.4425, "lon": 114.1842},
            {"name": "Tate's Cairn", "lat": 22.3578, "lon": 114.2178},
            {"name": "Ngong Ping", "lat": 22.2586, "lon": 113.9128},
            {"name": "Wetland Park", "lat": 22.4667, "lon": 114.0089},
            {"name": "Peng Chau", "lat": 22.2911, "lon": 114.0433},
            {"name": "Lau Fau Shan", "lat": 22.4689, "lon": 113.9836},
            {"name": "Ta Kwu Ling", "lat": 22.5286, "lon": 114.1567},
            {"name": "Tai Mei Tuk", "lat": 22.4753, "lon": 114.2375},
            {"name": "Tseung Kwan O", "lat": 22.3158, "lon": 114.2556},
            {"name": "Shek Kong", "lat": 22.4361, "lon": 114.0847},
            {"name": "Sha Chau", "lat": 22.3458, "lon": 113.8911},
            {"name": "Tap Mun", "lat": 22.4714, "lon": 114.3606},
            {"name": "Hong Kong Sea School", "lat": 22.2183, "lon": 114.2143},
            {"name": "Cheung Chau Beach", "lat": 22.2108, "lon": 114.0292}
        ]

        # Signal criteria based on HKO standards
        self.SIGNAL_3_MIN = 41  # km/h
        self.SIGNAL_3_MAX = 62  # km/h
        self.SIGNAL_8_MIN = 63  # km/h
        self.SIGNAL_8_MAX = 117 # km/h
        
    def init_csv_file(self):
        """Initialize CSV file for raw data logging"""
        try:
            with open(self.csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'timestamp',
                    'station_name', 
                    'latitude',
                    'longitude', 
                    'wind_speed_kmh',
                    'wind_gust_kmh',
                    'signal_level',
                    'overall_signal_calculated',
                    'official_signal_hko',
                    'data_url'
                ])
            print(f"✅ CSV file initialized: {self.csv_filename}")
        except Exception as e:
            print(f"❌ Error initializing CSV: {e}")
    
    def log_to_csv(self, station_data, overall_signal, official_signal):
        """Log station data to CSV file"""
        try:
            with open(self.csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                timestamp = datetime.now().isoformat()
                
                for station in station_data:
                    writer.writerow([
                        timestamp,
                        station.get('station_name', ''),
                        station.get('latitude', ''),
                        station.get('longitude', ''), 
                        station.get('last_wind_speed', ''),
                        station.get('last_wind_gust', ''),
                        station.get('signal_level', ''),
                        overall_signal,
                        official_signal,
                        station.get('csv_url', '')
                    ])
        except Exception as e:
            print(f"❌ Error logging to CSV: {e}")
        
    def fetch_station_locations(self) -> List[Dict]:
        """Fetch weather station locations from HKO WFS endpoint"""
        try:
            print(f"🔍 Fetching weather stations from HKO WFS...")
            response = requests.get(self.wfs_url, timeout=30)
            response.raise_for_status()
            
            geojson = response.json()
            stations = []
            
            for feature in geojson.get('features', []):
                props = feature.get('properties', {})
                coords = feature.get('geometry', {}).get('coordinates', [])
                
                if len(coords) >= 2:
                    station = {
                        'station_name': props.get('AutomaticWeatherStation_en', 'Unknown'),
                        'longitude': coords[0],
                        'latitude': coords[1],
                        'csv_url': props.get('Data_url', ''),
                        'last_wind_speed': None,
                        'last_wind_gust': None,
                        'status': 'no_data'
                    }
                    stations.append(station)
            
            print(f"✅ Found {len(stations)} weather stations from HKO WFS")
            return stations
            
        except Exception as e:
            print(f"❌ Error fetching HKO WFS data: {e}")
            print("📋 Using fallback demo stations...")
            return self.init_demo_stations()
    
    def init_demo_stations(self) -> List[Dict]:
        """Initialize demo weather station locations as fallback"""
        stations = []
        
        for demo_station in self.demo_stations:
            station = {
                'station_name': demo_station['name'],
                'longitude': demo_station['lon'],
                'latitude': demo_station['lat'],
                'csv_url': '',
                'last_wind_speed': None,
                'last_wind_gust': None,
                'status': 'no_data'
            }
            stations.append(station)
        
        print(f"✅ Initialized {len(stations)} demo weather stations")
        return stations
    
    def fetch_official_hko_signal(self) -> Dict:
        """Fetch current official typhoon signal from HKO API"""
        try:
            response = requests.get(self.hko_warning_url, timeout=15)
            response.raise_for_status()
            
            warnings = response.json()
            
            # Look for typhoon/tropical cyclone warnings
            current_signal = 1  # Default: No signal
            signal_info = "No tropical cyclone warning"
            signal_code = ""
            issue_time = ""
            
            # Check for WTCSGNL (Tropical Cyclone Warning Signal)
            if 'WTCSGNL' in warnings:
                tc_warning = warnings['WTCSGNL']
                signal_type = tc_warning.get('type', '')
                signal_code = tc_warning.get('code', '')
                signal_info = signal_type
                issue_time = tc_warning.get('issueTime', '')
                
                # Parse signal number from type or code
                if 'No. 8' in signal_type or 'TC8' in signal_code:
                    current_signal = 8
                elif 'No. 9' in signal_type or 'TC9' in signal_code:
                    current_signal = 9
                elif 'No. 10' in signal_type or 'TC10' in signal_code:
                    current_signal = 10
                elif 'No. 3' in signal_type or 'TC3' in signal_code:
                    current_signal = 3
                elif 'No. 1' in signal_type or 'TC1' in signal_code:
                    current_signal = 1
                else:
                    # Try to extract number from signal code
                    import re
                    match = re.search(r'TC(\d+)', signal_code)
                    if match:
                        current_signal = int(match.group(1))
            
            return {
                'signal': current_signal,
                'info': signal_info,
                'code': signal_code,
                'issue_time': issue_time,
                'last_update': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error fetching HKO official signal: {e}")
            return {
                'signal': -1,  # -1 indicates error
                'info': 'Unable to fetch official signal',
                'code': 'ERROR',
                'issue_time': '',
                'last_update': datetime.now().isoformat()
            }
    
    def parse_csv_data(self, csv_text: str) -> Optional[Dict]:
        """Parse CSV data to extract wind measurements"""
        try:
            lines = csv_text.strip().split('\n')
            if len(lines) < 2:
                print(f"⚠️ CSV has insufficient data: {len(lines)} lines")
                return None
                
            # Skip header and get latest reading
            data_line = lines[-1]  # Most recent reading
            values = [v.strip() for v in data_line.split(',')]
            
            print(f"🔍 Parsing CSV line: {values[:15]}...")  # Debug first 15 values
            
            # For HKO CSV format: wind speed is at column 9, gust at column 10
            # Format: Date time (Year),Month,Day,Hour,Minute,Second,Time Zone,Station,Direction,Speed,Gust,...
            wind_speed = None
            wind_gust = None
            
            # Try to extract from expected HKO positions first
            try:
                if len(values) > 10:
                    speed_val = float(values[9]) if values[9] else None
                    gust_val = float(values[10]) if values[10] else None
                    
                    if speed_val is not None and 0 <= speed_val <= 200:
                        wind_speed = speed_val
                        if gust_val is not None and 0 <= gust_val <= 300:
                            wind_gust = gust_val
                        else:
                            wind_gust = wind_speed * 1.3  # Estimate if gust missing
                        print(f"  HKO format parsed: speed={wind_speed}, gust={wind_gust}")
                        return {
                            'wind_speed': wind_speed,
                            'wind_gust': wind_gust,
                            'timestamp': datetime.now(timezone.utc)
                        }
            except (ValueError, IndexError):
                pass
            
            # Fallback: Look for numerical values that could be wind speeds
            wind_candidates = []
            for i, val in enumerate(values[5:], start=5):  # Skip first 5 columns
                try:
                    num_val = float(val)
                    # Reasonable wind speed range (km/h)
                    if 0 <= num_val <= 150:
                        wind_candidates.append((i, num_val))
                        print(f"  Found wind candidate at column {i}: {num_val}")
                except (ValueError, TypeError):
                    continue
            
            # Look for the actual wind speed patterns
            if len(wind_candidates) >= 2:
                # Take the first reasonable pair where gust >= speed
                for i in range(len(wind_candidates) - 1):
                    speed_val = wind_candidates[i][1]
                    gust_val = wind_candidates[i+1][1]
                    
                    if gust_val >= speed_val:  # Gust should be >= speed
                        wind_speed = speed_val
                        wind_gust = gust_val
                        break
                
                # If no good pair found, take the highest single value
                if wind_speed is None and wind_candidates:
                    max_candidate = max(wind_candidates, key=lambda x: x[1])
                    wind_speed = max_candidate[1]
                    wind_gust = wind_speed * 1.3  # Estimate gust
            
            print(f"  Final parsed: speed={wind_speed}, gust={wind_gust}")
            
            if wind_speed is None:
                return None
            
            return {
                'wind_speed': wind_speed,
                'wind_gust': wind_gust,
                'timestamp': datetime.now(timezone.utc)
            }
            
        except Exception as e:
            print(f"❌ CSV parsing error: {e}")
            return None
    
    def fetch_wind_data_from_csv(self):
        """Fetch latest wind data from the collector's CSV log, with fallback to live API."""
        try:
            print(f"🔄 Reading latest data from collector's CSV log...")
            
            log_path = self.csv_filename_pattern.format(datetime.now().strftime('%Y%m%d'))
            
            if not os.path.exists(log_path):
                print(f"⚠️ Collector log file not found: {log_path}. Falling back to live HKO API...")
                return self.fetch_live_hko_data()

            latest_timestamp = None
            station_updates = []
            with open(log_path, 'r', newline='', encoding='utf-8') as f:
                reader = list(csv.DictReader(f))
                if not reader:
                    print("⚠️ Collector log is empty. Falling back to live HKO API...")
                    return self.fetch_live_hko_data()
                # Group rows by timestamp
                from collections import defaultdict
                groups = defaultdict(list)
                for row in reader:
                    ts = row.get('timestamp_utc', '')
                    if ts:
                        groups[ts].append(row)
                # Choose a group:
                # 1) Prefer the latest ts with at least MIN_GROUP_SIZE rows
                # 2) Else pick the ts with the maximum count
                MIN_GROUP_SIZE = 10
                # Sort timestamps ascending for recency checks
                sorted_ts = sorted(groups.keys())
                chosen_ts = None
                for ts in reversed(sorted_ts):
                    if len(groups[ts]) >= MIN_GROUP_SIZE:
                        chosen_ts = ts
                        break
                if not chosen_ts:
                    # Pick the most complete group overall
                    chosen_ts = max(groups.items(), key=lambda kv: len(kv[1]))[0]
                latest_timestamp = chosen_ts
                station_updates = list(groups[chosen_ts])
                print(f"🗂️ Selected CSV batch {chosen_ts} with {len(station_updates)} rows (MIN={MIN_GROUP_SIZE})")
            
            # Check for suspicious data (all stations with identical low values)
            if station_updates:
                wind_speeds = []
                for update in station_updates:
                    try:
                        speed = float(update.get('wind_speed_kmh', '0') or 0)
                        wind_speeds.append(speed)
                    except (ValueError, TypeError):
                        pass
                
                # If all speeds are identical and low (likely parsing error), use live data
                if len(set(wind_speeds)) == 1 and wind_speeds and wind_speeds[0] <= 10:
                    print(f"⚠️ Suspicious CSV data detected (all stations: {wind_speeds[0]} km/h). Using live HKO API...")
                    return self.fetch_live_hko_data()
            # If the selected batch is still too small, fallback to live API
            if not station_updates or len(station_updates) < 5:
                print(f"⚠️ CSV batch too small ({len(station_updates)} rows). Falling back to live HKO API...")
                return self.fetch_live_hko_data()
            
            if not self.stations:
                self.stations = self.fetch_station_locations()

            for station in self.stations:
                station_name = station.get('station_name')
                update_found = False
                for update in station_updates:
                    if update.get('station_name') == station_name:
                        try:
                            wind_speed = float(update.get('wind_speed_kmh', '0') or 0)
                            wind_gust = float(update.get('wind_gust_kmh', '0') or 0)
                            
                            station['last_wind_speed'] = wind_speed
                            station['last_wind_gust'] = wind_gust
                            station['status'] = 'active'
                            
                            if wind_speed >= self.SIGNAL_8_MIN:
                                station['signal_level'] = 8
                            elif wind_speed >= self.SIGNAL_3_MIN:
                                station['signal_level'] = 3
                            else:
                                station['signal_level'] = 1
                            
                            update_found = True
                            break
                        except (ValueError, TypeError):
                            continue
                
                if not update_found:
                    station['status'] = 'no_data'
                    station['signal_level'] = 0

            self.last_update = datetime.fromisoformat(latest_timestamp) if latest_timestamp else datetime.now(timezone.utc)
            self.calculate_overall_signal()
            print(f"✅ Data loaded from CSV for timestamp {latest_timestamp}")

        except Exception as e:
            print(f"❌ Error in fetch_wind_data_from_csv: {e}")
            print("🔄 Falling back to live HKO API...")
            return self.fetch_live_hko_data()

    def fetch_live_hko_data(self):
        """Fetch live data directly from HKO API as fallback when collector CSV is not available."""
        try:
            print(f"🌐 Fetching live data from HKO API...")
            
            if not self.stations:
                self.stations = self.fetch_station_locations()
            
            # For each station, try to fetch its CSV data directly
            active_stations = 0
            for station in self.stations:
                csv_url = station.get('csv_url', '')
                if csv_url:
                    try:
                        response = requests.get(csv_url, timeout=10)
                        response.raise_for_status()
                        
                        # Parse the latest reading from the CSV
                        csv_data = self.parse_csv_data(response.text)
                        if csv_data and csv_data['wind_speed'] is not None:
                            wind_speed = csv_data['wind_speed']
                            wind_gust = csv_data.get('wind_gust', wind_speed * 1.3)
                            
                            station['last_wind_speed'] = wind_speed
                            station['last_wind_gust'] = wind_gust
                            station['status'] = 'active'
                            
                            if wind_speed >= self.SIGNAL_8_MIN:
                                station['signal_level'] = 8
                            elif wind_speed >= self.SIGNAL_3_MIN:
                                station['signal_level'] = 3
                            else:
                                station['signal_level'] = 1
                            
                            active_stations += 1
                        else:
                            station['status'] = 'no_data'
                            station['signal_level'] = 0
                    except Exception as e:
                        print(f"⚠️ Failed to fetch data for {station['station_name']}: {e}")
                        station['status'] = 'error'
                        station['signal_level'] = 0
                else:
                    station['status'] = 'no_data'
                    station['signal_level'] = 0

            self.last_update = datetime.now(timezone.utc)
            self.calculate_overall_signal()
            print(f"✅ Live data fetched from HKO API for {active_stations} stations")

        except Exception as e:
            print(f"❌ Error in fetch_live_hko_data: {e}")
            self.wind_data = {'overall_signal': 0, 'signal_reason': f'Error fetching live data: {e}'}
            self.last_update = datetime.now(timezone.utc)

    def fetch_wind_data(self):
        """Fetch simulated wind data from all stations (FOR LOCAL DEV ONLY)"""
        try:
            print(f"🌪️ [SIMULATING] Fetching wind data from {len(self.stations)} stations...")
            import random
            
            current_hour = datetime.now().hour
            if 6 <= current_hour <= 18:
                base_wind_range = (15, 45)
            elif 19 <= current_hour <= 23:
                base_wind_range = (25, 65) 
            else:
                base_wind_range = (30, 85)
            
            for i, station in enumerate(self.stations):
                if i < 5:
                    base_wind = random.uniform(base_wind_range[0] + 20, base_wind_range[1] + 20)
                elif i < 10:
                    base_wind = random.uniform(base_wind_range[0] + 10, base_wind_range[1] + 5)
                else:
                    base_wind = random.uniform(base_wind_range[0], base_wind_range[1])
                
                wind_variation = random.uniform(-5, 5)
                wind_speed = max(5, base_wind + wind_variation)
                gust_factor = random.uniform(1.2, 1.6)
                wind_gust = wind_speed * gust_factor
                
                station['last_wind_speed'] = round(wind_speed, 1)
                station['last_wind_gust'] = round(wind_gust, 1)
                station['status'] = 'active'
                
                if wind_speed >= self.SIGNAL_8_MIN:
                    station['signal_level'] = 8
                elif wind_speed >= self.SIGNAL_3_MIN:
                    station['signal_level'] = 3
                else:
                    station['signal_level'] = 1
            
            self.last_update = datetime.now(timezone.utc)
            self.calculate_overall_signal()
            
        except Exception as e:
            print(f"❌ Error in fetch_wind_data (simulation): {e}")

    def calculate_overall_signal(self):
        """Calculate overall typhoon signal based on HKO criteria"""
        active_stations = [s for s in self.stations if s['status'] == 'active' and s['last_wind_speed'] is not None]
        total_stations = len(active_stations)
        
        if total_stations == 0:
            self.wind_data['overall_signal'] = 0
            return
        
        signal8_stations = len([s for s in active_stations if s['last_wind_speed'] >= self.SIGNAL_8_MIN])
        signal3_stations = len([s for s in active_stations if s['last_wind_speed'] >= self.SIGNAL_3_MIN])
        
        # HKO Criteria: Half or more stations must meet the threshold
        half_stations = total_stations / 2
        
        if signal8_stations >= half_stations:
            self.wind_data['overall_signal'] = 8
            self.wind_data['signal_reason'] = f"{signal8_stations}/{total_stations} stations ≥ 63 km/h"
        elif signal3_stations >= half_stations:
            self.wind_data['overall_signal'] = 3
            self.wind_data['signal_reason'] = f"{signal3_stations}/{total_stations} stations ≥ 41 km/h"
        else:
            self.wind_data['overall_signal'] = "weaker than Signal 3"
            self.wind_data['signal_reason'] = f"Only {signal3_stations}/{total_stations} stations ≥ 41 km/h (need {int(half_stations)}+ for Signal 3)"
        
        # Fetch official HKO signal for comparison
        official_signal = self.fetch_official_hko_signal()
        
        self.wind_data.update({
            'total_stations': total_stations,
            'signal8_stations': signal8_stations,
            'signal3_stations': signal3_stations,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'official_signal': official_signal,
            'signal_match': (
                self.wind_data['overall_signal'] == official_signal['signal'] if 
                isinstance(self.wind_data['overall_signal'], int) else False
            ),
            'early_signal8_concern': {
                'active': True,
                'message': "Concern raised: Earlier than usual announcement of Signal 8 until 11 AM on September 9, 2025"
            }
        })
        
        # This is no longer needed as the web service reads, not writes.
        # # This is no longer needed as the web service reads, not writes.
        # self.log_to_csv(self.stations, self.wind_data['overall_signal'], official_signal['signal'])

        # Append to in-memory history and prune to analysis window
        try:
            calculated_signal = self.wind_data.get('overall_signal', 0)
            # Convert string to number for history tracking
            if isinstance(calculated_signal, str):
                calculated_signal = 0  # "weaker than Signal 3" -> 0
            
            self.append_history_record(self.last_update or datetime.now(timezone.utc),
                                       official_signal.get('signal', -1),
                                       calculated_signal)
            self.prune_history_to_window()
        except Exception as e:
            print(f"❌ Error updating history: {e}")

    # ===== History tracking for match/mismatch window (now -> 11:00 HKT tomorrow) =====
    def _now_utc(self) -> datetime:
        return datetime.now(timezone.utc)

    def _to_hkt(self, dt_utc: datetime) -> datetime:
        # HKT is UTC+8, no DST
        return (dt_utc + timedelta(hours=8)).replace(tzinfo=timezone.utc)

    def _from_hkt_to_utc(self, naive_hkt: datetime) -> datetime:
        # naive_hkt is a naive datetime interpreted as HKT; convert to UTC
        return (naive_hkt - timedelta(hours=8)).replace(tzinfo=timezone.utc)

    def get_window_bounds_utc(self):
        now_utc = self._now_utc()
        now_hkt = now_utc + timedelta(hours=8)
        # Start is 01:00 HKT today if current time is after 01:00, otherwise now
        if now_hkt.hour >= 1:
            start_hkt_naive = datetime(now_hkt.year, now_hkt.month, now_hkt.day, 1, 0, 0)
        else:
            start_hkt_naive = datetime(now_hkt.year, now_hkt.month, now_hkt.day, now_hkt.hour, now_hkt.minute, now_hkt.second)
        start_utc = self._from_hkt_to_utc(start_hkt_naive)
        # End is 11:00 HKT tomorrow
        end_date_hkt = (now_hkt.date() + timedelta(days=1))
        end_hkt_naive = datetime(end_date_hkt.year, end_date_hkt.month, end_date_hkt.day, 11, 0, 0)
        end_utc = self._from_hkt_to_utc(end_hkt_naive)
        return start_utc, end_utc

    def append_history_record(self, ts_utc: datetime, official: int, calculated: int):
        self.history.append({
            'ts_utc': ts_utc,
            'official': official,
            'calculated': calculated,
            'match': bool(official == calculated)
        })

    def prune_history_to_window(self):
        start_utc, end_utc = self.get_window_bounds_utc()
        self.history = [r for r in self.history if start_utc <= r['ts_utc'] <= end_utc]

    def get_match_mismatch_summary(self):
        # Always try CSV method first to get both historical and real-time data
        csv_result = self.get_match_mismatch_summary_from_csv()
        
        # If CSV fails, fall back to in-memory data
        if 'error' in csv_result:
            print(f"⚠️ CSV method failed: {csv_result.get('error')}. Falling back to in-memory data...")
            try:
                self.prune_history_to_window()
                if len(self.history) > 0:
                    start_utc, end_utc = self.get_window_bounds_utc()
                    match_count = sum(1 for r in self.history if r['match'])
                    mismatch_count = sum(1 for r in self.history if not r['match'])
                    total = len(self.history)
                    records = []
                    for r in self.history:
                        hkt_dt = (r['ts_utc'] + timedelta(hours=8))
                        records.append({
                            'time_hkt': hkt_dt.isoformat(),
                            'official': r['official'],
                            'calculated': r['calculated'],
                            'match': r['match']
                        })
                    return {
                        'source': 'memory',
                        'window_start_hkt': (start_utc + timedelta(hours=8)).isoformat(),
                        'window_end_hkt': (end_utc + timedelta(hours=8)).isoformat(),
                        'total_updates': total,
                        'matches': match_count,
                        'mismatches': mismatch_count,
                        'records': records
                    }
                else:
                    return {'error': 'No data available in memory either', 'source': 'memory'}
            except Exception as e:
                print(f"❌ In-memory fallback also failed: {e}")
                return {'error': f'Both CSV and memory methods failed: {csv_result.get("error")} | {e}', 'source': 'failed'}
        
        return csv_result

    def get_match_mismatch_summary_from_csv(self):
        # Compute summary from the daily CSV log by grouping on timestamp
        try:
            # Try multiple paths for the collected data
            collected_csv_paths = [
                '/Users/simonwang/Documents/Usage/VibeCoding/letter_writing/data_archive/hk_wind_log_20250908.csv',  # Local original
                'data_archive/hk_wind_log_20250908_deploy.csv',  # Railway deployment
                './data_archive/hk_wind_log_20250908_deploy.csv',  # Relative path
                os.path.join(os.path.dirname(__file__), 'data_archive', 'hk_wind_log_20250908_deploy.csv')  # Absolute from script
            ]
            
            # Also check today's date for any additional data
            today_log_path = self.csv_filename_pattern.format(datetime.now().strftime('%Y%m%d'))
            
            # Find the first existing CSV file
            log_path = None
            for path in collected_csv_paths:
                print(f"🔍 Checking CSV path: {path} - exists: {os.path.exists(path)}")
                if os.path.exists(path):
                    log_path = path
                    print(f"📊 Using CSV data from: {path}")
                    break
            
            # Fall back to today's log if no collected data found
            if not log_path and os.path.exists(today_log_path):
                log_path = today_log_path
                print(f"📊 Using today's log: {today_log_path}")
            
            if not log_path:
                print(f"❌ No CSV file found. Current dir: {os.getcwd()}")
                print(f"❌ Files in current dir: {os.listdir('.')}")
                if os.path.exists('data_archive'):
                    print(f"❌ Files in data_archive: {os.listdir('data_archive')}")
                return {'error': 'CSV log not found', 'source': 'csv'}

            # First pass: find actual data range
            earliest_time = None
            latest_time = None
            
            with open(log_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ts_str = row.get('timestamp_utc')
                    if not ts_str:
                        continue
                    try:
                        dt_utc = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                        dt_local_naive = dt_utc.astimezone().replace(tzinfo=None)
                        
                        if earliest_time is None or dt_local_naive < earliest_time:
                            earliest_time = dt_local_naive
                        if latest_time is None or dt_local_naive > latest_time:
                            latest_time = dt_local_naive
                    except Exception:
                        continue
            
            # Use actual data range as window, but extend to current time for ongoing monitoring
            if earliest_time and latest_time:
                start_local = earliest_time
                # Extend the end time to now to include real-time updates
                now_local = datetime.now()
                end_local = max(latest_time, now_local)
            else:
                # Fallback to original 1am-11am window
                now_local = datetime.now()
                if now_local.hour >= 1:
                    start_local = datetime(now_local.year, now_local.month, now_local.day, 1, 0, 0)
                else:
                    start_local = now_local
                end_date = now_local.date() + timedelta(days=1)
                end_local = datetime(end_date.year, end_date.month, end_date.day, 11, 0, 0)

            groups = {}
            with open(log_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ts_str = row.get('timestamp_utc')
                    if not ts_str:
                        continue
                    try:
                        # Convert UTC timestamp from CSV to local naive for comparison
                        dt_utc = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                        dt_local_naive = dt_utc.astimezone().replace(tzinfo=None)
                    except Exception:
                        continue # Skip unparsable
                    
                    if not (start_local <= dt_local_naive <= end_local):
                        continue

                    # Re-calculate overall signal for this timestamp group
                    # This is inefficient but necessary if the CSV doesn't store it
                    # For now, we assume the collector doesn't calculate it.
                    # Let's assume the official signal is present.
                    ts_group_key = row['timestamp_utc']
                    if ts_group_key not in groups:
                        groups[ts_group_key] = {
                            'stations': [], 
                            'official': -1, 
                            'timestamp_hkt': row.get('timestamp_hkt', '')
                        }
                    
                    try:
                        groups[ts_group_key]['official'] = int(row.get('official_signal_hko', '-1') or -1)
                        wind_speed = float(row.get('wind_speed_kmh', '0') or 0)
                        groups[ts_group_key]['stations'].append(wind_speed)
                    except (ValueError, TypeError):
                        continue

            # Process groups to get final match/mismatch
            processed_updates = []
            for ts, data in groups.items():
                total_stations = len(data['stations'])
                if total_stations == 0: continue

                signal8_stations = sum(1 for s in data['stations'] if s >= self.SIGNAL_8_MIN)
                signal3_stations = sum(1 for s in data['stations'] if s >= self.SIGNAL_3_MIN)
                half_stations = total_stations / 2
                
                calculated_signal = 1
                if signal8_stations >= half_stations:
                    calculated_signal = 8
                elif signal3_stations >= half_stations:
                    calculated_signal = 3

                processed_updates.append({
                    'time_utc': ts,
                    'time_hkt': data['timestamp_hkt'],
                    'official': data['official'],
                    'calculated': calculated_signal,
                    'match': data['official'] == calculated_signal
                })

            # Add current real-time comparison if we're extending to current time
            now_local = datetime.now()
            if end_local > latest_time if latest_time else True:
                try:
                    # Get current data for real-time comparison
                    self.ensure_fresh_data()
                    current_official = self.fetch_official_hko_signal()
                    current_official_code = current_official.get('signal', 0) if current_official else 0
                    
                    current_calculated = 0  # Default
                    if hasattr(self, 'wind_data') and self.wind_data:
                        # Get the overall signal and convert to numeric
                        overall_signal = self.wind_data.get('overall_signal', 'weaker than Signal 3')
                        if isinstance(overall_signal, str):
                            if 'Signal 3' in overall_signal:
                                current_calculated = 3
                            elif 'Signal 8' in overall_signal:
                                current_calculated = 8
                            else:
                                current_calculated = 0  # weaker than Signal 3
                        else:
                            current_calculated = int(overall_signal) if overall_signal else 0
                    
                    # Add current comparison if we have valid data
                    if current_official_code > 0:
                        current_utc = datetime.now(timezone.utc)
                        current_hkt = current_utc.astimezone(timezone(timedelta(hours=8)))
                        
                        processed_updates.append({
                            'time_utc': current_utc.isoformat(),
                            'time_hkt': current_hkt.isoformat(),
                            'official': current_official_code,
                            'calculated': current_calculated,
                            'match': current_official_code == current_calculated
                        })
                        print(f"📊 Added real-time comparison: Official={current_official_code}, Calculated={current_calculated}")
                except Exception as e:
                    print(f"⚠️ Could not add real-time comparison: {e}")

            total = len(processed_updates)
            matches = sum(1 for r in processed_updates if r['match'])
            mismatches = total - matches
            
            records = []
            for r in sorted(processed_updates, key=lambda x: x['time_utc'], reverse=True):  # Most recent first
                records.append({
                    'time_local': r['time_utc'], # Keep UTC for compatibility
                    'time_hkt': r['time_hkt'],   # Add proper HKT timestamp
                    'official': r['official'],
                    'calculated': r['calculated'],
                    'match': r['match']
                })

            return {
                'source': 'csv',
                'window_start_local': start_local.isoformat(),
                'window_end_local': end_local.isoformat(),
                'window_start_hkt': start_local.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
                'window_end_hkt': end_local.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
                'total_updates': total,
                'matches': matches,
                'mismatches': mismatches,
                'records': records[-20:]  # last up to 20 records
            }
        except Exception as e:
            return {
                'error': f'CSV summary failed: {e}',
                'source': 'csv'
            }
    
    def monitor_loop(self):
        """Continuous monitoring loop"""
        print("🚀 Starting Hong Kong Wind Monitor...")
        
        # Initial setup
        self.stations = self.fetch_station_locations()
        
        while self.is_running:
            try:
                self.fetch_wind_data()
                print(f"✅ Data updated at {datetime.now().strftime('%H:%M:%S')} - Signal {self.wind_data.get('overall_signal', 0)}")
                
                # Wait 10 minutes (600 seconds) for next update
                for _ in range(600):  # 10 minutes in seconds
                    if not self.is_running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                print(f"❌ Error in monitoring loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
        
        print("🛑 Wind monitoring stopped")
    
    def start_monitoring(self):
        """Start background monitoring thread"""
        with self._thread_lock:
            if self._thread_started:
                return None
            self._thread_started = True
            monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            monitor_thread.start()
            return monitor_thread

    def ensure_fresh_data(self, max_age_seconds: int = 540):
        """Ensure stations are loaded and wind data is fresh (default 9 min)."""
        try:
            # Use an environment variable to be explicit about the environment
            is_production = os.environ.get('FLASK_ENV') == 'production'

            if not self.stations:
                self.stations = self.fetch_station_locations()

            now = datetime.now(timezone.utc)
            if not self.last_update or (now - self.last_update).total_seconds() > max_age_seconds:
                if is_production:
                    # Production should always show live HKO API data
                    print("Production environment detected. Fetching LIVE HKO data.")
                    self.fetch_live_hko_data()
                    # As a last resort, if no stations returned, fall back to CSV log
                    if self.wind_data.get('total_stations', 0) == 0:
                        print("⚠️ Live data returned zero stations. Falling back to CSV log once.")
                        self.fetch_wind_data_from_csv()
                else:
                    # Local dev runs the simulation
                    print("Local environment detected. Running simulation.")
                    self.fetch_wind_data()
        except Exception as e:
            print(f"❌ ensure_fresh_data error: {e}")

# Global wind monitor instance
wind_monitor = HKWindMonitor()

# No longer needed for Flask 3 / Gunicorn
# @app.before_first_request
# def _init_background_and_warm_cache():
#     """Start the background monitor in WSGI (Gunicorn) and warm initial data."""
#     try:
#         wind_monitor.start_monitoring()
#         # Warm up data so first request isn't empty
#         wind_monitor.ensure_fresh_data(max_age_seconds=0)
#     except Exception as e:
#         print(f"❌ Error during app warm-up: {e}")

def calculate_next_update(last_update_str):
    """Calculate when the next update is expected based on the last update time"""
    try:
        if last_update_str:
            # Parse last update time and add 10 minutes
            last_update = datetime.fromisoformat(last_update_str.replace('Z', '+00:00'))
            next_update = last_update + timedelta(minutes=10)
            return next_update.isoformat()
        else:
            # If no last update, assume next update is in 10 minutes from now
            return (datetime.now() + timedelta(minutes=10)).isoformat()
    except Exception:
        # Fallback to current time + 10 minutes
        return (datetime.now() + timedelta(minutes=10)).isoformat()

def get_numeric_signal(overall_signal):
    """Convert signal string to numeric value for API consistency"""
    if isinstance(overall_signal, str):
        if 'Signal 8' in overall_signal:
            return 8
        elif 'Signal 3' in overall_signal:
            return 3
        else:
            return 0  # weaker than Signal 3
    return int(overall_signal) if overall_signal else 0

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/wind-data')
def api_wind_data():
    """API endpoint for current wind data"""
    # Ensure data is available/fresh even if background monitor hasn't kicked in yet
    wind_monitor.ensure_fresh_data()
    return jsonify({
        'stations': wind_monitor.stations,
        'overall_signal': wind_monitor.wind_data.get('overall_signal', 0),
        'calculated_signal': get_numeric_signal(wind_monitor.wind_data.get('overall_signal', 'weaker than Signal 3')),
        'signal_reason': wind_monitor.wind_data.get('signal_reason', 'No data'),
        'total_stations': wind_monitor.wind_data.get('total_stations', 0),
        'signal8_stations': wind_monitor.wind_data.get('signal8_stations', 0),
        'signal3_stations': wind_monitor.wind_data.get('signal3_stations', 0),
        'last_update': wind_monitor.wind_data.get('last_update'),
        'next_update': calculate_next_update(wind_monitor.wind_data.get('last_update')),
        'official_signal': wind_monitor.wind_data.get('official_signal', {}),
        'signal_match': wind_monitor.wind_data.get('signal_match', False),
        'early_signal8_concern': wind_monitor.wind_data.get('early_signal8_concern', {}),
        'criteria': {
            'signal_3_range': f"{wind_monitor.SIGNAL_3_MIN}-{wind_monitor.SIGNAL_3_MAX} km/h",
            'signal_8_range': f"{wind_monitor.SIGNAL_8_MIN}-{wind_monitor.SIGNAL_8_MAX} km/h",
            'threshold_rule': "Half or more stations must meet sustained wind criteria"
        },
        'credits': {
            'researcher': "Dr Simon Wang, Lecturer and Innovation Officer, Language Centre, HKBU",
            'email': "simonwang@hkbu.edu.hk",
            'assistant': "GitHub Copilot agent",
            'data_source': "Hong Kong Observatory"
        }
    })

@app.route('/api/match-summary')
def api_match_summary():
    """API endpoint returning match/mismatch summary for now -> 11:00 HKT tomorrow."""
    try:
        summary = wind_monitor.get_match_mismatch_summary()
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/data/csv')
def download_csv():
    """Generate and serve only corrected data as CSV for public access.
    Rules:
    - Include external curated data file (2025-09-07) in unified schema.
    - Include our collector logs ONLY from/after the integrity cutoff (HKT).
    - Exclude live snapshot to avoid mixing potentially inconsistent data.
    - Deduplicate by (timestamp_utc, station_name).
    """
    try:
        import csv as csv_lib
        
        # Helpers
        HKT = timezone(timedelta(hours=8))
        def parse_hkt(ts: str):
            if not ts:
                return None
            try:
                # Try full ISO first
                dt = datetime.fromisoformat(ts)
                return dt.astimezone(HKT) if dt.tzinfo else dt.replace(tzinfo=HKT)
            except Exception:
                pass
            try:
                # Try 'YYYY-MM-DD HH:MM:SS' as naive HKT
                dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
                return dt.replace(tzinfo=HKT)
            except Exception:
                return None

        # Integrity cutoff: rows before this HKT time from our logs are excluded
        cutoff_hkt = datetime(2025, 9, 8, 9, 55, 0, tzinfo=HKT)

        # Output schema header
        header = "timestamp_utc,timestamp_hkt,station_name,latitude,longitude,wind_speed_kmh,wind_gust_kmh,data_url,official_signal_hko,data_source"
        rows_out = []

        # Helper to add filtered internal logs
        def add_internal_log(path: str, label: str):
            if not os.path.exists(path):
                return
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv_lib.DictReader(f)
                for row in reader:
                    ts_hkt_raw = row.get('timestamp_hkt', '')
                    dt_hkt = parse_hkt(ts_hkt_raw)
                    if dt_hkt is None or dt_hkt < cutoff_hkt:
                        continue
                    rows_out.append([
                        row.get('timestamp_utc', ''),
                        ts_hkt_raw,
                        row.get('station_name', ''),
                        row.get('latitude', ''),
                        row.get('longitude', ''),
                        row.get('wind_speed_kmh', ''),
                        row.get('wind_gust_kmh', ''),
                        row.get('data_url', ''),
                        row.get('official_signal_hko', ''),
                        label
                    ])

        # Add 2025-09-08 (typhoon day) log with filtering and today's log
        add_internal_log(os.path.join('data_archive', 'hk_wind_log_20250908.csv'), 'collector_20250908_filtered')
        ymd = datetime.now().strftime('%Y%m%d')
        add_internal_log(os.path.join('data_archive', f'hk_wind_log_{ymd}.csv'), 'collector_today_filtered')

        # Add the curated external data file (no cutoff filter; already curated)
        external_path = os.path.join('data_archive', 'hko_wind_data_20250907_224309-1003.csv')
        if os.path.exists(external_path):
            with open(external_path, 'r', encoding='utf-8') as f:
                reader = csv_lib.DictReader(f)
                for row in reader:
                    ts_hkt_raw = row.get('timestamp', '')
                    dt_hkt = parse_hkt(ts_hkt_raw)
                    if dt_hkt:
                        ts_hkt_iso = dt_hkt.isoformat()
                        ts_utc_iso = dt_hkt.astimezone(timezone.utc).isoformat()
                    else:
                        ts_hkt_iso = ts_hkt_raw
                        ts_utc_iso = ''
                    rows_out.append([
                        ts_utc_iso,
                        ts_hkt_iso,
                        row.get('station_name', ''),
                        '',  # latitude unknown in external file
                        '',  # longitude unknown in external file
                        row.get('wind_speed_kmh', ''),
                        row.get('wind_gust_kmh', ''),
                        '',  # data_url not available in external file
                        '',  # official signal unknown for each row
                        'external_hko_20250907'
                    ])

        # Deduplicate by (timestamp_utc, station_name)
        seen = set()
        out_lines = [header]
        for r in rows_out:
            key = (r[0], r[2])
            if key in seen:
                continue
            seen.add(key)
            out_lines.append(','.join(str(x) for x in r))

        from flask import Response
        # Filename timestamp in HKT
        now_hkt = datetime.now(timezone.utc).astimezone(HKT)
        filename = f"hk_wind_corrected_data_{now_hkt.strftime('%Y%m%d_%H%M%S')}.csv"
        csv_string = '\n'.join(out_lines)
        return Response(csv_string, mimetype='text/csv', headers={'Content-Disposition': f'attachment; filename="{filename}"'})
    except Exception as e:
        return jsonify({'error': f'Could not generate CSV: {e}'}), 500

@app.route('/about')
def about():
    """Information page about data sources and methodology"""
    return render_template('about.html')

@app.route('/analysis')
def analysis_under_construction():
    return render_template('under_construction.html')

@app.route('/health/collector')
def health_collector():
    try:
        ymd = datetime.now().strftime('%Y%m%d')
        today_log = os.path.join('data_archive', f'hk_wind_log_{ymd}.csv')
        exists = os.path.exists(today_log)
        last_line = None
        if exists:
            with open(today_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    last_line = lines[-1].strip()
        return jsonify({
            'today_log_exists': exists,
            'today_log_path': today_log,
            'last_entry': last_line
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # When running locally, start the background monitor for simulated data.
    # The deployed version does NOT run this; it relies on the collector.
    print("🚀 Starting local development server with SIMULATED data...")
    os.environ['FLASK_ENV'] = 'development' # Set env for local run
    wind_monitor.start_monitoring()
    
    # Give it time to fetch initial data
    time.sleep(5)
    
    # Run Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
