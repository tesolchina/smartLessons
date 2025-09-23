#!/usr/bin/env python3
"""
Hong Kong Wind Data Explorer
============================

This script explores available wind data from Hong Kong Observatory APIs
and analyzes whether wind conditions might reach Tropical Cyclone Signal 8 levels.

Signal 8 criteria:
- Sustained winds of 63-87 km/h (17-24 m/s) expected within Hong Kong
- Usually issued when winds reach 41-62 km/h with further strengthening expected

Author: GitHub Copilot
Date: September 7, 2025
"""

import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Optional
import time

class HKWindDataExplorer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        # Common HK Observatory API endpoints to try
        self.api_endpoints = [
            # Official HKO data endpoints
            'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en',
            'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=ltmv&lang=en',
            'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=en',
            'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warningInfo&lang=en',
            
            # RSS feeds
            'https://rss.weather.gov.hk/rss/CurrentWeather.xml',
            'https://rss.weather.gov.hk/rss/WeatherWarningBulletin.xml',
            
            # Alternative data sources
            'https://api.data.gov.hk/v1/historical-archive/get-file?url=https%3A%2F%2Fdata.weather.gov.hk%2FweatherAPI%2Fopendata%2Fweather.php%3FdataType%3Drhrread%26lang%3Den',
        ]
        
        self.wind_data = []
        self.current_warnings = []

    def fetch_data_from_endpoint(self, url: str) -> Optional[Dict]:
        """Fetch data from a given endpoint and return parsed JSON/XML"""
        try:
            print(f"Trying endpoint: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '').lower()
            
            if 'json' in content_type or url.endswith('.json'):
                data = response.json()
                print(f"✓ Successfully fetched JSON data from {url}")
                return {'type': 'json', 'data': data, 'url': url}
                
            elif 'xml' in content_type or url.endswith('.xml'):
                root = ET.fromstring(response.text)
                print(f"✓ Successfully fetched XML data from {url}")
                return {'type': 'xml', 'data': root, 'url': url}
                
            else:
                # Try to parse as JSON first
                try:
                    data = response.json()
                    print(f"✓ Successfully parsed as JSON: {url}")
                    return {'type': 'json', 'data': data, 'url': url}
                except:
                    print(f"? Unknown content type for {url}: {content_type}")
                    return {'type': 'text', 'data': response.text[:500], 'url': url}
                    
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed to fetch {url}: {e}")
            return None
        except Exception as e:
            print(f"✗ Error parsing {url}: {e}")
            return None

    def explore_all_endpoints(self) -> List[Dict]:
        """Explore all available endpoints and return successful responses"""
        successful_data = []
        
        print("=" * 60)
        print("EXPLORING HONG KONG OBSERVATORY WIND DATA APIS")
        print("=" * 60)
        
        for endpoint in self.api_endpoints:
            result = self.fetch_data_from_endpoint(endpoint)
            if result:
                successful_data.append(result)
            time.sleep(1)  # Be respectful to the API
            
        return successful_data

    def parse_wind_data(self, data_sources: List[Dict]) -> List[Dict]:
        """Parse wind data from successful API responses"""
        wind_readings = []
        
        for source in data_sources:
            try:
                if source['type'] == 'json':
                    wind_readings.extend(self._parse_json_wind_data(source))
                elif source['type'] == 'xml':
                    wind_readings.extend(self._parse_xml_wind_data(source))
                    
            except Exception as e:
                print(f"Error parsing wind data from {source['url']}: {e}")
                
        return wind_readings

    def _parse_json_wind_data(self, source: Dict) -> List[Dict]:
        """Parse wind data from JSON responses"""
        wind_data = []
        data = source['data']
        url = source['url']
        
        print(f"\nParsing JSON data from: {url}")
        
        # Handle different JSON structures
        if isinstance(data, dict):
            # Check for regional weather data
            if 'rainfall' in data and isinstance(data['rainfall'], list):
                for station in data['rainfall']:
                    if 'station' in station:
                        wind_info = {
                            'station': station['station'],
                            'source': url,
                            'timestamp': datetime.now().isoformat(),
                            'data_type': 'rainfall_station'
                        }
                        wind_data.append(wind_info)
                        
            # Check for weather warnings
            if 'warningMessage' in data:
                for warning in data.get('warningMessage', []):
                    if any(keyword in warning.get('name', '').lower() 
                          for keyword in ['wind', 'typhoon', 'hurricane', 'gale']):
                        wind_info = {
                            'warning': warning.get('name', ''),
                            'message': warning.get('text', ''),
                            'source': url,
                            'timestamp': datetime.now().isoformat(),
                            'data_type': 'wind_warning'
                        }
                        wind_data.append(wind_info)
                        
            # Check for temperature and wind in current weather
            if 'temperature' in data or 'humidity' in data:
                wind_info = {
                    'temperature': data.get('temperature'),
                    'humidity': data.get('humidity'),
                    'source': url,
                    'timestamp': datetime.now().isoformat(),
                    'data_type': 'current_weather'
                }
                # Look for wind-related fields
                for key in data:
                    if 'wind' in key.lower():
                        wind_info[key] = data[key]
                wind_data.append(wind_info)
                
        return wind_data

    def _parse_xml_wind_data(self, source: Dict) -> List[Dict]:
        """Parse wind data from XML responses"""
        wind_data = []
        root = source['data']
        url = source['url']
        
        print(f"\nParsing XML data from: {url}")
        
        # Parse RSS feeds
        if root.tag == 'rss' or 'rss' in str(root.tag).lower():
            for item in root.findall('.//item'):
                title = item.find('title')
                description = item.find('description')
                pubDate = item.find('pubDate')
                
                if title is not None:
                    title_text = title.text or ''
                    desc_text = description.text if description is not None else ''
                    
                    # Check if this is wind/weather related
                    if any(keyword in (title_text + desc_text).lower() 
                          for keyword in ['wind', 'typhoon', 'hurricane', 'gale', 'weather']):
                        
                        wind_info = {
                            'title': title_text,
                            'description': desc_text,
                            'pub_date': pubDate.text if pubDate is not None else '',
                            'source': url,
                            'timestamp': datetime.now().isoformat(),
                            'data_type': 'rss_weather'
                        }
                        wind_data.append(wind_info)
                        
        return wind_data

    def analyze_signal_8_risk(self, wind_data: List[Dict]) -> Dict:
        """Analyze if conditions might reach Signal 8 tomorrow morning"""
        
        print("\n" + "=" * 60)
        print("SIGNAL 8 RISK ANALYSIS")
        print("=" * 60)
        
        analysis = {
            'current_time': datetime.now().isoformat(),
            'target_time': (datetime.now() + timedelta(hours=12)).isoformat(),
            'signal_8_criteria': {
                'sustained_winds_kmh': [63, 87],
                'sustained_winds_ms': [17, 24],
                'warning_winds_kmh': [41, 62]
            },
            'risk_level': 'UNKNOWN',
            'risk_factors': [],
            'recommendations': []
        }
        
        # Analyze current warnings
        warnings_found = []
        wind_readings = []
        
        for data in wind_data:
            if data.get('data_type') == 'wind_warning':
                warnings_found.append(data)
                
            if 'wind' in str(data).lower():
                wind_readings.append(data)
        
        # Check for active typhoon/wind warnings
        if warnings_found:
            analysis['risk_factors'].append(f"Found {len(warnings_found)} wind-related warnings")
            analysis['risk_level'] = 'MODERATE'
            
            for warning in warnings_found:
                if any(term in warning.get('warning', '').lower() 
                      for term in ['typhoon', 'hurricane', 'strong wind']):
                    analysis['risk_level'] = 'HIGH'
                    analysis['risk_factors'].append(f"Active severe weather warning: {warning.get('warning')}")
        
        # If we have wind readings, analyze them
        if wind_readings:
            analysis['risk_factors'].append(f"Found {len(wind_readings)} wind-related data points")
        
        # Provide recommendations
        if analysis['risk_level'] == 'HIGH':
            analysis['recommendations'] = [
                "Monitor HKO warnings closely",
                "Prepare for possible Signal 8 issuance",
                "Secure loose objects and avoid outdoor activities",
                "Check public transport schedules"
            ]
        elif analysis['risk_level'] == 'MODERATE':
            analysis['recommendations'] = [
                "Stay updated with latest weather warnings",
                "Monitor wind conditions development",
                "Be prepared for changing conditions"
            ]
        else:
            analysis['recommendations'] = [
                "Continue monitoring weather conditions",
                "Check HKO official forecasts for updates"
            ]
            
        return analysis

    def display_results(self, wind_data: List[Dict], analysis: Dict):
        """Display the exploration results in a formatted way"""
        
        print("\n" + "=" * 60)
        print("WIND DATA EXPLORATION RESULTS")
        print("=" * 60)
        
        print(f"\nData Sources Found: {len(wind_data)}")
        print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Group data by type
        data_by_type = {}
        for data in wind_data:
            data_type = data.get('data_type', 'unknown')
            if data_type not in data_by_type:
                data_by_type[data_type] = []
            data_by_type[data_type].append(data)
        
        print(f"\nData Types Found:")
        for data_type, items in data_by_type.items():
            print(f"  - {data_type}: {len(items)} items")
        
        # Display sample data
        print(f"\nSample Data:")
        for i, data in enumerate(wind_data[:5]):  # Show first 5 items
            print(f"\n{i+1}. {data.get('data_type', 'unknown').upper()}")
            for key, value in data.items():
                if key not in ['source', 'timestamp', 'data_type']:
                    print(f"   {key}: {str(value)[:100]}...")
        
        # Display analysis
        print(f"\n" + "=" * 40)
        print("SIGNAL 8 RISK ASSESSMENT")
        print("=" * 40)
        print(f"Risk Level: {analysis['risk_level']}")
        print(f"Target Time: Tomorrow morning ({analysis['target_time'][:16]})")
        
        print(f"\nRisk Factors:")
        for factor in analysis['risk_factors']:
            print(f"  • {factor}")
            
        print(f"\nRecommendations:")
        for rec in analysis['recommendations']:
            print(f"  • {rec}")
            
        print(f"\nSignal 8 Criteria:")
        criteria = analysis['signal_8_criteria']
        print(f"  • Sustained winds: {criteria['sustained_winds_kmh'][0]}-{criteria['sustained_winds_kmh'][1]} km/h")
        print(f"  • Warning threshold: {criteria['warning_winds_kmh'][0]}-{criteria['warning_winds_kmh'][1]} km/h")

def main():
    """Main function to run the wind data exploration"""
    
    print("Hong Kong Wind Data Explorer")
    print("Analyzing wind conditions for Signal 8 assessment")
    print("=" * 60)
    
    explorer = HKWindDataExplorer()
    
    # Step 1: Explore all available endpoints
    successful_data = explorer.explore_all_endpoints()
    
    if not successful_data:
        print("\n❌ No data sources were accessible.")
        print("This might be due to:")
        print("  - Network connectivity issues")
        print("  - API endpoint changes")
        print("  - Rate limiting")
        print("\nTry running the script again later or check your internet connection.")
        return
    
    # Step 2: Parse wind-related data
    wind_data = explorer.parse_wind_data(successful_data)
    
    # Step 3: Analyze Signal 8 risk
    analysis = explorer.analyze_signal_8_risk(wind_data)
    
    # Step 4: Display results
    explorer.display_results(wind_data, analysis)
    
    # Step 5: Save results to file
    results = {
        'exploration_time': datetime.now().isoformat(),
        'wind_data': wind_data,
        'signal_8_analysis': analysis,
        'successful_endpoints': [data['url'] for data in successful_data]
    }
    
    with open('hk_wind_analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to 'hk_wind_analysis_results.json'")
    print(f"\n🌪️  Keep monitoring HKO official channels for the most up-to-date information!")

if __name__ == "__main__":
    main()
