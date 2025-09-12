#!/usr/bin/env python3
"""
Debug script to examine the HTML structure of the HK government website
"""

import requests
from bs4 import BeautifulSoup
import re

def debug_page_structure():
    url = "https://www.access.gov.hk/en/howtomakeinfo/index.html"
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    print(f"Fetching: {url}")
    response = session.get(url, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Look for all links
    all_links = soup.find_all('a', href=True)
    print(f"Total links found: {len(all_links)}")
    
    # Filter for potential department links
    department_links = []
    for link in all_links:
        href = link.get('href')
        if href and isinstance(href, str):
            # Print first few links to understand the pattern
            if len(department_links) < 20:
                text = link.get_text(strip=True)
                print(f"Link: {href} -> Text: '{text}'")
            
            # Look for various patterns
            if ('/howtomakeinfo/' in href or 
                href.startswith('https://www.access.gov.hk/en/howtomakeinfo/') or
                (href.endswith('.html') and 'howtomakeinfo' in href)):
                department_links.append({
                    'href': href,
                    'text': link.get_text(strip=True)
                })
    
    print(f"\nDepartment-related links found: {len(department_links)}")
    for dept in department_links[:10]:  # Show first 10
        print(f"  {dept['href']} -> {dept['text']}")
    
    # Also search for text that might contain emails
    page_text = soup.get_text()
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    emails = email_pattern.findall(page_text)
    print(f"\nEmails found on main page: {len(emails)}")
    for email in emails[:5]:  # Show first 5
        print(f"  {email}")

if __name__ == "__main__":
    debug_page_structure()
