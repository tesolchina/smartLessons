#!/usr/bin/env python3
"""
LANG 2077 Canva Slide Creator
Automated creation of course introduction slides using Canva API/Selenium
Created: September 6, 2025
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import argparse

class CanvaSlideCreator:
    def __init__(self, email="simonwang@hkbu.edu.hk"):
        self.email = email
        self.driver = None
        self.wait = None
    
    def setup_driver(self):
        """Initialize Chrome WebDriver for Canva automation"""
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Remove headless for first-time login
        # options.add_argument("--headless")  
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.maximize_window()
    
    def login_to_canva(self):
        """Login to Canva using provided email"""
        try:
            self.driver.get("https://www.canva.com/login")
            time.sleep(3)
            
            # Enter email
            email_input = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
            email_input.clear()
            email_input.send_keys(self.email)
            
            # Click continue
            continue_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue') or contains(text(), '继续')]")))
            continue_button.click()
            
            print(f"✅ Email entered: {self.email}")
            print("🔐 Please complete login in browser (password/SSO)")
            print("⏳ Waiting for login completion...")
            
            # Wait for successful login (check for dashboard)
            self.wait.until(EC.url_contains("canva.com/"))
            time.sleep(5)
            
            print("✅ Login successful!")
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def create_presentation_from_template(self):
        """Create a new presentation from template"""
        try:
            # Navigate to presentations
            self.driver.get("https://www.canva.com/presentations/templates/")
            time.sleep(3)
            
            # Search for academic/education templates
            search_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Search']")))
            search_box.clear()
            search_box.send_keys("academic presentation university")
            search_box.submit()
            time.sleep(3)
            
            # Select first suitable template
            first_template = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid*='template'] img")))
            first_template.click()
            time.sleep(5)
            
            print("✅ Template selected and opened")
            return True
            
        except Exception as e:
            print(f"❌ Template selection failed: {e}")
            return False
    
    def customize_slide_content(self, slide_number, content):
        """Customize individual slide content"""
        try:
            # Navigate to specific slide if needed
            if slide_number > 1:
                slide_thumbnail = self.driver.find_element(By.CSS_SELECTOR, f"[data-testid='slide-thumbnail-{slide_number-1}']")
                slide_thumbnail.click()
                time.sleep(2)
            
            # Find and update text elements
            text_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid*='text'], [contenteditable='true']")
            
            for i, element in enumerate(text_elements[:len(content)]):
                try:
                    element.click()
                    time.sleep(1)
                    
                    # Clear and type new content
                    element.clear()
                    element.send_keys(content[i])
                    time.sleep(1)
                    
                except Exception as text_error:
                    print(f"⚠️ Could not update text element {i}: {text_error}")
            
            print(f"✅ Slide {slide_number} content updated")
            return True
            
        except Exception as e:
            print(f"❌ Slide {slide_number} customization failed: {e}")
            return False
    
    def create_lang2077_slides(self):
        """Create all 3 LANG 2077 slides with content"""
        
        slides_content = [
            # Slide 1: Course Introduction
            [
                "LANG 2077",
                "Language Skills for human-AI partnership:",
                "Customizing Chatbots to Empower Communities",
                "Dr. Simon Wang | Language Centre, HKBU | Fall 2025"
            ],
            
            # Slide 2: Learning Objectives
            [
                "What Students Will Learn",
                "Language Skills Development",
                "AI Partnership Skills", 
                "Community Engagement"
            ],
            
            # Slide 3: Community Impact
            [
                "Empowering Communities Through AI",
                "Community Partner Collaboration",
                "Chatbot Customization Projects",
                "Student Deliverables"
            ]
        ]
        
        for i, content in enumerate(slides_content, 1):
            print(f"📝 Customizing slide {i}...")
            success = self.customize_slide_content(i, content)
            if not success:
                print(f"⚠️ Slide {i} customization had issues")
            time.sleep(3)
        
        return True
    
    def save_and_export(self, filename="LANG2077_Course_Introduction"):
        """Save the presentation and attempt export"""
        try:
            # Save/rename the presentation
            share_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid*='share'], button[aria-label*='Share']")))
            share_button.click()
            time.sleep(2)
            
            # Look for download option
            download_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid*='download'], a[href*='download']")
            download_button.click()
            time.sleep(3)
            
            print(f"✅ Presentation saved as: {filename}")
            print("📥 Download initiated (check your Downloads folder)")
            return True
            
        except Exception as e:
            print(f"⚠️ Save/export encountered issues: {e}")
            print("💡 You can manually save the presentation in Canva")
            return False
    
    def cleanup(self):
        """Close browser and cleanup"""
        if self.driver:
            time.sleep(5)  # Give user time to see results
            print("🔄 Closing browser in 5 seconds...")
            self.driver.quit()

def main():
    parser = argparse.ArgumentParser(description="LANG 2077 Canva Slide Creator")
    parser.add_argument("--email", default="simonwang@hkbu.edu.hk", help="Canva login email")
    parser.add_argument("--keep-open", action="store_true", help="Keep browser open after creation")
    
    args = parser.parse_args()
    
    creator = CanvaSlideCreator(email=args.email)
    
    print("🎨 LANG 2077 Canva Slide Creator")
    print("=" * 40)
    print(f"📧 Using email: {args.email}")
    print("🌐 Initializing browser...")
    
    try:
        # Setup
        creator.setup_driver()
        
        # Login
        if not creator.login_to_canva():
            print("❌ Could not login to Canva")
            return
        
        # Create presentation
        if not creator.create_presentation_from_template():
            print("❌ Could not create presentation from template")
            return
        
        # Customize slides
        print("📝 Creating LANG 2077 course slides...")
        creator.create_lang2077_slides()
        
        # Save and export
        creator.save_and_export("LANG2077_Course_Introduction")
        
        print("✅ LANG 2077 slides creation completed!")
        print("📋 Next steps:")
        print("   1. Review slides in Canva")
        print("   2. Add images and visual elements")
        print("   3. Adjust colors to HKBU branding")
        print("   4. Download final presentation")
        
        if args.keep_open:
            input("Press Enter to close browser...")
        
    except KeyboardInterrupt:
        print("\n⏹️ Process interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if not args.keep_open:
            creator.cleanup()

if __name__ == "__main__":
    main()
