#!/usr/bin/env python3
"""
Canva Direct Creator - Focused on Slide Creation
Streamlined Canva automation for creating slides without collaboration complexity
Created: September 6, 2025
"""

import os
import sys
import time
import argparse
from datetime import datetime
from dotenv import load_dotenv

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("❌ Selenium not installed. Run: pip3 install selenium webdriver-manager")
    sys.exit(1)

class CanvaDirectCreator:
    """Simplified Canva automation focused on slide creation"""
    
    def __init__(self):
        load_dotenv()
        self.email = os.getenv("CANVA_EMAIL", "simonwang@hkbu.edu.hk")
        self.password = os.getenv("CANVA_PASSWORD", "")
        
        self.driver = None
        self.wait = None
        
        print(f"🎯 Canva Direct Creator - {self.email}")
    
    def setup_browser(self):
        """Setup Chrome browser for Canva"""
        try:
            print("🔧 Setting up browser...")
            
            # Chrome options
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--window-size=1400,900")
            
            # Clear webdriver cache
            import shutil
            wdm_path = os.path.expanduser("~/.wdm")
            if os.path.exists(wdm_path):
                shutil.rmtree(wdm_path)
            
            # Initialize driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.maximize_window()
            
            # Setup wait and remove automation flags
            self.wait = WebDriverWait(self.driver, 15)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Browser ready")
            return True
            
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
    
    def login_to_canva(self):
        """Login to Canva account"""
        try:
            print("🔐 Logging into Canva...")
            
            # Go to Canva login
            self.driver.get("https://www.canva.com/login")
            time.sleep(3)
            
            # Enter email
            email_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name='email']")))
            email_input.clear()
            email_input.send_keys(self.email)
            time.sleep(1)
            
            # Click continue/login button
            login_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'], button[data-testid='continueWithEmail']")))
            login_btn.click()
            time.sleep(3)
            
            # Handle password if required
            try:
                password_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password'], input[name='password']")))
                if self.password:
                    password_input.send_keys(self.password)
                    submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                    submit_btn.click()
                    time.sleep(3)
                else:
                    print("⏸️  Password required - please enter manually in browser")
                    input("Press Enter after logging in manually...")
            except TimeoutException:
                print("ℹ️  No password field - email login used")
            
            # Wait for dashboard
            time.sleep(5)
            current_url = self.driver.current_url.lower()
            if "canva.com" in current_url and "login" not in current_url:
                print("✅ Login successful")
                return True
            else:
                print("❌ Login may have failed - check browser")
                return False
                
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def create_presentation(self, template_search="academic presentation"):
        """Create a new presentation in Canva"""
        try:
            print("📊 Creating presentation...")
            
            # Navigate to presentations
            self.driver.get("https://www.canva.com/create/presentations/")
            time.sleep(4)
            
            # Search for template if specified
            if template_search:
                print(f"🔍 Searching for: {template_search}")
                try:
                    search_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Search' i], input[type='search'], input[aria-label*='search' i]")))
                    search_input.clear()
                    search_input.send_keys(template_search)
                    search_input.send_keys(Keys.RETURN)
                    time.sleep(3)
                except TimeoutException:
                    print("⚠️  Search box not found, using default templates")
            
            # Select a template
            try:
                print("🎨 Selecting template...")
                # Look for template thumbnails
                template = self.wait.until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR, 
                    "[data-testid*='template'], [class*='template'], [data-testid*='design'], img[alt*='template' i], div[role='button'] img"
                )))
                template.click()
                time.sleep(5)
                print("✅ Template selected")
                
            except TimeoutException:
                # Try creating blank presentation
                print("⚠️  No template found, creating blank presentation")
                try:
                    blank_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Blank') or contains(text(), 'Create blank')]")))
                    blank_btn.click()
                    time.sleep(5)
                except TimeoutException:
                    print("❌ Could not create presentation")
                    return False
            
            # Wait for editor to load
            print("⏳ Waiting for editor to load...")
            time.sleep(10)
            
            # Check if we're in the editor
            if "/design/" in self.driver.current_url:
                print("✅ Presentation created - editor loaded")
                return True
            else:
                print("⚠️  Editor may not have loaded properly")
                return True  # Continue anyway
                
        except Exception as e:
            print(f"❌ Failed to create presentation: {e}")
            return False
    
    def add_slide_content(self, slide_content):
        """Add content to the current slide"""
        try:
            print("📝 Adding slide content...")
            
            # Find text elements
            text_elements = self.driver.find_elements(By.CSS_SELECTOR, "[contenteditable='true'], [data-text-edit='true'], div[role='textbox']")
            
            if text_elements and len(slide_content) > 0:
                for i, element in enumerate(text_elements[:len(slide_content)]):
                    try:
                        # Click to focus
                        element.click()
                        time.sleep(1)
                        
                        # Clear and add content
                        element.clear()
                        element.send_keys(slide_content[i])
                        time.sleep(1)
                        
                        print(f"  ✓ Added: {slide_content[i][:50]}...")
                        
                    except Exception as e:
                        print(f"  ⚠️  Could not edit element {i}: {e}")
                        continue
                
                print("✅ Content added to slide")
                return True
            else:
                print("⚠️  No editable text elements found - content may need manual entry")
                return False
                
        except Exception as e:
            print(f"❌ Failed to add content: {e}")
            return False
    
    def rename_presentation(self, title):
        """Rename the presentation"""
        try:
            print(f"📝 Renaming presentation to: {title}")
            
            # Look for title input/button
            title_elements = [
                "input[placeholder*='Untitled' i]",
                "[data-testid*='title']",
                "button[aria-label*='title' i]",
                "h1[contenteditable='true']"
            ]
            
            for selector in title_elements:
                try:
                    title_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    title_element.click()
                    time.sleep(1)
                    title_element.clear()
                    title_element.send_keys(title)
                    title_element.send_keys(Keys.RETURN)
                    time.sleep(2)
                    print("✅ Title updated")
                    return True
                except:
                    continue
            
            print("⚠️  Could not find title element")
            return False
            
        except Exception as e:
            print(f"❌ Failed to rename: {e}")
            return False
    
    def wait_for_manual_editing(self):
        """Pause for manual editing"""
        print("⏸️  Browser ready for manual editing")
        print("📋 You can now:")
        print("   • Edit text content")
        print("   • Change colors and fonts")
        print("   • Add images and shapes")
        print("   • Duplicate slides")
        print("   • Apply HKBU branding")
        
        input("\nPress Enter when finished editing...")
    
    def close_browser(self):
        """Close the browser"""
        if self.driver:
            print("🔒 Closing browser")
            self.driver.quit()

def create_lang2077_slides():
    """Create LANG 2077 course slides in Canva"""
    
    print("🎓 LANG 2077 Slide Creator")
    print("=" * 40)
    
    # Slide content for LANG 2077
    slides_content = {
        "title": "LANG2077_Course_Introduction",
        "slide1": ["LANG 2077", "Language Skills for human-AI partnership", "Customizing Chatbots to Empower Communities"],
        "slide2": ["What Students Will Learn", "Language Skills • AI Partnership • Community Engagement"],
        "slide3": ["Empowering Communities Through AI", "Service Learning Projects"]
    }
    
    creator = CanvaDirectCreator()
    
    try:
        # Setup and login
        if not creator.setup_browser():
            return False
            
        if not creator.login_to_canva():
            return False
        
        # Create presentation
        if not creator.create_presentation("academic presentation university"):
            return False
        
        # Add content to first slide
        creator.add_slide_content(slides_content["slide1"])
        
        # Rename presentation
        creator.rename_presentation(slides_content["title"])
        
        # Wait for manual editing
        creator.wait_for_manual_editing()
        
        print("✅ LANG 2077 slides created successfully!")
        print("💡 Remember to:")
        print("   • Add HKBU logo")
        print("   • Apply burgundy/gold colors")
        print("   • Create additional slides")
        print("   • Save/export as needed")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    finally:
        creator.close_browser()

def main():
    parser = argparse.ArgumentParser(description="Canva Direct Slide Creator")
    parser.add_argument("--course", default="lang2077", help="Course to create slides for")
    parser.add_argument("--template", default="academic presentation university", help="Template search term")
    parser.add_argument("--manual", action="store_true", help="Pause for manual editing")
    
    args = parser.parse_args()
    
    if args.course.lower() == "lang2077":
        create_lang2077_slides()
    else:
        print(f"Creating slides for: {args.course}")
        # Could extend for other courses

if __name__ == "__main__":
    main()
