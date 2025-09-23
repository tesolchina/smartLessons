#!/usr/bin/env python3
"""
Hong Kong Wind Data Consolidation Script - Final Version
========================================================

This script consolidates all successful methods to access Hong Kong wind data:
1. Real-time HKO APIs (working endpoints)
2. RSS feeds with wind information
3. Alternative data sources
4. Comprehensive analysis for Signal 8 assessment

Based on our testing, this provides the best available access to Hong Kong wind data
for monitoring Signal 8 conditions tomorrow morning.

Author: GitHub Copilot
Date: September 8, 2025
"""

import requests
import json
import time
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from bs4 import BeautifulSoup

class HKWindDataConsolidated:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json, application/xml, text/html, */*',
            'Accept-Language': 'en-US,en;q=0.9'
        })
        
        # Proven working endpoints from our testing
        self.working_endpoints = [
            {
                'url': 'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en',
                'type': 'json',
                'description': 'HKO Regional Hourly Weather',
                'priority': 1
            },
            {
                'url': 'https://rss.weather.gov.hk/rss/CurrentWeather.xml',
                'type': 'xml',
                'description': 'HKO Current Weather RSS',
                'priority': 1
            },
            {
                'url': 'https://rss.weather.gov.hk/rss/WeatherWarningBulletin.xml',
                'type': 'xml',
                'description': 'HKO Weather Warning RSS',
                'priority': 1
            },
            {
                'url': 'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=en',
                'type': 'json',
                'description': 'HKO 9-day Weather Forecast',
                'priority': 2
            },
            {
                'url': 'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warningInfo&lang=en',
                'type': 'json',
                'description': 'HKO Warning Information',
                'priority': 1
            }
        ]
        
        # Signal thresholds for quick reference
        self.signal_thresholds = {
            'signal_1': 22,   # Standby
            'signal_3': 41,   # Strong Wind
            'signal_8': 63,   # Gale or Storm
            'signal_9': 88,   # Increasing Gale
            'signal_10': 118  # Hurricane
        }

    def fetch_all_wind_data(self) -> Dict[str, Any]:
        """Fetch wind data from all working endpoints"""
        
        print("🌪️  Fetching consolidated Hong Kong wind data...")
        print("=" * 60)
        
        results = {
            'fetch_time': datetime.now().isoformat(),
            'successful_sources': [],
            'failed_sources': [],
            'wind_data': [],
            'current_warnings': [],
            'station_data': [],
            'forecast_data': []
        }
        
        # Sort endpoints by priority
        sorted_endpoints = sorted(self.working_endpoints, key=lambda x: x['priority'])
        
        for endpoint in sorted_endpoints:
            url = endpoint['url']
            endpoint_type = endpoint['type']
            description = endpoint['description']
            
            try:
                print(f"📡 {description}...")
                
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                if endpoint_type == 'json':
                    data = response.json()
                    parsed_data = self._parse_json_data(data, url, description)
                else:  # xml
                    parsed_data = self._parse_xml_data(response.text, url, description)
                
                if parsed_data:
                    results['successful_sources'].append({
                        'url': url,
                        'description': description,
                        'data_points': len(parsed_data)
                    })
                    
                    # Categorize data
                    for item in parsed_data:
                        if item.get('category') == 'warning':
                            results['current_warnings'].append(item)
                        elif item.get('category') == 'station_data':
                            results['station_data'].append(item)
                        elif item.get('category') == 'forecast':
                            results['forecast_data'].append(item)
                        else:
                            results['wind_data'].append(item)
                    
                    print(f"  ✅ Success: {len(parsed_data)} data points")
                else:
                    print(f"  ⚠️  No useful data extracted")
                    
            except Exception as e:
                results['failed_sources'].append({
                    'url': url,
                    'description': description,
                    'error': str(e)[:100]
                })
                print(f"  ❌ Failed: {str(e)[:50]}...")
                
            time.sleep(0.5)  # Rate limiting
        
        return results

    def _parse_json_data(self, data: dict, source: str, description: str) -> List[Dict[str, Any]]:
        """Parse JSON data from HKO APIs"""
        parsed_items = []
        
        # Handle regional weather data (rhrread)
        if 'rainfall' in data:
            for station in data.get('rainfall', []):
                if isinstance(station, dict) and 'station' in station:
                    item = {
                        'timestamp': datetime.now().isoformat(),
                        'source': source,
                        'description': description,
                        'category': 'station_data',
                        'station': station['station'],
                        'type': 'regional_weather'
                    }
                    
                    # Add all numeric data
                    for key, value in station.items():
                        if key != 'station' and isinstance(value, (int, float)):
                            item[key] = value
                    
                    parsed_items.append(item)
        
        # Handle warning information
        elif 'warningMessage' in data:
            for warning in data.get('warningMessage', []):
                if isinstance(warning, dict):
                    item = {
                        'timestamp': datetime.now().isoformat(),
                        'source': source,
                        'description': description,
                        'category': 'warning',
                        'warning_name': warning.get('name', ''),
                        'warning_message': warning.get('text', ''),
                        'type': 'official_warning'
                    }
                    parsed_items.append(item)
        
        # Handle forecast data
        elif 'weatherForecast' in data:
            forecasts = data.get('weatherForecast', [])
            if isinstance(forecasts, list):
                for forecast in forecasts:
                    if isinstance(forecast, dict):
                        item = {
                            'timestamp': datetime.now().isoformat(),
                            'source': source,
                            'description': description,
                            'category': 'forecast',
                            'type': 'weather_forecast'
                        }
                        item.update(forecast)
                        parsed_items.append(item)
        
        # Handle general data
        else:
            item: Dict[str, Any] = {
                'timestamp': datetime.now().isoformat(),
                'source': source,
                'description': description,
                'category': 'general',
                'type': 'json_data'
            }
            
            # Add relevant fields
            for key, value in data.items():
                if isinstance(value, (str, int, float, bool)):
                    item[key] = value
            
            if len(item) > 6:  # More than just metadata
                parsed_items.append(item)
        
        return parsed_items

    def _parse_xml_data(self, xml_text: str, source: str, description: str) -> List[Dict[str, Any]]:
        """Parse XML/RSS data"""
        parsed_items = []
        
        try:
            root = ET.fromstring(xml_text)
            
            # Handle RSS feeds
            for item in root.findall('.//item'):
                title = item.find('title')
                description_elem = item.find('description')
                pub_date = item.find('pubDate')
                
                if title is not None:
                    title_text = title.text or ''
                    desc_text = description_elem.text if description_elem is not None else ''
                    
                    parsed_item = {
                        'timestamp': datetime.now().isoformat(),
                        'source': source,
                        'description': description,
                        'category': 'rss_feed',
                        'title': title_text,
                        'content': desc_text[:500] if desc_text else '',  # Truncate long content
                        'pub_date': pub_date.text if pub_date is not None else '',
                        'type': 'rss_item'
                    }
                    
                    # Extract wind-related information
                    combined_text = title_text + (desc_text or '')
                    if 'wind' in combined_text.lower():
                        # Extract wind speeds
                        if desc_text:
                            speed_matches = re.findall(r'(\d+)(?:,\s*(\d+)\s*and\s*(\d+))?\s*kilometres per hour', desc_text)
                            if speed_matches:
                                speeds = []
                                for match in speed_matches:
                                    speeds.extend([int(s) for s in match if s])
                                parsed_item['extracted_wind_speeds'] = speeds
                                parsed_item['max_extracted_wind'] = max(speeds) if speeds else 0
                            
                            # Extract gust information
                            gust_matches = re.findall(r'maximum gusts exceeding (\d+)(?:,\s*(\d+)\s*and\s*(\d+))?\s*kilometres per hour', desc_text)
                            if gust_matches:
                                gusts = []
                                for match in gust_matches:
                                    gusts.extend([int(g) for g in match if g])
                                parsed_item['extracted_gust_speeds'] = gusts
                                parsed_item['max_extracted_gust'] = max(gusts) if gusts else 0
                            
                            # Extract station names
                            station_matches = re.findall(r'at ([A-Za-z\s]+?)(?:,|\s+were|\s+was)', desc_text)
                            if station_matches:
                                parsed_item['mentioned_stations'] = [s.strip() for s in station_matches]
                            
                            # Check for signal information
                            if 'Signal No.' in desc_text or 'Signal No.' in title_text:
                                signal_match = re.search(r'Signal No\. (\d+)', combined_text)
                                if signal_match:
                                    parsed_item['current_signal'] = int(signal_match.group(1))
                    
                    parsed_items.append(parsed_item)
                    
        except Exception as e:
            print(f"XML parsing error: {e}")
            
        return parsed_items

    def analyze_signal_8_conditions(self, consolidated_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive analysis for Signal 8 conditions tomorrow morning"""
        
        analysis = {
            'analysis_time': datetime.now().isoformat(),
            'data_summary': {
                'total_sources': len(consolidated_data['successful_sources']),
                'total_data_points': len(consolidated_data['wind_data']) + 
                                   len(consolidated_data['current_warnings']) +
                                   len(consolidated_data['station_data']),
                'warning_count': len(consolidated_data['current_warnings']),
                'station_count': len(consolidated_data['station_data'])
            },
            'current_signal_status': None,
            'wind_measurements': {
                'extracted_speeds': [],
                'extracted_gusts': [],
                'max_speed': 0,
                'max_gust': 0
            },
            'tomorrow_morning_forecast': {
                'signal_8_probability': 'UNKNOWN',
                'risk_level': 'UNKNOWN',
                'key_factors': []
            },
            'official_warnings': [],
            'monitoring_stations': []
        }
        
        # Analyze current warnings
        for warning in consolidated_data['current_warnings']:
            warning_name = warning.get('warning_name', '')
            warning_message = warning.get('warning_message', '')
            
            analysis['official_warnings'].append({
                'name': warning_name,
                'severity': self._assess_warning_severity(warning_name, warning_message)
            })
        
        # Extract wind measurements from all sources
        all_items = (consolidated_data['wind_data'] + 
                    consolidated_data['current_warnings'] +
                    consolidated_data['station_data'])
        
        for item in all_items:
            # Extract speeds from RSS content
            if 'extracted_wind_speeds' in item:
                analysis['wind_measurements']['extracted_speeds'].extend(item['extracted_wind_speeds'])
            if 'extracted_gust_speeds' in item:
                analysis['wind_measurements']['extracted_gusts'].extend(item['extracted_gust_speeds'])
            
            # Check for current signal status
            if 'current_signal' in item:
                analysis['current_signal_status'] = item['current_signal']
            
            # Collect station information
            if 'station' in item:
                station_info = {
                    'name': item['station'],
                    'source': item.get('description', 'Unknown')
                }
                if station_info not in analysis['monitoring_stations']:
                    analysis['monitoring_stations'].append(station_info)
            
            if 'mentioned_stations' in item:
                for station in item['mentioned_stations']:
                    station_info = {
                        'name': station,
                        'source': item.get('description', 'RSS feed')
                    }
                    if station_info not in analysis['monitoring_stations']:
                        analysis['monitoring_stations'].append(station_info)
        
        # Calculate wind statistics
        speeds = analysis['wind_measurements']['extracted_speeds']
        gusts = analysis['wind_measurements']['extracted_gusts']
        
        if speeds:
            analysis['wind_measurements']['max_speed'] = max(speeds)
            analysis['wind_measurements']['avg_speed'] = sum(speeds) / len(speeds)
            analysis['wind_measurements']['speed_count'] = len(speeds)
        
        if gusts:
            analysis['wind_measurements']['max_gust'] = max(gusts)
            analysis['wind_measurements']['avg_gust'] = sum(gusts) / len(gusts)
            analysis['wind_measurements']['gust_count'] = len(gusts)
        
        # Tomorrow morning assessment
        max_wind = analysis['wind_measurements']['max_speed']
        max_gust = analysis['wind_measurements']['max_gust']
        current_signal = analysis['current_signal_status']
        
        # Determine probability based on current conditions
        if current_signal and current_signal >= 8:
            analysis['tomorrow_morning_forecast']['signal_8_probability'] = 'HIGH'
            analysis['tomorrow_morning_forecast']['risk_level'] = 'HIGH RISK'
            analysis['tomorrow_morning_forecast']['key_factors'].append(f"Signal {current_signal} currently in force")
        
        elif max_wind >= 63 or max_gust >= 63:
            analysis['tomorrow_morning_forecast']['signal_8_probability'] = 'HIGH'
            analysis['tomorrow_morning_forecast']['risk_level'] = 'HIGH RISK'
            analysis['tomorrow_morning_forecast']['key_factors'].append(f"Wind speeds at Signal 8 level: {max_wind} km/h")
        
        elif max_wind >= 41 or max_gust >= 41:
            analysis['tomorrow_morning_forecast']['signal_8_probability'] = 'MODERATE'
            analysis['tomorrow_morning_forecast']['risk_level'] = 'MODERATE RISK'
            analysis['tomorrow_morning_forecast']['key_factors'].append(f"Strong winds detected: {max_wind} km/h")
        
        elif max_wind > 0:
            analysis['tomorrow_morning_forecast']['signal_8_probability'] = 'LOW'
            analysis['tomorrow_morning_forecast']['risk_level'] = 'LOW RISK'
            analysis['tomorrow_morning_forecast']['key_factors'].append(f"Light winds: {max_wind} km/h")
        
        else:
            analysis['tomorrow_morning_forecast']['signal_8_probability'] = 'UNKNOWN'
            analysis['tomorrow_morning_forecast']['risk_level'] = 'UNKNOWN'
            analysis['tomorrow_morning_forecast']['key_factors'].append("Insufficient wind measurement data")
        
        # Add contextual factors
        if len(analysis['official_warnings']) > 0:
            analysis['tomorrow_morning_forecast']['key_factors'].append(f"{len(analysis['official_warnings'])} official weather warnings active")
        
        if len(analysis['monitoring_stations']) > 10:
            analysis['tomorrow_morning_forecast']['key_factors'].append("Comprehensive station coverage available")
        elif len(analysis['monitoring_stations']) < 5:
            analysis['tomorrow_morning_forecast']['key_factors'].append("Limited station coverage - assessment may be incomplete")
        
        return analysis

    def _assess_warning_severity(self, warning_name: str, warning_message: str) -> str:
        """Assess the severity of weather warnings"""
        combined_text = (warning_name + ' ' + warning_message).lower()
        
        if any(term in combined_text for term in ['typhoon', 'hurricane', 'signal', 'storm']):
            return 'HIGH'
        elif any(term in combined_text for term in ['strong wind', 'gale', 'heavy rain']):
            return 'MODERATE'
        else:
            return 'LOW'

    def generate_final_report(self, consolidated_data: Dict[str, Any], analysis: Dict[str, Any]):
        """Generate the final comprehensive report"""
        
        print(f"\n" + "🌪️ " * 30)
        print("HONG KONG WIND CONDITIONS - FINAL CONSOLIDATED REPORT")
        print(f"Tomorrow Morning Assessment • {datetime.now().strftime('%H:%M HKT, %B %d, %Y')}")
        print("🌪️ " * 30)
        
        # Data sources summary
        print(f"\n📊 DATA SOURCES SUMMARY")
        print("=" * 30)
        print(f"Successful Sources: {analysis['data_summary']['total_sources']}")
        print(f"Total Data Points: {analysis['data_summary']['total_data_points']}")
        print(f"Active Warnings: {analysis['data_summary']['warning_count']}")
        print(f"Monitoring Stations: {analysis['data_summary']['station_count']}")
        
        print(f"\nData Source Details:")
        for source in consolidated_data['successful_sources']:
            print(f"  ✅ {source['description']}: {source['data_points']} points")
        
        if consolidated_data['failed_sources']:
            print(f"\nUnavailable Sources:")
            for source in consolidated_data['failed_sources']:
                print(f"  ❌ {source['description']}")
        
        # Current signal status
        print(f"\n🚨 CURRENT SIGNAL STATUS")
        print("=" * 30)
        if analysis['current_signal_status']:
            signal_num = analysis['current_signal_status']
            print(f"SIGNAL {signal_num} IS IN FORCE")
            if signal_num >= 8:
                print("🚨 GALE OR STORM SIGNAL ACTIVE")
            elif signal_num >= 3:
                print("⚠️  STRONG WIND SIGNAL ACTIVE")
        else:
            print("No current signal information available")
        
        # Wind measurements
        wind_data = analysis['wind_measurements']
        print(f"\n💨 WIND MEASUREMENTS")
        print("=" * 25)
        
        if wind_data['max_speed'] > 0:
            print(f"Maximum Wind Speed: {wind_data['max_speed']} km/h")
            if 'avg_speed' in wind_data:
                print(f"Average Wind Speed: {wind_data['avg_speed']:.1f} km/h")
            print(f"Wind Readings: {wind_data.get('speed_count', 0)}")
        else:
            print("No quantitative wind speed data available")
        
        if wind_data['max_gust'] > 0:
            print(f"Maximum Gust: {wind_data['max_gust']} km/h")
            if 'avg_gust' in wind_data:
                print(f"Average Gust: {wind_data['avg_gust']:.1f} km/h")
            print(f"Gust Readings: {wind_data.get('gust_count', 0)}")
        
        # Tomorrow morning forecast
        forecast = analysis['tomorrow_morning_forecast']
        print(f"\n🌅 TOMORROW MORNING FORECAST")
        print("=" * 35)
        print(f"Signal 8 Probability: {forecast['signal_8_probability']}")
        print(f"Risk Level: {forecast['risk_level']}")
        
        print(f"Key Assessment Factors:")
        for factor in forecast['key_factors']:
            print(f"  • {factor}")
        
        # Official warnings
        if analysis['official_warnings']:
            print(f"\n⚠️  OFFICIAL WARNINGS")
            print("=" * 22)
            for warning in analysis['official_warnings']:
                severity_emoji = "🚨" if warning['severity'] == 'HIGH' else "⚠️" if warning['severity'] == 'MODERATE' else "ℹ️"
                print(f"{severity_emoji} {warning['name']}")
        
        # Monitoring stations
        if analysis['monitoring_stations']:
            print(f"\n🏢 MONITORING STATIONS")
            print("=" * 25)
            print(f"Total Stations: {len(analysis['monitoring_stations'])}")
            
            # Group by source
            by_source = {}
            for station in analysis['monitoring_stations']:
                source = station['source']
                if source not in by_source:
                    by_source[source] = []
                by_source[source].append(station['name'])
            
            for source, stations in by_source.items():
                print(f"{source}: {len(stations)} stations")
                if len(stations) <= 5:
                    for station in stations:
                        print(f"  • {station}")
                else:
                    for station in stations[:3]:
                        print(f"  • {station}")
                    print(f"  • ... and {len(stations) - 3} more")
        
        # Action recommendations
        print(f"\n🎯 TOMORROW MORNING RECOMMENDATIONS")
        print("=" * 40)
        
        probability = forecast['signal_8_probability']
        
        if probability == 'HIGH':
            recommendations = [
                "🚨 STAY HOME - Signal 8 conditions likely to continue",
                "🚌 Public transport will be suspended",
                "💼 Work and schools will be cancelled",
                "🏪 Most businesses will be closed",
                "📱 Monitor HKO updates every 30 minutes",
                "⚡ Keep devices charged, prepare for power outages"
            ]
        elif probability == 'MODERATE':
            recommendations = [
                "⚠️  Check Signal status before leaving home",
                "🚌 Monitor public transport announcements closely",
                "💼 Confirm work/school arrangements with employers",
                "📱 Check HKO updates every hour",
                "🎒 Prepare to return home quickly if conditions worsen"
            ]
        elif probability == 'LOW':
            recommendations = [
                "✅ Conditions appear manageable for tomorrow",
                "📱 Monitor weather updates regularly",
                "🚌 Check transport status before travel",
                "⚠️  Remain alert for changing conditions"
            ]
        else:
            recommendations = [
                "❓ Limited data available for reliable assessment",
                "📱 Monitor official HKO channels continuously",
                "🔍 Check multiple weather sources",
                "⚠️  Err on the side of caution"
            ]
        
        for i, rec in enumerate(recommendations, 1):
            print(f"{i:2d}. {rec}")
        
        # Signal reference
        print(f"\n📋 SIGNAL REFERENCE")
        print("=" * 20)
        for signal, speed in self.signal_thresholds.items():
            signal_name = signal.replace('_', ' ').title()
            print(f"{signal_name}: {speed}+ km/h")
        
        # Next steps
        print(f"\n🔗 IMMEDIATE NEXT STEPS")
        print("=" * 25)
        print("1. 📱 Official HKO: https://www.hko.gov.hk")
        print("2. 📱 HKO MyObservatory App")
        print("3. ☎️  HKO Hotline: 1878 200")
        print("4. 🚨 Emergency: 999")
        print("5. 🔄 Re-run this analysis in 1-2 hours")
        
        print(f"\n" + "🌪️ " * 30)
        print("⚠️  FINAL REMINDER: Always prioritize official HKO announcements")
        print("🌪️ " * 30)

def main():
    """Main execution function"""
    
    consolidator = HKWindDataConsolidated()
    
    print("🚀 Hong Kong Wind Data - Final Consolidated Analysis")
    print("Comprehensive assessment for Signal 8 conditions tomorrow morning")
    print("=" * 75)
    
    # Step 1: Fetch all available wind data
    consolidated_data = consolidator.fetch_all_wind_data()
    
    # Step 2: Analyze Signal 8 conditions
    analysis = consolidator.analyze_signal_8_conditions(consolidated_data)
    
    # Step 3: Generate final report
    consolidator.generate_final_report(consolidated_data, analysis)
    
    # Step 4: Save comprehensive results
    final_results = {
        'consolidation_time': datetime.now().isoformat(),
        'consolidated_data': consolidated_data,
        'signal_8_analysis': analysis,
        'metadata': {
            'script_version': 'Final v1.0',
            'purpose': 'Signal 8 assessment for tomorrow morning',
            'data_sources': 'Multiple HKO APIs and RSS feeds',
            'update_frequency': 'Run every 1-2 hours for monitoring'
        }
    }
    
    filename = f"hk_wind_final_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Complete analysis saved to: {filename}")
    print(f"🕐 Recommended update interval: Every 1-2 hours")
    print(f"📅 Next assessment: {(datetime.now() + timedelta(hours=1)).strftime('%H:%M HKT')}")

if __name__ == "__main__":
    main()
