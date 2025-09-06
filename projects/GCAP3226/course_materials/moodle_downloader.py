#!/usr/bin/env python3
"""
Moodle Material Download Script for GCAP 3226
"""

import requests
from pathlib import Path
import json

class MoodleDownloader:
    def __init__(self, course_id="GCAP3226", username="", password=""):
        self.course_id = course_id
        self.username = username
        self.password = password
        self.base_url = "https://moodle.hkbu.edu.hk"  # Adjust as needed
        self.download_dir = Path("../course_materials")
        
    def login(self):
        """Login to Moodle"""
        # Implementation depends on HKBU Moodle setup
        # This is a template - needs actual authentication details
        pass
    
    def download_syllabus(self):
        """Download course syllabus"""
        print("Downloading course syllabus...")
        # Implementation for syllabus download
        pass
    
    def download_student_lists(self):
        """Download enrolled student lists"""
        print("Downloading student lists...")
        # Implementation for student list download
        pass
    
    def download_assignments(self):
        """Download all assignment instructions"""
        print("Downloading assignment instructions...")
        # Implementation for assignment download
        pass
    
    def download_all(self):
        """Download all available materials"""
        self.login()
        self.download_syllabus()
        self.download_student_lists()
        self.download_assignments()
        print("All downloads completed!")

if __name__ == "__main__":
    # Usage: python moodle_downloader.py
    # Configure your Moodle credentials first
    downloader = MoodleDownloader()
    downloader.download_all()
