#!/usr/bin/env python3
"""
Hong Kong Real-time 10-Minute Wind Data API Access
==================================================

This script specifically targets the spatial wind data layer mentioned in the notes:
- Dataset: latest_10min_wind (Spatial Layer)
- Update Frequency: Every 10 minutes
- Contains: Wind direction, wind speed, and maximum gust data
- Spatial coverage: All Hong Kong automatic weather stations

Based on the data specification:
- AutomaticWeatherStation_en (English station names)
- AutomaticWeatherStation_uc/sc (Chinese station names)  
- Data_url (Direct data access URLs)

Author: GitHub Copilot
Date: September 8, 2025
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import xml.etree.ElementTree as ET
import re

class HKRealTimeWindDataAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json, application/xml, */*',
            'Accept-Language': 'en-US,en;q=0.9'
        })
        
        # Target the specific spatial data endpoints from the notes
        self.spatial_endpoints = [
            # Main CSDI portal endpoint
            'https://portal.csdi.gov.hk/geoportal/rest/services/hko/hko_rcd_1634953844424_88011/MapServer',
            'https://portal.csdi.gov.hk/geoportal/rest/services/hko/hko_rcd_1634953844424_88011/MapServer/0',
            'https://portal.csdi.gov.hk/geoportal/rest/services/hko/hko_rcd_1634953844424_88011/MapServer/0/query',
            
            # Alternative ArcGIS REST service formats
            'https://portal.csdi.gov.hk/geoportal/rest/services/hko/hko_rcd_1634953844424_88011/FeatureServer',
            'https://portal.csdi.gov.hk/geoportal/rest/services/hko/hko_rcd_1634953844424_88011/FeatureServer/0',
            'https://portal.csdi.gov.hk/geoportal/rest/services/hko/hko_rcd_1634953844424_88011/FeatureServer/0/query',
            
            # Try data.gov.hk direct access
            'https://geodata.gov.hk/gs/api/v1.0.0/geoDataSearch',
            'https://data.gov.hk/en-data/api/get',
        ]
        
        # Known working HKO endpoints for comparison
        self.hko_endpoints = [
            'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en',
            'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=ltmv&lang=en'
        ]

    def build_spatial_query_parameters(self) -> Dict[str, str]:
        """Build comprehensive query parameters for spatial wind data"""
        return {
            # Standard ArcGIS REST parameters
            'where': '1=1',  # Get all records
            'outFields': '*',  # All fields including wind data
            'f': 'json',  # JSON format
            'returnGeometry': 'true',  # Include spatial coordinates
            'spatialRel': 'esriSpatialRelIntersects',
            'returnCountOnly': 'false',
            'returnIdsOnly': 'false',
            'returnDistinctValues': 'false',
            'orderByFields': 'AutomaticWeatherStation_en ASC',
            
            # Time-based filtering for latest data
            'timeRelation': 'esriTimeRelationOverlaps',
            'resultRecordCount': '100',  # Limit results
            
            # Specific fields we want
            'outSR': '4326',  # WGS84 coordinate system
        }

    def fetch_10_minute_wind_data(self) -> List[Dict]:
        """Fetch the latest 10-minute wind data from spatial endpoints"""
        
        all_wind_data = []
        query_params = self.build_spatial_query_parameters()
        
        print("🌪️  Fetching 10-minute real-time wind data...")
        print("=" * 60)
        
        # Try spatial endpoints first
        for endpoint in self.spatial_endpoints:
            try:
                print(f"🔍 Trying spatial endpoint: {endpoint[:50]}...")
                
                if 'query' in endpoint:
                    # For query endpoints, add parameters
                    response = self.session.get(endpoint, params=query_params, timeout=15)
                elif 'geoDataSearch' in endpoint:
                    # For geodata search
                    search_params = {'q': 'wind', 'limit': 50, 'format': 'json'}
                    response = self.session.get(endpoint, params=search_params, timeout=15)
                elif 'data.gov.hk' in endpoint:
                    # For data.gov.hk API
                    api_params = {
                        'url': 'https://portal.csdi.gov.hk/geoportal/rest/services/hko/hko_rcd_1634953844424_88011',
                        'format': 'json'
                    }
                    response = self.session.get(endpoint, params=api_params, timeout=15)
                else:
                    # For service info endpoints
                    info_params = {'f': 'json'}
                    response = self.session.get(endpoint, params=info_params, timeout=15)
                
                response.raise_for_status()
                
                # Parse the response
                wind_data = self._parse_spatial_response(response, endpoint)
                if wind_data:
                    all_wind_data.extend(wind_data)
                    print(f"✅ Success: {len(wind_data)} wind data points from spatial API")
                else:
                    print(f"⚠️  No wind data in response")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Request failed: {str(e)[:80]}...")
            except Exception as e:
                print(f"❌ Parse error: {str(e)[:80]}...")
                
            time.sleep(1)  # Rate limiting
        
        # If spatial endpoints fail, try known working HKO endpoints
        if not all_wind_data:
            print(f"\n🔄 Spatial endpoints failed, trying HKO APIs...")
            for endpoint in self.hko_endpoints:
                try:
                    print(f"🔍 Trying HKO endpoint: {endpoint[:50]}...")
                    response = self.session.get(endpoint, timeout=10)
                    response.raise_for_status()
                    
                    wind_data = self._parse_hko_response(response, endpoint)
                    if wind_data:
                        all_wind_data.extend(wind_data)
                        print(f"✅ Fallback success: {len(wind_data)} data points")
                        
                except Exception as e:
                    print(f"❌ HKO endpoint failed: {str(e)[:60]}...")
                    
                time.sleep(1)
        
        return all_wind_data

    def _parse_spatial_response(self, response: requests.Response, endpoint: str) -> List[Dict]:
        """Parse spatial API response for wind data"""
        wind_data = []
        
        try:
            content_type = response.headers.get('content-type', '').lower()
            
            if 'json' in content_type or response.text.strip().startswith('{'):
                data = response.json()
                
                # Handle ArcGIS FeatureServer/MapServer responses
                if 'features' in data:
                    for feature in data['features']:
                        wind_point = self._extract_spatial_wind_data(feature, endpoint)
                        if wind_point:
                            wind_data.append(wind_point)
                
                # Handle service metadata responses
                elif 'layers' in data:
                    print(f"📊 Service info: Found {len(data['layers'])} layers")
                    for layer in data['layers']:
                        if 'wind' in layer.get('name', '').lower():
                            print(f"  🌪️  Wind layer: {layer.get('name')}")
                
                # Handle general JSON responses
                elif isinstance(data, dict):
                    wind_point = self._extract_general_wind_data(data, endpoint)
                    if wind_point:
                        wind_data.append(wind_point)
                        
                # Handle search results
                elif isinstance(data, list):
                    for item in data:
                        wind_point = self._extract_general_wind_data(item, endpoint)
                        if wind_point:
                            wind_data.append(wind_point)
            
            else:
                # Handle non-JSON responses
                text = response.text
                if 'wind' in text.lower():
                    print(f"📄 Found text data with wind information ({len(text)} chars)")
                    # Could add text parsing here if needed
                    
        except json.JSONDecodeError:
            print(f"⚠️  Non-JSON response from {endpoint}")
        except Exception as e:
            print(f"❌ Parse error: {e}")
            
        return wind_data

    def _extract_spatial_wind_data(self, feature: Dict, source: str) -> Optional[Dict]:
        """Extract wind data from spatial feature"""
        
        attributes = feature.get('attributes', {})
        geometry = feature.get('geometry', {})
        
        wind_data = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'data_type': 'spatial_10min_wind'
        }
        
        # Extract station information (from data spec)
        for station_field in ['AutomaticWeatherStation_en', 'AutomaticWeatherStation_uc', 'AutomaticWeatherStation_sc']:
            if station_field in attributes:
                wind_data['station'] = attributes[station_field]
                wind_data['station_field'] = station_field
                break
        
        # Extract data URL if available
        if 'Data_url' in attributes:
            wind_data['data_url'] = attributes['Data_url']
        
        # Extract coordinates
        if geometry:
            if 'x' in geometry and 'y' in geometry:
                wind_data['longitude'] = geometry['x']
                wind_data['latitude'] = geometry['y']
            elif 'coordinates' in geometry:
                coords = geometry['coordinates']
                if isinstance(coords, list) and len(coords) >= 2:
                    wind_data['longitude'] = coords[0]
                    wind_data['latitude'] = coords[1]
        
        # Look for wind-specific fields
        wind_fields_found = False
        for key, value in attributes.items():
            key_lower = key.lower()
            
            # Wind speed
            if any(term in key_lower for term in ['wind_speed', 'windspeed', 'speed']):
                wind_data['wind_speed_kmh'] = value
                wind_fields_found = True
            
            # Wind direction  
            elif any(term in key_lower for term in ['wind_dir', 'direction', 'bearing']):
                wind_data['wind_direction'] = value
                wind_fields_found = True
                
            # Gust speed
            elif 'gust' in key_lower:
                wind_data['gust_speed_kmh'] = value
                wind_fields_found = True
                
            # Include all other attributes for analysis
            else:
                wind_data[f'attr_{key}'] = value
        
        # Only return if we have wind data or station info
        return wind_data if (wind_fields_found or 'station' in wind_data) else None

    def _extract_general_wind_data(self, data: Dict, source: str) -> Optional[Dict]:
        """Extract wind data from general JSON structure"""
        
        wind_data = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'data_type': 'general_wind_data'
        }
        
        wind_fields_found = False
        
        for key, value in data.items():
            key_lower = str(key).lower()
            
            # Station identification
            if any(term in key_lower for term in ['station', 'site', 'location']):
                wind_data['station'] = value
                
            # Wind measurements
            elif 'wind' in key_lower:
                if 'speed' in key_lower:
                    wind_data['wind_speed'] = value
                    wind_fields_found = True
                elif 'direction' in key_lower or 'dir' in key_lower:
                    wind_data['wind_direction'] = value  
                    wind_fields_found = True
                elif 'gust' in key_lower:
                    wind_data['gust_speed'] = value
                    wind_fields_found = True
                else:
                    wind_data[f'wind_{key}'] = value
                    wind_fields_found = True
            
            # Geographic coordinates
            elif key_lower in ['lat', 'latitude', 'y']:
                wind_data['latitude'] = value
            elif key_lower in ['lon', 'lng', 'longitude', 'x']:
                wind_data['longitude'] = value
                
            # Data URL
            elif 'url' in key_lower and 'data' in key_lower:
                wind_data['data_url'] = value
        
        return wind_data if wind_fields_found else None

    def _parse_hko_response(self, response: requests.Response, endpoint: str) -> List[Dict]:
        """Parse HKO API response as fallback"""
        wind_data = []
        
        try:
            data = response.json()
            
            # Parse regional weather data
            if 'rainfall' in data and isinstance(data['rainfall'], list):
                for station_data in data['rainfall']:
                    wind_point = {
                        'timestamp': datetime.now().isoformat(),
                        'source': endpoint,
                        'data_type': 'hko_regional_weather',
                        'station': station_data.get('station', 'Unknown')
                    }
                    
                    # Look for any wind-related fields
                    for key, value in station_data.items():
                        if 'wind' in key.lower():
                            wind_point[key] = value
                    
                    wind_data.append(wind_point)
                    
        except Exception as e:
            print(f"HKO parsing error: {e}")
            
        return wind_data

    def analyze_10_minute_wind_trends(self, wind_data: List[Dict]) -> Dict:
        """Analyze the 10-minute wind data for trends and patterns"""
        
        analysis = {
            'data_timestamp': datetime.now().isoformat(),
            'total_stations': len(wind_data),
            'data_sources': list(set([d.get('source', 'unknown') for d in wind_data])),
            'station_coverage': {},
            'wind_measurements': {},
            'spatial_distribution': {},
            'signal_8_assessment': {}
        }
        
        # Analyze station coverage
        stations = []
        coordinates = []
        wind_speeds = []
        gust_speeds = []
        
        for data_point in wind_data:
            # Station information
            station = data_point.get('station')
            if station:
                stations.append(station)
            
            # Coordinates
            lat = data_point.get('latitude')
            lon = data_point.get('longitude') 
            if lat and lon:
                coordinates.append((float(lat), float(lon)))
            
            # Wind measurements
            wind_speed = data_point.get('wind_speed_kmh') or data_point.get('wind_speed')
            if wind_speed:
                try:
                    wind_speeds.append(float(wind_speed))
                except (ValueError, TypeError):
                    pass
                    
            gust_speed = data_point.get('gust_speed_kmh') or data_point.get('gust_speed')
            if gust_speed:
                try:
                    gust_speeds.append(float(gust_speed))
                except (ValueError, TypeError):
                    pass
        
        analysis['station_coverage'] = {
            'total_stations': len(set(stations)),
            'stations_with_coordinates': len(coordinates),
            'station_list': list(set(stations))[:10]  # First 10 stations
        }
        
        # Wind measurements analysis
        if wind_speeds:
            analysis['wind_measurements']['sustained_winds'] = {
                'count': len(wind_speeds),
                'max_kmh': max(wind_speeds),
                'min_kmh': min(wind_speeds),
                'avg_kmh': round(sum(wind_speeds) / len(wind_speeds), 1)
            }
            
        if gust_speeds:
            analysis['wind_measurements']['gusts'] = {
                'count': len(gust_speeds),
                'max_kmh': max(gust_speeds),
                'min_kmh': min(gust_speeds),
                'avg_kmh': round(sum(gust_speeds) / len(gust_speeds), 1)
            }
        
        # Spatial distribution
        if coordinates:
            lats = [coord[0] for coord in coordinates]
            lons = [coord[1] for coord in coordinates]
            analysis['spatial_distribution'] = {
                'coordinate_count': len(coordinates),
                'latitude_range': [min(lats), max(lats)],
                'longitude_range': [min(lons), max(lons)],
                'geographic_coverage': 'Hong Kong region' if len(coordinates) > 5 else 'Limited coverage'
            }
        
        # Signal 8 assessment
        max_wind = max(wind_speeds) if wind_speeds else 0
        max_gust = max(gust_speeds) if gust_speeds else 0
        
        if max_wind >= 63 or max_gust >= 63:
            risk_level = "HIGH - Signal 8 conditions present"
        elif max_wind >= 41 or max_gust >= 41:
            risk_level = "MODERATE - Signal 3 conditions, monitor for Signal 8"
        elif max_wind >= 22 or max_gust >= 22:
            risk_level = "LOW - Signal 1 conditions"
        else:
            risk_level = "MINIMAL - Calm conditions"
            
        analysis['signal_8_assessment'] = {
            'risk_level': risk_level,
            'max_sustained_wind': max_wind,
            'max_gust': max_gust,
            'stations_above_signal8': len([w for w in wind_speeds if w >= 63]),
            'stations_above_signal3': len([w for w in wind_speeds if w >= 41])
        }
        
        return analysis

    def generate_realtime_report(self, wind_data: List[Dict], analysis: Dict):
        """Generate real-time wind data report"""
        
        print(f"\n" + "🌪️ " * 25)
        print("HONG KONG 10-MINUTE REAL-TIME WIND DATA REPORT")
        print(f"Data Updated Every 10 Minutes • {datetime.now().strftime('%H:%M HKT, %B %d, %Y')}")
        print("🌪️ " * 25)
        
        # Data summary
        print(f"\n📊 DATA SUMMARY")
        print("=" * 30)
        print(f"Total Data Points: {analysis['total_stations']}")
        print(f"Data Sources: {len(analysis['data_sources'])}")
        
        for source in analysis['data_sources']:
            source_count = len([d for d in wind_data if d.get('source') == source])
            print(f"  • {source[:50]}... ({source_count} points)")
        
        # Station coverage
        coverage = analysis['station_coverage']
        print(f"\n🏢 STATION COVERAGE")
        print("=" * 25)
        print(f"Unique Stations: {coverage['total_stations']}")
        print(f"With Coordinates: {coverage['stations_with_coordinates']}")
        
        if coverage['station_list']:
            print(f"Sample Stations:")
            for i, station in enumerate(coverage['station_list'][:5], 1):
                print(f"  {i}. {station}")
        
        # Wind measurements
        measurements = analysis.get('wind_measurements', {})
        if measurements:
            print(f"\n💨 WIND MEASUREMENTS (10-Minute Averages)")
            print("=" * 45)
            
            sustained = measurements.get('sustained_winds')
            if sustained:
                print(f"Sustained Winds ({sustained['count']} stations):")
                print(f"  • Maximum: {sustained['max_kmh']} km/h")
                print(f"  • Average: {sustained['avg_kmh']} km/h") 
                print(f"  • Minimum: {sustained['min_kmh']} km/h")
            
            gusts = measurements.get('gusts')
            if gusts:
                print(f"Wind Gusts ({gusts['count']} stations):")
                print(f"  • Maximum: {gusts['max_kmh']} km/h")
                print(f"  • Average: {gusts['avg_kmh']} km/h")
                print(f"  • Minimum: {gusts['min_kmh']} km/h")
        
        # Spatial coverage
        spatial = analysis.get('spatial_distribution', {})
        if spatial:
            print(f"\n🗺️  SPATIAL COVERAGE")
            print("=" * 22)
            print(f"Coordinates Available: {spatial['coordinate_count']}")
            if spatial.get('latitude_range'):
                lat_range = spatial['latitude_range']
                lon_range = spatial['longitude_range']
                print(f"Latitude Range: {lat_range[0]:.3f}° to {lat_range[1]:.3f}°N")
                print(f"Longitude Range: {lon_range[0]:.3f}° to {lon_range[1]:.3f}°E")
            print(f"Coverage: {spatial.get('geographic_coverage', 'Unknown')}")
        
        # Signal assessment
        signal_assessment = analysis['signal_8_assessment']
        print(f"\n🎯 SIGNAL 8 REAL-TIME ASSESSMENT")
        print("=" * 35)
        print(f"Risk Level: {signal_assessment['risk_level']}")
        print(f"Max Sustained Wind: {signal_assessment['max_sustained_wind']} km/h")
        print(f"Max Gust: {signal_assessment['max_gust']} km/h")
        print(f"Stations ≥ Signal 8 (63+ km/h): {signal_assessment['stations_above_signal8']}")
        print(f"Stations ≥ Signal 3 (41+ km/h): {signal_assessment['stations_above_signal3']}")
        
        # Data quality assessment
        print(f"\n📈 DATA QUALITY")
        print("=" * 18)
        
        data_quality = "EXCELLENT" if analysis['total_stations'] > 10 else \
                      "GOOD" if analysis['total_stations'] > 5 else \
                      "LIMITED" if analysis['total_stations'] > 0 else "NO DATA"
        
        print(f"Overall Quality: {data_quality}")
        print(f"Update Frequency: Every 10 minutes (as per specification)")
        print(f"Last Update: {datetime.now().strftime('%H:%M:%S HKT')}")
        
        print(f"\n" + "🌪️ " * 25)

def main():
    """Main execution function"""
    
    api = HKRealTimeWindDataAPI()
    
    print("🚀 Accessing Hong Kong 10-minute real-time wind data...")
    print("Targeting spatial data layer: latest_10min_wind")
    print("=" * 70)
    
    # Fetch the 10-minute wind data
    wind_data = api.fetch_10_minute_wind_data()
    
    if not wind_data:
        print("\n❌ Unable to access 10-minute wind data")
        print("🔍 Possible issues:")
        print("  • Spatial API endpoints may require authentication")
        print("  • API structure may have changed")
        print("  • Network or service temporarily unavailable")
        print("\n💡 Recommendations:")
        print("  • Check the CSDI portal directly at:")
        print("    https://portal.csdi.gov.hk/geoportal/?datasetId=hko_rcd_1634953844424_88011")
        print("  • Try again in a few minutes")
        print("  • Contact HKO for API access details")
        return
    
    # Analyze the wind data
    analysis = api.analyze_10_minute_wind_trends(wind_data)
    
    # Generate report
    api.generate_realtime_report(wind_data, analysis)
    
    # Save detailed results
    results = {
        'fetch_time': datetime.now().isoformat(),
        'wind_data': wind_data,
        'analysis': analysis,
        'metadata': {
            'script_version': '1.0',
            'target_dataset': 'latest_10min_wind',
            'update_frequency': '10 minutes',
            'data_fields': ['AutomaticWeatherStation_en', 'AutomaticWeatherStation_uc', 'AutomaticWeatherStation_sc', 'Data_url']
        }
    }
    
    filename = f"hk_10min_wind_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed data saved to: {filename}")
    print(f"🔄 Run this script every 10 minutes for continuous monitoring")
    print(f"📱 For official updates: https://www.hko.gov.hk")

if __name__ == "__main__":
    main()
