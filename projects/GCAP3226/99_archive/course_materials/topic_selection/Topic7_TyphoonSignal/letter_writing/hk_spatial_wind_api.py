#!/usr/bin/env python3
"""
Hong Kong Observatory Spatial Wind Data Access
==============================================

This script specifically targets the spatial wind data mentioned in the notes,
focusing on the "latest_10min_wind" layer from the HKO Regional Weather API.

Based on the data specification in notes.md:
- Dataset: Regional weather in Hong Kong – latest 10-minute mean wind direction and wind speed and maximum gust
- Layer: latest_10min_wind (Spatial Layer)
- Update Frequency: Every 10 minutes

Author: GitHub Copilot
Date: September 7, 2025
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import re

class HKSpatialWindDataAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json, application/xml, text/xml, */*'
        })
        
        # Endpoints based on the data specification
        self.base_endpoints = [
            # Official HKO Weather API endpoints
            'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en',
            'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=ltmv&lang=en',
            
            # Spatial data endpoints (based on notes)
            'https://portal.csdi.gov.hk/geoportal/rest/services/hko/hko_rcd_1634953844424_88011/MapServer',
            'https://portal.csdi.gov.hk/geoportal/rest/services/hko/hko_rcd_1634953844424_88011/MapServer/0',
            'https://portal.csdi.gov.hk/geoportal/rest/services/hko/hko_rcd_1634953844424_88011/MapServer/0/query',
            
            # Alternative formats
            'https://geodata.gov.hk/gs/api/v1.0.0/geoDataSearch?q=wind',
            'https://api.data.gov.hk/v1/historical-archive/list-file-versions?url=https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread',
        ]
        
        # Signal 8 thresholds (from HKO official criteria)
        self.signal_thresholds = {
            'signal_1': 22,   # km/h - Standby signal
            'signal_3': 41,   # km/h - Strong wind signal  
            'signal_8_ne': 63, # km/h - No. 8 Northeast Gale or Storm Signal
            'signal_8_nw': 63, # km/h - No. 8 Northwest Gale or Storm Signal
            'signal_8_se': 63, # km/h - No. 8 Southeast Gale or Storm Signal
            'signal_8_sw': 63, # km/h - No. 8 Southwest Gale or Storm Signal
            'signal_9': 88,   # km/h - No. 9 Increasing Gale or Storm Signal
            'signal_10': 118, # km/h - No. 10 Hurricane Signal
        }

    def build_spatial_query_url(self, base_url: str) -> str:
        """Build spatial query URL with parameters for wind data"""
        if 'query' not in base_url:
            return base_url
            
        params = {
            'where': '1=1',  # Get all records
            'outFields': '*', # Get all fields
            'f': 'json',     # Return as JSON
            'returnGeometry': 'false',  # We mainly want the data, not geometry
            'orderByFields': 'AutomaticWeatherStation_en',
        }
        
        param_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        return f"{base_url}?{param_string}"

    def fetch_wind_data(self) -> List[Dict]:
        """Fetch wind data from all available endpoints"""
        all_wind_data = []
        
        print("🌪️  Fetching Hong Kong wind data...")
        print("=" * 50)
        
        for base_url in self.base_endpoints:
            try:
                # Build query URL for spatial endpoints
                if 'query' in base_url or 'MapServer' in base_url:
                    url = self.build_spatial_query_url(base_url)
                else:
                    url = base_url
                
                print(f"📡 Trying: {url[:80]}...")
                
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                # Parse response
                data = self._parse_response(response, url)
                if data:
                    all_wind_data.extend(data)
                    print(f"✅ Success: Found {len(data)} data points")
                else:
                    print(f"⚠️  No wind data found")
                    
            except Exception as e:
                print(f"❌ Failed: {str(e)[:60]}...")
                
            time.sleep(1)  # Rate limiting
            
        return all_wind_data

    def _parse_response(self, response: requests.Response, url: str) -> List[Dict]:
        """Parse API response and extract wind data"""
        try:
            content_type = response.headers.get('content-type', '').lower()
            
            # Try JSON first
            if 'json' in content_type or response.text.strip().startswith(('{', '[')):
                return self._parse_json_response(response.json(), url)
            else:
                # If not JSON, check if it contains useful text data
                text = response.text
                if any(keyword in text.lower() for keyword in ['wind', 'weather', 'station']):
                    return [{'raw_data': text[:500], 'source': url, 'type': 'text'}]
                return []
                
        except Exception as e:
            print(f"Parse error: {e}")
            return []

    def _parse_json_response(self, data: dict, url: str) -> List[Dict]:
        """Parse JSON response to extract wind information"""
        wind_data = []
        
        try:
            # Handle ArcGIS REST service responses
            if 'features' in data:
                for feature in data['features']:
                    attributes = feature.get('attributes', {})
                    wind_info = self._extract_wind_info(attributes, url, 'spatial_features')
                    if wind_info:
                        wind_data.append(wind_info)
            
            # Handle HKO weather API responses
            elif 'rainfall' in data:  # Regional weather data structure
                for station_data in data.get('rainfall', []):
                    wind_info = self._extract_wind_info(station_data, url, 'regional_weather')
                    if wind_info:
                        wind_data.append(wind_info)
                        
            # Handle other structured data
            elif isinstance(data, dict):
                wind_info = self._extract_wind_info(data, url, 'general')
                if wind_info:
                    wind_data.append(wind_info)
                    
        except Exception as e:
            print(f"JSON parsing error: {e}")
            
        return wind_data

    def _extract_wind_info(self, data: dict, source: str, data_type: str) -> Optional[Dict]:
        """Extract wind-related information from data object"""
        wind_info = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'data_type': data_type
        }
        
        # Look for station information (from data spec)
        station_fields = ['AutomaticWeatherStation_en', 'AutomaticWeatherStation_uc', 'station']
        for field in station_fields:
            if field in data:
                wind_info['station'] = data[field]
                break
                
        # Look for data URL
        if 'Data_url' in data:
            wind_info['data_url'] = data['Data_url']
        
        # Extract wind-related fields
        wind_fields_found = False
        for key, value in data.items():
            key_lower = str(key).lower()
            
            # Wind speed fields
            if any(wind_term in key_lower for wind_term in ['wind_speed', 'windspeed', 'wind']):
                if any(speed_term in key_lower for speed_term in ['speed', 'velocity']):
                    wind_info['wind_speed'] = value
                    wind_fields_found = True
                    
            # Wind direction fields  
            elif 'direction' in key_lower or 'dir' in key_lower:
                wind_info['wind_direction'] = value
                wind_fields_found = True
                
            # Gust fields
            elif 'gust' in key_lower:
                wind_info['gust_speed'] = value  
                wind_fields_found = True
                
            # Temperature and other weather data
            elif key_lower in ['temperature', 'humidity', 'pressure']:
                wind_info[key_lower] = value
        
        # Only return if we found wind-related data or station info
        return wind_info if (wind_fields_found or 'station' in wind_info) else None

    def analyze_signal_8_probability(self, wind_data: List[Dict]) -> Dict:
        """Analyze probability of Signal 8 issuance for tomorrow morning"""
        
        analysis = {
            'analysis_time': datetime.now().isoformat(),
            'target_period': 'Tomorrow morning (8 AM - 12 PM)',
            'data_points_analyzed': len(wind_data),
            'signal_8_probability': 'UNKNOWN',
            'current_conditions': {},
            'risk_indicators': [],
            'stations_monitored': [],
            'recommendations': []
        }
        
        # Extract current wind conditions
        current_speeds = []
        current_gusts = []
        stations = set()
        
        for data in wind_data:
            if 'station' in data:
                stations.add(data['station'])
                
            # Extract wind speeds (handle different units)
            if 'wind_speed' in data:
                speed = self._normalize_wind_speed(data['wind_speed'])
                if speed:
                    current_speeds.append(speed)
                    
            if 'gust_speed' in data:
                gust = self._normalize_wind_speed(data['gust_speed'])
                if gust:
                    current_gusts.append(gust)
        
        analysis['stations_monitored'] = list(stations)
        
        # Analyze current conditions
        if current_speeds:
            max_speed = max(current_speeds)
            avg_speed = sum(current_speeds) / len(current_speeds)
            analysis['current_conditions']['max_wind_speed_kmh'] = max_speed
            analysis['current_conditions']['avg_wind_speed_kmh'] = round(avg_speed, 1)
            
        if current_gusts:
            max_gust = max(current_gusts)
            analysis['current_conditions']['max_gust_kmh'] = max_gust
            
        # Assess Signal 8 probability
        probability, risk_indicators = self._assess_signal_8_risk(
            current_speeds, current_gusts, len(stations)
        )
        
        analysis['signal_8_probability'] = probability
        analysis['risk_indicators'] = risk_indicators
        analysis['recommendations'] = self._get_recommendations(probability)
        
        return analysis

    def _normalize_wind_speed(self, speed_value) -> Optional[float]:
        """Convert wind speed to km/h"""
        try:
            # Handle different input formats
            if isinstance(speed_value, (int, float)):
                return float(speed_value)
            elif isinstance(speed_value, str):
                # Extract numeric value
                numbers = re.findall(r'\d+\.?\d*', speed_value)
                if numbers:
                    speed = float(numbers[0])
                    # Convert m/s to km/h if needed
                    if 'm/s' in speed_value.lower() or speed < 20:  # Assume m/s if low value
                        return speed * 3.6
                    return speed
        except:
            pass
        return None

    def _assess_signal_8_risk(self, speeds: List[float], gusts: List[float], station_count: int) -> Tuple[str, List[str]]:
        """Assess the risk of Signal 8 based on current conditions"""
        risk_indicators = []
        
        if not speeds and not gusts:
            return "UNKNOWN", ["No wind speed data available"]
        
        max_speed = max(speeds) if speeds else 0
        max_gust = max(gusts) if gusts else 0
        
        # Check against thresholds
        if max_speed >= self.signal_thresholds['signal_8_ne']:
            probability = "HIGH"
            risk_indicators.append(f"Current wind speed ({max_speed:.1f} km/h) already at Signal 8 threshold")
        elif max_speed >= self.signal_thresholds['signal_3']:
            if max_gust >= self.signal_thresholds['signal_8_ne']:
                probability = "HIGH" 
                risk_indicators.append(f"Strong winds ({max_speed:.1f} km/h) with Signal 8+ gusts ({max_gust:.1f} km/h)")
            else:
                probability = "MODERATE"
                risk_indicators.append(f"Strong winds detected ({max_speed:.1f} km/h) - Signal 3 level")
        elif max_speed >= self.signal_thresholds['signal_1']:
            probability = "LOW-MODERATE"
            risk_indicators.append(f"Moderate winds ({max_speed:.1f} km/h) - Monitor for strengthening")
        else:
            probability = "LOW"
            risk_indicators.append(f"Light winds ({max_speed:.1f} km/h) - No immediate concern")
        
        # Additional risk factors
        if station_count < 3:
            risk_indicators.append(f"Limited monitoring stations ({station_count}) - assessment may be incomplete")
            
        if len(speeds) > 5:  # Multiple stations reporting
            speed_range = max(speeds) - min(speeds)
            if speed_range > 20:
                risk_indicators.append("Large wind speed variation across stations - localized severe weather possible")
        
        return probability, risk_indicators

    def _get_recommendations(self, probability: str) -> List[str]:
        """Get recommendations based on probability assessment"""
        recommendations = {
            "HIGH": [
                "🚨 Monitor HKO Signal 8 warnings closely - issuance likely",
                "🏠 Secure all loose objects and outdoor furniture NOW",
                "🚌 Check public transport status - services may be suspended",
                "💼 Consider flexible work arrangements for tomorrow",
                "📱 Keep emergency supplies and phone charged"
            ],
            "MODERATE": [
                "⚠️  Stay alert for weather warnings and updates",
                "🔧 Prepare to secure loose objects if conditions worsen", 
                "🚌 Monitor public transport announcements",
                "📊 Check updated forecasts every 2-3 hours"
            ],
            "LOW-MODERATE": [
                "👀 Continue monitoring weather conditions",
                "📱 Enable HKO weather alert notifications",
                "🌊 Stay informed about weather developments"
            ],
            "LOW": [
                "✅ Current conditions appear stable",
                "📱 Maintain awareness of weather updates",
                "🌤️  Normal precautions sufficient"
            ],
            "UNKNOWN": [
                "❓ Unable to assess due to limited data",
                "🔍 Check official HKO forecasts and warnings",
                "📱 Monitor multiple weather sources",
                "⏰ Re-run analysis when more data available"
            ]
        }
        
        return recommendations.get(probability, recommendations["UNKNOWN"])

    def generate_report(self, wind_data: List[Dict], analysis: Dict):
        """Generate a comprehensive report"""
        
        print("\n" + "🌪️ " * 20)
        print("HONG KONG WIND CONDITIONS REPORT")
        print("Signal 8 Assessment for Tomorrow Morning")
        print("🌪️ " * 20)
        
        print(f"\n📊 DATA SUMMARY")
        print("=" * 40)
        print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S HKT')}")
        print(f"Data Points: {analysis['data_points_analyzed']}")
        print(f"Stations Monitored: {len(analysis['stations_monitored'])}")
        
        if analysis['stations_monitored']:
            print(f"Station List: {', '.join(analysis['stations_monitored'][:5])}")
            if len(analysis['stations_monitored']) > 5:
                print(f"             ...and {len(analysis['stations_monitored']) - 5} more")
        
        print(f"\n🌬️  CURRENT CONDITIONS") 
        print("=" * 40)
        current = analysis['current_conditions']
        
        if current:
            if 'max_wind_speed_kmh' in current:
                print(f"Max Wind Speed: {current['max_wind_speed_kmh']:.1f} km/h")
            if 'avg_wind_speed_kmh' in current:
                print(f"Avg Wind Speed: {current['avg_wind_speed_kmh']:.1f} km/h")
            if 'max_gust_kmh' in current:
                print(f"Max Gust Speed: {current['max_gust_kmh']:.1f} km/h")
        else:
            print("No current wind speed data available")
        
        print(f"\n🎯 SIGNAL 8 ASSESSMENT")
        print("=" * 40)
        print(f"Probability: {analysis['signal_8_probability']}")
        print(f"Target Period: {analysis['target_period']}")
        
        print(f"\n📈 RISK INDICATORS")
        for indicator in analysis['risk_indicators']:
            print(f"  • {indicator}")
        
        print(f"\n💡 RECOMMENDATIONS") 
        for rec in analysis['recommendations']:
            print(f"  {rec}")
        
        print(f"\n📋 SIGNAL REFERENCE")
        print("=" * 40)
        print(f"Signal 1 (Standby): {self.signal_thresholds['signal_1']} km/h")
        print(f"Signal 3 (Strong Wind): {self.signal_thresholds['signal_3']} km/h") 
        print(f"Signal 8 (Gale/Storm): {self.signal_thresholds['signal_8_ne']} km/h")
        print(f"Signal 9 (Severe Gale): {self.signal_thresholds['signal_9']} km/h")
        print(f"Signal 10 (Hurricane): {self.signal_thresholds['signal_10']} km/h")

def main():
    """Main execution function"""
    
    api = HKSpatialWindDataAPI()
    
    # Step 1: Fetch wind data
    wind_data = api.fetch_wind_data()
    
    if not wind_data:
        print("\n❌ Unable to fetch wind data from any source")
        print("🔍 Possible issues:")
        print("  • Network connectivity problems")
        print("  • API endpoints may have changed")
        print("  • Rate limiting or access restrictions")
        print("\n💡 Try again later or check Hong Kong Observatory website directly:")
        print("   https://www.hko.gov.hk")
        return
    
    # Step 2: Analyze Signal 8 probability
    analysis = api.analyze_signal_8_probability(wind_data)
    
    # Step 3: Generate report
    api.generate_report(wind_data, analysis)
    
    # Step 4: Save detailed results
    results = {
        'wind_data': wind_data,
        'analysis': analysis,
        'metadata': {
            'script_version': '1.0',
            'execution_time': datetime.now().isoformat(),
            'signal_thresholds': api.signal_thresholds
        }
    }
    
    filename = f"hk_wind_signal8_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed results saved to: {filename}")
    print(f"\n⚠️  IMPORTANT: This analysis is based on available API data.")
    print(f"Always check official Hong Kong Observatory sources for authoritative weather warnings!")
    print(f"🌐 Official HKO: https://www.hko.gov.hk")

if __name__ == "__main__":
    main()
