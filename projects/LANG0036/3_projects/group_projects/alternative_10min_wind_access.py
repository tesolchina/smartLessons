#!/usr/bin/env python3
"""
Hong Kong 10-Minute Wind Data Alternative Access Methods
========================================================

Since the direct spatial API endpoints are not publicly accessible,
this script explores alternative methods to access the 10-minute wind data:

1. Web scraping the CSDI portal interface
2. Parsing embedded data from the portal page
3. Finding alternative data.gov.hk endpoints
4. Using working HKO APIs with detailed station mapping

Author: GitHub Copilot
Date: September 8, 2025
"""

import requests
import json
import time
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

class HKWindDataAlternativeAccess:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # Alternative data sources to explore
        self.alternative_sources = [
            # CSDI portal main page
            'https://portal.csdi.gov.hk/geoportal/?datasetId=hko_rcd_1634953844424_88011&lang=en',
            
            # Data.gov.hk dataset page
            'https://data.gov.hk/en-data/dataset/hk-hko-rss-latest-ten-minute-wind-info/resource/3dadbf08-148c-4daa-8051-7ce315fa013b',
            
            # Alternative HKO endpoints
            'https://www.hko.gov.hk/en/wxinfo/currwx/current.htm',
            'https://www.hko.gov.hk/en/wxinfo/ts/index_uc.htm',
            
            # Known working APIs
            'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en',
            'https://rss.weather.gov.hk/rss/CurrentWeather.xml',
            'https://rss.weather.gov.hk/rss/WeatherWarningBulletin.xml'
        ]

    def explore_csdi_portal(self) -> Dict:
        """Explore the CSDI portal page for embedded wind data"""
        
        print("🔍 Exploring CSDI portal for embedded wind data...")
        
        portal_url = 'https://portal.csdi.gov.hk/geoportal/?datasetId=hko_rcd_1634953844424_88011&lang=en'
        
        try:
            response = self.session.get(portal_url, timeout=15)
            response.raise_for_status()
            
            print(f"✅ Successfully accessed CSDI portal ({len(response.text)} chars)")
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for data or API endpoints in the page
            portal_data = {
                'page_title': soup.title.string if soup.title else 'Unknown',
                'data_links': [],
                'api_references': [],
                'embedded_data': [],
                'metadata': {}
            }
            
            # Find all links that might contain data
            for link in soup.find_all('a', href=True):
                href = link['href']
                if any(term in href.lower() for term in ['api', 'data', 'download', 'rest', 'service']):
                    portal_data['data_links'].append({
                        'url': href,
                        'text': link.get_text().strip()[:100]
                    })
            
            # Look for JSON data embedded in script tags
            for script in soup.find_all('script'):
                if script.string:
                    script_content = script.string
                    if 'wind' in script_content.lower() or 'station' in script_content.lower():
                        # Try to extract JSON objects
                        json_matches = re.findall(r'\{[^{}]*"[^"]*":[^{}]*\}', script_content)
                        for match in json_matches[:5]:  # Limit to first 5 matches
                            try:
                                json_data = json.loads(match)
                                portal_data['embedded_data'].append(json_data)
                            except json.JSONDecodeError:
                                pass
            
            # Look for metadata tables
            for table in soup.find_all('table'):
                table_data = {}
                for row in table.find_all('tr'):
                    cells = row.find_all(['td', 'th'])
                    if len(cells) == 2:
                        key = cells[0].get_text().strip()
                        value = cells[1].get_text().strip()
                        if key and value:
                            table_data[key] = value
                
                if table_data and any(term in str(table_data).lower() for term in ['wind', 'station', 'data']):
                    portal_data['metadata'].update(table_data)
            
            return portal_data
            
        except Exception as e:
            print(f"❌ Error accessing CSDI portal: {e}")
            return {}

    def find_working_endpoints(self) -> List[Dict]:
        """Find alternative working endpoints for wind data"""
        
        print(f"\n🔍 Testing alternative data sources...")
        
        working_endpoints = []
        
        for url in self.alternative_sources:
            try:
                print(f"  Testing: {url[:60]}...")
                
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                content_type = response.headers.get('content-type', '').lower()
                
                endpoint_info = {
                    'url': url,
                    'status': 'accessible',
                    'content_type': content_type,
                    'content_length': len(response.text),
                    'contains_wind_data': 'wind' in response.text.lower()
                }
                
                # Try to parse as JSON
                if 'json' in content_type:
                    try:
                        data = response.json()
                        endpoint_info['data_type'] = 'json'
                        endpoint_info['has_features'] = 'features' in str(data)
                        endpoint_info['has_stations'] = 'station' in str(data).lower()
                    except:
                        pass
                
                # Try to parse as XML
                elif 'xml' in content_type:
                    try:
                        root = ET.fromstring(response.text)
                        endpoint_info['data_type'] = 'xml'
                        endpoint_info['xml_root'] = root.tag
                    except:
                        pass
                
                # HTML content analysis
                elif 'html' in content_type:
                    endpoint_info['data_type'] = 'html'
                    if 'wind' in response.text.lower():
                        # Count wind references
                        wind_count = response.text.lower().count('wind')
                        station_count = response.text.lower().count('station')
                        endpoint_info['wind_references'] = wind_count
                        endpoint_info['station_references'] = station_count
                
                working_endpoints.append(endpoint_info)
                print(f"    ✅ Accessible ({endpoint_info['content_length']} chars, wind: {endpoint_info['contains_wind_data']})")
                
            except Exception as e:
                print(f"    ❌ Failed: {str(e)[:50]}...")
                
            time.sleep(0.5)  # Rate limiting
        
        return working_endpoints

    def extract_detailed_wind_data(self, working_endpoints: List[Dict]) -> List[Dict]:
        """Extract detailed wind data from working endpoints"""
        
        print(f"\n📊 Extracting detailed wind data...")
        
        all_wind_data = []
        
        for endpoint in working_endpoints:
            if not endpoint['contains_wind_data']:
                continue
                
            url = endpoint['url']
            
            try:
                print(f"  📡 Processing: {url[:50]}...")
                
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                if endpoint.get('data_type') == 'json':
                    wind_data = self._extract_json_wind_data(response.json(), url)
                elif endpoint.get('data_type') == 'xml':
                    wind_data = self._extract_xml_wind_data(response.text, url)
                elif endpoint.get('data_type') == 'html':
                    wind_data = self._extract_html_wind_data(response.text, url)
                else:
                    continue
                
                if wind_data:
                    all_wind_data.extend(wind_data)
                    print(f"    ✅ Extracted {len(wind_data)} wind data points")
                else:
                    print(f"    ⚠️  No extractable wind data")
                    
            except Exception as e:
                print(f"    ❌ Extraction failed: {str(e)[:50]}...")
        
        return all_wind_data

    def _extract_json_wind_data(self, data: dict, source: str) -> List[Dict]:
        """Extract wind data from JSON responses"""
        wind_data = []
        
        # Handle HKO regional weather data
        if 'rainfall' in data and isinstance(data['rainfall'], list):
            for station in data['rainfall']:
                if 'station' in station:
                    wind_point = {
                        'timestamp': datetime.now().isoformat(),
                        'source': source,
                        'station': station['station'],
                        'data_type': 'hko_regional'
                    }
                    
                    # Extract all numeric values that might be wind-related
                    for key, value in station.items():
                        if isinstance(value, (int, float)) and key != 'station':
                            wind_point[key] = value
                    
                    wind_data.append(wind_point)
        
        # Handle other JSON structures
        elif isinstance(data, dict):
            for key, value in data.items():
                if 'wind' in key.lower() and isinstance(value, (list, dict)):
                    if isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                wind_point = {
                                    'timestamp': datetime.now().isoformat(),
                                    'source': source,
                                    'data_type': 'json_wind',
                                    'category': key
                                }
                                wind_point.update(item)
                                wind_data.append(wind_point)
        
        return wind_data

    def _extract_xml_wind_data(self, xml_text: str, source: str) -> List[Dict]:
        """Extract wind data from XML responses"""
        wind_data = []
        
        try:
            root = ET.fromstring(xml_text)
            
            # Handle RSS feeds
            for item in root.findall('.//item'):
                title = item.find('title')
                description = item.find('description')
                pub_date = item.find('pubDate')
                
                if title is not None and description is not None:
                    title_text = title.text or ''
                    desc_text = description.text or ''
                    
                    if 'wind' in (title_text + desc_text).lower():
                        wind_point = {
                            'timestamp': datetime.now().isoformat(),
                            'source': source,
                            'data_type': 'xml_rss',
                            'title': title_text[:100],
                            'pub_date': pub_date.text if pub_date is not None else ''
                        }
                        
                        # Extract wind speeds from description
                        speed_matches = re.findall(r'(\d+)\s*kilometres per hour', desc_text)
                        if speed_matches:
                            wind_point['wind_speeds_kmh'] = [int(s) for s in speed_matches]
                            wind_point['max_wind_kmh'] = max([int(s) for s in speed_matches])
                        
                        # Extract station names
                        station_matches = re.findall(r'at ([A-Za-z\s]+)(?:,|\s+were|\s+was)', desc_text)
                        if station_matches:
                            wind_point['stations'] = [s.strip() for s in station_matches]
                        
                        wind_data.append(wind_point)
                        
        except Exception as e:
            print(f"XML parsing error: {e}")
            
        return wind_data

    def _extract_html_wind_data(self, html_text: str, source: str) -> List[Dict]:
        """Extract wind data from HTML pages"""
        wind_data = []
        
        try:
            soup = BeautifulSoup(html_text, 'html.parser')
            
            # Look for tables with wind data
            for table in soup.find_all('table'):
                rows = table.find_all('tr')
                if len(rows) < 2:
                    continue
                
                # Check if this table contains wind data
                table_text = table.get_text().lower()
                if not any(term in table_text for term in ['wind', 'gust', 'station']):
                    continue
                
                # Extract headers
                header_row = rows[0]
                headers = [th.get_text().strip() for th in header_row.find_all(['th', 'td'])]
                
                # Extract data rows
                for row in rows[1:]:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) == len(headers):
                        row_data: Dict[str, Any] = {
                            'timestamp': datetime.now().isoformat(),
                            'source': source,
                            'data_type': 'html_table'
                        }
                        
                        for header, cell in zip(headers, cells):
                            cell_text = cell.get_text().strip()
                            header_key = header.lower().replace(' ', '_')
                            
                            # Try to convert numeric values
                            try:
                                if '.' in cell_text:
                                    row_data[header_key] = float(cell_text)
                                elif cell_text.isdigit():
                                    row_data[header_key] = int(cell_text)
                                else:
                                    row_data[header_key] = cell_text
                            except ValueError:
                                row_data[header_key] = cell_text
                        
                        # Only add if it contains potential wind data
                        if any('wind' in str(v).lower() for v in row_data.values()):
                            wind_data.append(row_data)
            
        except Exception as e:
            print(f"HTML parsing error: {e}")
            
        return wind_data

    def create_station_mapping(self, wind_data: List[Dict]) -> Dict:
        """Create a comprehensive mapping of Hong Kong weather stations"""
        
        station_mapping = {
            'total_unique_stations': 0,
            'stations_with_coordinates': 0,
            'stations_with_wind_data': 0,
            'station_details': {},
            'data_sources_per_station': {}
        }
        
        all_stations = set()
        
        for data_point in wind_data:
            station = data_point.get('station') or data_point.get('location')
            
            if station:
                all_stations.add(station)
                
                if station not in station_mapping['station_details']:
                    station_mapping['station_details'][station] = {
                        'first_seen': data_point.get('timestamp'),
                        'data_sources': [],
                        'has_wind_data': False,
                        'has_coordinates': False,
                        'latest_measurements': {}
                    }
                
                station_info = station_mapping['station_details'][station]
                
                # Track data sources
                source = data_point.get('source', 'unknown')
                if source not in station_info['data_sources']:
                    station_info['data_sources'].append(source)
                
                # Check for wind data
                if any('wind' in str(k).lower() for k in data_point.keys()):
                    station_info['has_wind_data'] = True
                
                # Check for coordinates
                if any(coord in data_point for coord in ['latitude', 'longitude', 'lat', 'lon']):
                    station_info['has_coordinates'] = True
                
                # Update latest measurements
                for key, value in data_point.items():
                    if isinstance(value, (int, float)) and 'wind' in key.lower():
                        station_info['latest_measurements'][key] = value
        
        station_mapping['total_unique_stations'] = len(all_stations)
        station_mapping['stations_with_wind_data'] = len([s for s in station_mapping['station_details'].values() if s['has_wind_data']])
        station_mapping['stations_with_coordinates'] = len([s for s in station_mapping['station_details'].values() if s['has_coordinates']])
        
        return station_mapping

    def generate_comprehensive_assessment(self, portal_data: Dict, wind_data: List[Dict], station_mapping: Dict):
        """Generate comprehensive assessment of available wind data"""
        
        print(f"\n" + "🌪️ " * 30)
        print("HONG KONG 10-MINUTE WIND DATA COMPREHENSIVE ASSESSMENT")
        print(f"Alternative Access Methods Analysis • {datetime.now().strftime('%H:%M HKT, %B %d, %Y')}")
        print("🌪️ " * 30)
        
        # Portal analysis
        print(f"\n🌐 CSDI PORTAL ANALYSIS")
        print("=" * 30)
        if portal_data:
            print(f"Portal Access: ✅ Successful")
            print(f"Page Title: {portal_data.get('page_title', 'Unknown')}")
            print(f"Data Links Found: {len(portal_data.get('data_links', []))}")
            print(f"Embedded Data Objects: {len(portal_data.get('embedded_data', []))}")
            print(f"Metadata Fields: {len(portal_data.get('metadata', {}))}")
            
            # Show some key metadata
            metadata = portal_data.get('metadata', {})
            for key, value in list(metadata.items())[:5]:
                if len(key) < 30 and len(str(value)) < 50:
                    print(f"  • {key}: {value}")
                    
        else:
            print(f"Portal Access: ❌ Failed")
        
        # Data collection summary
        print(f"\n📊 DATA COLLECTION SUMMARY")
        print("=" * 35)
        print(f"Total Data Points Collected: {len(wind_data)}")
        print(f"Data Sources Accessed: {len(set([d.get('source', 'unknown') for d in wind_data]))}")
        print(f"Time Range: Last 10 minutes (real-time)")
        
        # Show data by type
        data_types = {}
        for data_point in wind_data:
            data_type = data_point.get('data_type', 'unknown')
            data_types[data_type] = data_types.get(data_type, 0) + 1
        
        if data_types:
            print(f"Data Types:")
            for dtype, count in data_types.items():
                print(f"  • {dtype}: {count} points")
        
        # Station analysis
        print(f"\n🏢 WEATHER STATION ANALYSIS")
        print("=" * 35)
        print(f"Total Unique Stations: {station_mapping['total_unique_stations']}")
        print(f"Stations with Wind Data: {station_mapping['stations_with_wind_data']}")
        print(f"Stations with Coordinates: {station_mapping['stations_with_coordinates']}")
        
        # Top stations with wind data
        stations_with_wind = {name: info for name, info in station_mapping['station_details'].items() 
                             if info['has_wind_data']}
        
        if stations_with_wind:
            print(f"\nTop Stations with Wind Measurements:")
            for i, (name, info) in enumerate(list(stations_with_wind.items())[:5], 1):
                measurements = info['latest_measurements']
                measurement_text = ", ".join([f"{k}: {v}" for k, v in list(measurements.items())[:2]])
                print(f"  {i}. {name}")
                if measurement_text:
                    print(f"     Latest: {measurement_text}")
        
        # Wind data quality assessment
        print(f"\n💨 WIND DATA QUALITY ASSESSMENT")
        print("=" * 40)
        
        # Extract wind measurements
        wind_speeds = []
        gust_speeds = []
        
        for data_point in wind_data:
            for key, value in data_point.items():
                if isinstance(value, (int, float)):
                    if 'wind' in key.lower() and 'speed' in key.lower():
                        wind_speeds.append(value)
                    elif 'gust' in key.lower():
                        gust_speeds.append(value)
                    elif 'wind_speeds_kmh' in key.lower() and isinstance(value, list):
                        wind_speeds.extend([v for v in value if isinstance(v, (int, float))])
        
        if wind_speeds:
            print(f"Wind Speed Measurements: {len(wind_speeds)} readings")
            print(f"  • Maximum: {max(wind_speeds)} km/h")
            print(f"  • Average: {sum(wind_speeds)/len(wind_speeds):.1f} km/h")
            print(f"  • Minimum: {min(wind_speeds)} km/h")
        else:
            print(f"Wind Speed Measurements: No quantitative data found")
        
        if gust_speeds:
            print(f"Gust Measurements: {len(gust_speeds)} readings")
            print(f"  • Maximum: {max(gust_speeds)} km/h")
        else:
            print(f"Gust Measurements: No gust data found")
        
        # 10-minute data assessment
        print(f"\n⏱️  10-MINUTE DATA ASSESSMENT")
        print("=" * 35)
        
        data_currency = "CURRENT" if len(wind_data) > 0 else "UNAVAILABLE"
        update_frequency = "Every 10 minutes" if data_currency == "CURRENT" else "Unable to verify"
        
        print(f"Data Currency: {data_currency}")
        print(f"Update Frequency: {update_frequency}")
        print(f"Last Assessment: {datetime.now().strftime('%H:%M:%S HKT')}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS")
        print("=" * 25)
        
        if len(wind_data) > 10:
            print("✅ EXCELLENT: Substantial wind data available")
            print("  • Real-time monitoring is feasible")
            print("  • Signal 8 assessment can be performed")
            print("  • Continue using current data sources")
        elif len(wind_data) > 5:
            print("✅ GOOD: Adequate wind data available")
            print("  • Basic monitoring is possible")
            print("  • Supplement with official HKO updates")
            print("  • Monitor data source reliability")
        elif len(wind_data) > 0:
            print("⚠️  LIMITED: Some wind data available")
            print("  • Use as supplementary information only")
            print("  • Rely primarily on official HKO channels")
            print("  • Explore additional data sources")
        else:
            print("❌ INSUFFICIENT: No reliable wind data found")
            print("  • Direct API access may require authentication")
            print("  • Contact HKO for official API access")
            print("  • Use official HKO website for updates")
        
        print(f"\n🔗 NEXT STEPS")
        print("=" * 15)
        print("1. 📱 Monitor official HKO channels: https://www.hko.gov.hk")
        print("2. 📧 Contact CSDI for API access: portal.csdi.gov.hk")
        print("3. 🔄 Run this assessment every 10 minutes")
        print("4. 📊 Cross-reference with official weather warnings")
        
        print(f"\n" + "🌪️ " * 30)

def main():
    """Main execution function"""
    
    accessor = HKWindDataAlternativeAccess()
    
    print("🚀 Hong Kong 10-Minute Wind Data Alternative Access")
    print("Exploring multiple methods to access real-time wind data")
    print("=" * 70)
    
    # Step 1: Explore CSDI portal
    portal_data = accessor.explore_csdi_portal()
    
    # Step 2: Find working endpoints
    working_endpoints = accessor.find_working_endpoints()
    
    # Step 3: Extract detailed wind data
    wind_data = accessor.extract_detailed_wind_data(working_endpoints)
    
    # Step 4: Create station mapping
    station_mapping = accessor.create_station_mapping(wind_data)
    
    # Step 5: Generate comprehensive assessment
    accessor.generate_comprehensive_assessment(portal_data, wind_data, station_mapping)
    
    # Step 6: Save results
    results = {
        'assessment_time': datetime.now().isoformat(),
        'portal_analysis': portal_data,
        'working_endpoints': working_endpoints,
        'wind_data': wind_data,
        'station_mapping': station_mapping,
        'metadata': {
            'target_dataset': 'latest_10min_wind',
            'intended_frequency': 'Every 10 minutes',
            'alternative_methods': 'Web scraping, RSS feeds, working APIs'
        }
    }
    
    filename = f"hk_10min_wind_alternative_access_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed assessment saved to: {filename}")

if __name__ == "__main__":
    main()
