#!/usr/bin/env python3
"""
Canva CLI - Main Interface
Generic Canva automation system for academic and professional use
Created: September 6, 2025
"""

import os
import sys
import time
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
except ImportError:
    print("❌ Missing dependencies. Please run:")
    print("pip3 install -r requirements.txt")
    sys.exit(1)

class CanvaCLI:
    """Main Canva CLI automation class"""
    
    def __init__(self):
        load_dotenv()
        self.email = os.getenv("CANVA_EMAIL", "simonwang@hkbu.edu.hk")
        self.password = os.getenv("CANVA_PASSWORD", "")
        self.headless = os.getenv("BROWSER_HEADLESS", "false").lower() == "true"
        self.download_path = os.getenv("DOWNLOAD_PATH", os.path.expanduser("~/Downloads/canva_designs"))
        self.driver = None
        self.wait = None
        
        # Create download directory
        os.makedirs(self.download_path, exist_ok=True)
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        try:
            # Chrome options for headless browsing
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Optional: run in headless mode
            if self.headless:
                chrome_options.add_argument('--headless')
            
            # Setup Chrome driver - let webdriver manager handle everything
            try:
                # Clear any cached drivers
                import shutil
                import os
                wdm_path = os.path.expanduser("~/.wdm")
                if os.path.exists(wdm_path):
                    shutil.rmtree(wdm_path)
                
                print("🔍 Setting up Chrome driver...")
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                
            except Exception as driver_error:
                print(f"❌ Chrome driver setup failed: {driver_error}")
                return False
            
            self.driver.implicitly_wait(10)
            
            # Setup WebDriverWait
            self.wait = WebDriverWait(self.driver, 10)
            
            # Execute script to prevent detection
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Browser initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize browser: {e}")
            print("💡 Make sure Google Chrome is installed and up to date")
            return False
    
    def login(self):
        """Login to Canva account"""
        try:
            print(f"🔐 Logging into Canva with: {self.email}")
            self.driver.get("https://www.canva.com/login")
            time.sleep(3)
            
            # Enter email
            email_field = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
            email_field.clear()
            email_field.send_keys(self.email)
            
            # Click continue
            continue_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' or contains(text(), 'Continue')]")))
            continue_btn.click()
            time.sleep(2)
            
            # Handle password or SSO
            try:
                password_field = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, "password")))
                if self.password:
                    password_field.send_keys(self.password)
                    login_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                    login_btn.click()
                else:
                    print("⚠️ Password field detected but no password provided")
                    print("🔐 Please enter password manually")
                    input("Press Enter when login is complete...")
            except TimeoutException:
                print("🔐 SSO or alternative login detected")
                print("⏳ Please complete login manually in the browser")
                input("Press Enter when you're logged in and see the Canva dashboard...")
            
            # Verify login success
            self.wait.until(EC.url_contains("canva.com"))
            time.sleep(3)
            
            print("✅ Successfully logged into Canva")
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def create_design(self, design_type="presentation", template_search="", custom_size=None):
        """Create a new design from template or blank"""
        try:
            # Navigate to create page
            if design_type == "presentation":
                self.driver.get("https://www.canva.com/create/presentations/")
            elif design_type == "poster":
                self.driver.get("https://www.canva.com/create/posters/")
            elif design_type == "social":
                self.driver.get("https://www.canva.com/create/instagram-posts/")
            else:
                self.driver.get("https://www.canva.com/create/")
            
            time.sleep(5)
            
            # Search for template if specified
            if template_search:
                try:
                    search_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='search' i], input[type='search']")))
                    search_box.clear()
                    search_box.send_keys(template_search)
                    search_box.send_keys(Keys.RETURN)
                    time.sleep(3)
                    
                    print(f"🔍 Searched for template: {template_search}")
                except:
                    print("⚠️ Could not find search box, using default templates")
            
            # Select first available template/design
            try:
                template = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid*='template'], .template, [class*='template']")))
                template.click()
                time.sleep(8)
                
                print(f"✅ Created new {design_type} design")
                return True
                
            except TimeoutException:
                # Try blank design if no templates found
                try:
                    blank_design = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Blank') or contains(text(), 'Create blank')]")))
                    blank_design.click()
                    time.sleep(8)
                    
                    print(f"✅ Created blank {design_type} design")
                    return True
                    
                except:
                    print("❌ Could not create design")
                    return False
            
        except Exception as e:
            print(f"❌ Design creation failed: {e}")
            return False
    
    def add_text_to_design(self, text_content):
        """Add text elements to the current design"""
        try:
            # Look for existing text elements first
            text_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid*='text'], [contenteditable='true'], .text-element")
            
            if text_elements:
                # Update existing text
                for i, element in enumerate(text_elements[:len(text_content)]):
                    try:
                        element.click()
                        time.sleep(1)
                        element.clear()
                        element.send_keys(text_content[i])
                        time.sleep(1)
                        print(f"✅ Updated text element {i+1}: {text_content[i][:30]}...")
                    except:
                        continue
            else:
                # Add new text elements
                for text in text_content:
                    try:
                        # Look for text tool in sidebar
                        text_tool = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Text') or contains(text(), 'Text')]")))
                        text_tool.click()
                        time.sleep(2)
                        
                        # Add text
                        add_text_btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add a heading') or contains(text(), 'Add text')]")))
                        add_text_btn.click()
                        time.sleep(2)
                        
                        # Type the content
                        active_text = self.driver.find_element(By.CSS_SELECTOR, "[contenteditable='true']")
                        active_text.clear()
                        active_text.send_keys(text)
                        
                        print(f"✅ Added text: {text[:30]}...")
                        time.sleep(1)
                        
                    except TimeoutException:
                        print("⚠️ Could not find text tool, skipping text addition")
                        break
            
            return True
            
        except Exception as e:
            print(f"❌ Text addition failed: {e}")
            return False
    
    def save_design(self, filename=None):
        """Save and optionally download the design"""
        try:
            if not filename:
                filename = f"canva_design_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Try to rename the design first
            try:
                # Look for design name/title field
                title_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Untitled'], [data-testid*='title'], .design-title")
                title_field.clear()
                title_field.send_keys(filename)
                print(f"📝 Design renamed to: {filename}")
            except:
                print("⚠️ Could not rename design")
            
            # Look for share/download options
            try:
                share_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid*='share'], button[aria-label*='Share']")))
                share_btn.click()
                time.sleep(3)
                
                # Look for download option
                download_btn = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid*='download'], a[href*='download'], button:contains('Download')")
                download_btn.click()
                time.sleep(3)
                
                print(f"✅ Design saved and download initiated: {filename}")
                return True
                
            except:
                print("⚠️ Could not find download option")
                print("💡 Design is saved in your Canva account")
                return True
                
        except Exception as e:
            print(f"❌ Save operation failed: {e}")
            return False
    
    def close(self):
        """Clean up and close browser"""
        if self.driver:
            self.driver.quit()
            print("🔄 Browser closed")

def main():
    parser = argparse.ArgumentParser(description="Canva CLI - Automated Design Creation")
    parser.add_argument("--type", default="presentation", choices=["presentation", "poster", "social", "custom"], help="Design type")
    parser.add_argument("--template", default="", help="Template search term")
    parser.add_argument("--text", nargs='+', help="Text content to add")
    parser.add_argument("--filename", help="Save filename")
    parser.add_argument("--keep-open", action="store_true", help="Keep browser open")
    
    args = parser.parse_args()
    
    print("🎨 Canva CLI - Automated Design Creation")
    print("=" * 50)
    
    canva = CanvaCLI()
    
    try:
        # Setup
        if not canva.setup_driver():
            print("❌ Failed to setup browser")
            return
        
        # Login
        if not canva.login():
            print("❌ Failed to login")
            return
        
        # Create design
        if not canva.create_design(args.type, args.template):
            print("❌ Failed to create design")
            return
        
        # Add text if provided
        if args.text:
            canva.add_text_to_design(args.text)
        
        # Save design
        canva.save_design(args.filename)
        
        print("✅ Canva CLI process completed successfully!")
        
        if args.keep_open:
            input("Press Enter to close browser...")
        
    except KeyboardInterrupt:
        print("\n⏹️ Process interrupted")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if not args.keep_open:
            canva.close()

if __name__ == "__main__":
    main()
