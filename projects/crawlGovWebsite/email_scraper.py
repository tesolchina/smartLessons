#!/usr/bin/env python3
"""
Hong Kong Government Website Email Scraper
Extracts email addresses from https://www.access.gov.hk/en/howtomakeinfo/index.html
and all linked department pages.
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import csv
import json
from urllib.parse import urljoin, urlparse
from datetime import datetime
import sys

class HKGovEmailScraper:
    def __init__(self):
        self.base_url = "https://www.access.gov.hk"
        self.start_url = "https://www.access.gov.hk/en/howtomakeinfo/index.html"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.emails_found = []
        self.department_links = []
        self.processed_urls = set()
        
        # Email regex pattern
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    
    def fetch_page(self, url, max_retries=3):
        """Fetch a web page with error handling and retries"""
        for attempt in range(max_retries):
            try:
                print(f"Fetching: {url}")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {url} (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    print(f"Failed to fetch {url} after {max_retries} attempts")
                    return None
    
    def extract_department_links(self):
        """Extract all department links from the main page"""
        print("Extracting department links from main page...")
        response = self.fetch_page(self.start_url)
        if not response:
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all links that point to department pages
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href')
            if href and isinstance(href, str):
                # Look for .html files that are likely department pages
                # They appear as relative links like "afcd.html", "judiciary.html", etc.
                if (href.endswith('.html') and 
                    not href.startswith('http') and 
                    not href.startswith('#') and
                    not href.startswith('javascript:') and
                    'filemanager' not in href):
                    
                    # Convert relative URL to absolute URL
                    full_url = urljoin(self.start_url, href)
                    department_name = link.get_text(strip=True)
                    
                    if department_name and full_url not in [d['url'] for d in self.department_links]:
                        self.department_links.append({
                            'name': department_name,
                            'url': full_url
                        })
        
        print(f"Found {len(self.department_links)} department links")
    
    def extract_emails_from_text(self, text, source_url, department_name):
        """Extract email addresses from text content"""
        emails = self.email_pattern.findall(text)
        for email in emails:
            # Skip common false positives
            if not any(skip in email.lower() for skip in ['example.com', 'test.com', 'dummy']):
                email_data = {
                    'email': email.lower(),
                    'department': department_name,
                    'source_url': source_url,
                    'found_at': datetime.now().isoformat()
                }
                # Avoid duplicates
                if not any(e['email'] == email.lower() and e['department'] == department_name 
                          for e in self.emails_found):
                    self.emails_found.append(email_data)
                    print(f"Found email: {email} from {department_name}")
    
    def scrape_department_page(self, department):
        """Scrape a single department page for email addresses"""
        url = department['url']
        name = department['name']
        
        if url in self.processed_urls:
            return
        
        self.processed_urls.add(url)
        response = self.fetch_page(url)
        if not response:
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract all text content
        page_text = soup.get_text()
        self.extract_emails_from_text(page_text, url, name)
        
        # Also look for mailto links
        mailto_links = soup.find_all('a', href=re.compile(r'^mailto:', re.I))
        for link in mailto_links:
            href = link.get('href')
            if href and isinstance(href, str):
                email_match = re.search(r'mailto:([^?&\s]+)', href, re.I)
            if email_match:
                email = email_match.group(1).lower()
                email_data = {
                    'email': email,
                    'department': name,
                    'source_url': url,
                    'found_at': datetime.now().isoformat()
                }
                if not any(e['email'] == email and e['department'] == name 
                          for e in self.emails_found):
                    self.emails_found.append(email_data)
                    print(f"Found mailto email: {email} from {name}")
        
        # Be respectful to the server
        time.sleep(1)
    
    def scrape_all_departments(self):
        """Scrape all department pages for email addresses"""
        print(f"\nScraping {len(self.department_links)} department pages...")
        for i, department in enumerate(self.department_links, 1):
            print(f"\nProgress: {i}/{len(self.department_links)} - {department['name']}")
            self.scrape_department_page(department)
    
    def save_results(self):
        """Save the extracted emails to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as CSV
        csv_filename = f"hk_gov_emails_{timestamp}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            if self.emails_found:
                fieldnames = ['email', 'department', 'source_url', 'found_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for email_data in self.emails_found:
                    writer.writerow(email_data)
        
        # Save as JSON
        json_filename = f"hk_gov_emails_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.emails_found, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to:")
        print(f"- {csv_filename}")
        print(f"- {json_filename}")
    
    def print_summary(self):
        """Print a summary of the scraping results"""
        print(f"\n{'='*50}")
        print(f"SCRAPING SUMMARY")
        print(f"{'='*50}")
        print(f"Total emails found: {len(self.emails_found)}")
        print(f"Total departments scraped: {len(self.processed_urls)}")
        
        if self.emails_found:
            print(f"\nUnique email domains:")
            domains = set()
            for email_data in self.emails_found:
                domain = email_data['email'].split('@')[1]
                domains.add(domain)
            for domain in sorted(domains):
                count = sum(1 for e in self.emails_found if e['email'].endswith('@' + domain))
                print(f"- {domain}: {count} emails")
            
            print(f"\nSample emails found:")
            for email_data in self.emails_found[:10]:  # Show first 10
                print(f"- {email_data['email']} ({email_data['department']})")
            
            if len(self.emails_found) > 10:
                print(f"... and {len(self.emails_found) - 10} more")
    
    def run(self):
        """Run the complete scraping process"""
        print("Starting Hong Kong Government Email Scraper...")
        print(f"Target URL: {self.start_url}")
        
        try:
            # Step 1: Extract department links
            self.extract_department_links()
            
            if not self.department_links:
                print("No department links found. Exiting.")
                return
            
            # Step 2: Scrape main page for emails
            print("\nScraping main page for emails...")
            response = self.fetch_page(self.start_url)
            if response:
                soup = BeautifulSoup(response.content, 'html.parser')
                page_text = soup.get_text()
                self.extract_emails_from_text(page_text, self.start_url, "Main Page")
            
            # Step 3: Scrape all department pages
            self.scrape_all_departments()
            
            # Step 4: Save and display results
            if self.emails_found:
                self.save_results()
                self.print_summary()
            else:
                print("\nNo emails found.")
                
        except KeyboardInterrupt:
            print("\n\nScraping interrupted by user.")
            if self.emails_found:
                print("Saving partial results...")
                self.save_results()
                self.print_summary()
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            if self.emails_found:
                print("Saving partial results...")
                self.save_results()

def main():
    scraper = HKGovEmailScraper()
    scraper.run()

if __name__ == "__main__":
    main()
