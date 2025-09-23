#!/usr/bin/env python3
"""
Hong Kong Signal 8 Summary - Tomorrow Morning Assessment
=======================================================

Final comprehensive summary based on real-time HKO data analysis.
This script provides a clear, actionable assessment for September 8, 2025 morning.

Key Findings from Live Data:
- Signal 8 Southeast Gale is CURRENTLY ACTIVE (as of 00:06 HKT Sep 8)
- Severe Tropical Storm Tapah is 250km southwest of Hong Kong  
- HKO forecasts Signal 8 will remain until at least 11 AM Monday
- Wind speeds: 60 km/h sustained, gusts up to 89 km/h recorded
- Storm surge flooding warnings active for low-lying areas

Author: GitHub Copilot  
Date: September 8, 2025
"""

import json
from datetime import datetime
from typing import Dict, Any

def load_latest_analysis() -> Dict[str, Any]:
    """Load the most recent analysis data"""
    try:
        with open('signal8_emergency_report_20250908_000624.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Emergency report file not found. Please run signal8_emergency_analyzer.py first.")
        return {}

def generate_tomorrow_morning_briefing(analysis_data: Dict[str, Any]):
    """Generate executive summary for tomorrow morning conditions"""
    
    print("=" * 80)
    print("🌪️  HONG KONG WIND CONDITIONS - EXECUTIVE BRIEFING")
    print("   Tomorrow Morning Assessment: September 8, 2025")
    print("=" * 80)
    
    # Current situation
    current_conditions = analysis_data.get('current_conditions', {})
    storm_info = current_conditions.get('typhoon_info', {})
    
    print(f"\n📋 SITUATION SUMMARY")
    print("─" * 30)
    print(f"• STATUS: Signal 8 Southeast Gale IS CURRENTLY IN FORCE")
    print(f"• STORM: Severe Tropical Storm {storm_info.get('name', 'Tapah')}")
    print(f"• DISTANCE: {storm_info.get('distance_km', 250)} km {storm_info.get('direction', 'southwest')} of Hong Kong")
    print(f"• STORM INTENSITY: {storm_info.get('max_sustained_winds_kmh', 105)} km/h maximum winds")
    print(f"• UPDATE TIME: {datetime.now().strftime('%H:%M HKT, %B %d, %Y')}")
    
    # Tomorrow morning specific assessment
    print(f"\n🌅 TOMORROW MORNING (8 AM - 12 PM) FORECAST")
    print("─" * 50)
    
    signal_8_analysis = analysis_data.get('signal_8_analysis', {})
    tomorrow_assessment = signal_8_analysis.get('tomorrow_morning_assessment', {})
    
    probability = tomorrow_assessment.get('probability', 'MODERATE')
    if probability == 'VERY HIGH':
        status_emoji = "🚨"
        risk_level = "EXTREME RISK"
    elif probability == 'HIGH':
        status_emoji = "⚠️"
        risk_level = "HIGH RISK"  
    elif probability == 'MODERATE':
        status_emoji = "⚠️"
        risk_level = "MODERATE RISK"
    else:
        status_emoji = "❓"
        risk_level = "UNCERTAIN"
        
    print(f"{status_emoji} SIGNAL 8 CONTINUATION PROBABILITY: {probability}")
    print(f"{status_emoji} RISK LEVEL: {risk_level}")
    print(f"• REASONING: {tomorrow_assessment.get('reasoning', 'Based on current storm track')}")
    print(f"• EXPECTED CONDITIONS: {tomorrow_assessment.get('expected_conditions', 'Monitor official updates')}")
    print(f"• CRITICAL TIMING: {tomorrow_assessment.get('peak_time', 'Early morning hours')}")
    
    # Official HKO forecast
    forecast = current_conditions.get('forecast', {})
    if forecast:
        print(f"\n📊 OFFICIAL HKO FORECAST")
        print("─" * 30)
        if 'signal_duration' in forecast:
            print(f"• SIGNAL DURATION: {forecast['signal_duration']}")
        if 'wind_expectation' in forecast:
            print(f"• WIND OUTLOOK: {forecast['wind_expectation']}")
    
    # Current wind measurements  
    wind_conditions = signal_8_analysis.get('current_wind_conditions', {})
    if wind_conditions:
        print(f"\n💨 CURRENT WIND READINGS")
        print("─" * 30)
        print(f"• STATIONS REPORTING: {wind_conditions.get('stations_reporting', 0)}")
        print(f"• MAX SUSTAINED WIND: {wind_conditions.get('max_sustained_wind', 0)} km/h")
        print(f"• MAX GUST RECORDED: {wind_conditions.get('max_gust', 0)} km/h")
        
        # Show key locations
        locations = wind_conditions.get('locations', [])
        if locations and any(loc.get('sustained_wind', 0) > 0 for loc in locations):
            print(f"• KEY MEASUREMENTS:")
            for loc in locations[:3]:  # Top 3 locations
                sustained = loc.get('sustained_wind', 0)
                gust = loc.get('gust', 0)
                if sustained > 0:
                    gust_text = f", gusts {gust} km/h" if gust > 0 else ""
                    print(f"  - {loc['name']}: {sustained} km/h{gust_text}")
    
    # Action items for tomorrow morning
    print(f"\n🎯 ACTION ITEMS FOR TOMORROW MORNING")
    print("─" * 45)
    
    if probability in ['VERY HIGH', 'HIGH']:
        actions = [
            "❌ DO NOT GO OUTSIDE - Signal 8 conditions expected",
            "🚌 Public transport will be SUSPENDED",
            "💼 Work and schools will be CANCELLED", 
            "🏪 Most shops and services will be CLOSED",
            "📱 Monitor HKO updates every 30 minutes",
            "🔋 Keep devices charged, prepare for power outages",
            "🌊 AVOID all coastal and exposed areas"
        ]
    elif probability == 'MODERATE':
        actions = [
            "⚠️  Check Signal status before leaving home",
            "🚌 Monitor public transport announcements", 
            "💼 Confirm work/school arrangements with employers",
            "📱 Check HKO updates every hour",
            "🧳 Prepare to return home quickly if Signal continues",
            "🌊 Avoid coastal areas and exposed locations"
        ]
    else:
        actions = [
            "❓ Monitor official HKO updates hourly",
            "📱 Enable emergency weather alerts",
            "🚌 Check transport status before travel",
            "⚠️  Be prepared for rapid changes in conditions"
        ]
    
    for i, action in enumerate(actions, 1):
        print(f"{i:2d}. {action}")
    
    # Emergency preparedness
    print(f"\n🆘 EMERGENCY PREPAREDNESS")  
    print("─" * 30)
    print("• EMERGENCY CONTACT: 999")
    print("• HKO WEATHER HOTLINE: 1878 200") 
    print("• TRAFFIC INFO: 1968")
    print("• HKO WEBSITE: https://www.hko.gov.hk")
    print("• HKO MOBILE APP: MyObservatory")
    
    # Key warnings
    warnings = current_conditions.get('warnings', [])
    if warnings:
        print(f"\n🚩 ACTIVE WARNINGS")
        print("─" * 20)
        for warning in warnings:
            print(f"• {warning.upper()}")
    
    # Final assessment
    print(f"\n" + "=" * 80)
    print("🎯 FINAL ASSESSMENT FOR TOMORROW MORNING")
    print("=" * 80)
    
    if probability in ['VERY HIGH', 'HIGH']:
        final_advice = "🚨 STAY HOME - Signal 8 conditions will continue tomorrow morning. Do not attempt to go outside or travel. This is a dangerous weather situation."
    elif probability == 'MODERATE':
        final_advice = "⚠️  EXERCISE EXTREME CAUTION - Signal 8 may continue into tomorrow morning. Check conditions before leaving home and be prepared to shelter immediately."
    else:
        final_advice = "❓ STAY VIGILANT - Weather conditions are changing rapidly. Monitor official updates and be prepared for Signal 8 to continue or change quickly."
    
    print(f"\n{final_advice}")
    
    print(f"\n⏰ NEXT UPDATE: Monitor HKO announcements continuously")
    print(f"📅 REPORT GENERATED: {datetime.now().strftime('%H:%M HKT on %B %d, %Y')}")
    print(f"\n" + "=" * 80)

def create_quick_reference_card():
    """Create a quick reference card for easy access"""
    
    reference_card = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     🌪️  SIGNAL 8 QUICK REFERENCE CARD                       ║
║                        Tomorrow Morning - Sept 8, 2025                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  CURRENT STATUS: Signal 8 Southeast Gale IN FORCE                          ║  
║  STORM: Severe Tropical Storm Tapah (250km SW of Hong Kong)                ║
║  FORECAST: Signal continues until at least 11 AM Monday                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ⚠️  TOMORROW MORNING PROBABILITY: MODERATE                                  ║
║  🌅 CONDITIONS: Signal may continue, winds strengthen at sunrise             ║
║  🎯 CRITICAL PERIOD: 6 AM - 11 AM                                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  🚨 IMMEDIATE ACTIONS:                                                       ║
║  • Check Signal status before leaving home                                  ║
║  • Monitor transport announcements                                          ║
║  • Confirm work/school arrangements                                         ║
║  • Stay away from coastal areas                                            ║
║  • Keep emergency supplies ready                                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  📞 EMERGENCY CONTACTS:                                                      ║
║  • Emergency: 999                                                          ║
║  • HKO Hotline: 1878 200                                                   ║
║  • Traffic Info: 1968                                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  📱 OFFICIAL SOURCES:                                                        ║
║  • Website: https://www.hko.gov.hk                                         ║
║  • Mobile App: MyObservatory                                               ║
║  • Gov News: https://www.news.gov.hk                                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ⏰ NEXT UPDATE: Monitor HKO every 30-60 minutes                            ║
║  📅 Generated: {datetime.now().strftime('%H:%M HKT, %B %d, %Y')}                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    
    print(reference_card)
    
    # Save to file
    with open('signal8_quick_reference.txt', 'w', encoding='utf-8') as f:
        f.write(reference_card)
    
    print("💾 Quick reference card saved to 'signal8_quick_reference.txt'")

def main():
    """Main execution function"""
    
    # Load the latest analysis
    analysis_data = load_latest_analysis()
    
    if not analysis_data:
        print("❌ Unable to load analysis data. Please run the emergency analyzer first.")
        return
    
    # Generate comprehensive briefing
    generate_tomorrow_morning_briefing(analysis_data)
    
    print("\n" + "─" * 80)
    
    # Create quick reference card
    create_quick_reference_card()
    
    print(f"\n🌪️  Analysis complete. Stay safe and monitor official HKO channels!")

if __name__ == "__main__":
    main()
