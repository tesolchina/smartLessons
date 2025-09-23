#!/usr/bin/env python3
"""
Quick script to check collector status and data
"""
import os
import subprocess
from datetime import datetime

def check_collector_status():
    print(f"🔍 Collector Status Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check if process is running
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if 'collect_realtime_wind.py' in result.stdout:
            lines = [line for line in result.stdout.split('\n') if 'collect_realtime_wind.py' in line]
            for line in lines:
                if 'grep' not in line:
                    print(f"✅ Collector is running: {line.strip()}")
        else:
            print("❌ Collector process not found!")
    except Exception as e:
        print(f"❌ Error checking process: {e}")
    
    print()
    
    # Check data files
    data_dir = "data_archive"
    if os.path.exists(data_dir):
        files = os.listdir(data_dir)
        csv_files = [f for f in files if f.endswith('.csv')]
        
        print(f"📁 Data files in {data_dir}:")
        for file in sorted(files):
            file_path = os.path.join(data_dir, file)
            size = os.path.getsize(file_path)
            mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            print(f"  📄 {file} ({size} bytes, modified: {mtime.strftime('%H:%M:%S')})")
        
        if csv_files:
            # Show latest data from newest CSV
            latest_csv = sorted(csv_files)[-1]
            csv_path = os.path.join(data_dir, latest_csv)
            
            try:
                with open(csv_path, 'r') as f:
                    lines = f.readlines()
                    print(f"\n📊 Latest CSV: {latest_csv} ({len(lines)} lines)")
                    if len(lines) > 1:
                        print(f"  Last entry: {lines[-1].strip()}")
            except Exception as e:
                print(f"❌ Error reading CSV: {e}")
    else:
        print("❌ Data archive directory not found!")
    
    print("\n🕐 Scheduled to stop: Tomorrow (Sep 9) at 5:00 PM")

if __name__ == "__main__":
    check_collector_status()
