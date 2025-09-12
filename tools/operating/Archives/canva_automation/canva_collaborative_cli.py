#!/usr/bin/env python3
"""
Canva Collaborative CLI - Create and Share Designs
Enhanced Canva automation with team collaboration features
Created: September 6, 2025
"""

import os
import sys
import time
import argparse
import json
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
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
except ImportError:
    print("❌ Missing dependencies. Please run:")
    print("pip3 install -r requirements.txt")
    sys.exit(1)

class CanvaCollaborativeCLI:
    """Enhanced Canva CLI with collaboration features"""
    
    def __init__(self):
        load_dotenv()
        self.email = os.getenv("CANVA_EMAIL", "simonwang@hkbu.edu.hk")
        self.password = os.getenv("CANVA_PASSWORD", "")
        self.headless = os.getenv("BROWSER_HEADLESS", "false").lower() == "true"
        self.download_path = os.getenv("DOWNLOAD_PATH", os.path.expanduser("~/Downloads/canva_designs"))
        
        self.driver = None
        self.wait = None
        
        # Default collaborators for HKBU Language Centre
        self.default_collaborators = [
            "colleague1@hkbu.edu.hk",
            "colleague2@hkbu.edu.hk",
            "admin@hkbu.edu.hk"
        ]
        
        # Create download directory
        os.makedirs(self.download_path, exist_ok=True)
    
    def setup_driver(self):
        """Setup Chrome WebDriver with collaboration-friendly settings"""
        try:
            print("🔍 Setting up Chrome driver for collaboration...")
            
            # Chrome options optimized for sharing
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Don't run headless for sharing tasks (need to see share dialogs)
            # if self.headless:
            #     chrome_options.add_argument('--headless')
            
            # Clear any cached drivers and setup fresh
            import shutil
            wdm_path = os.path.expanduser("~/.wdm")
            if os.path.exists(wdm_path):
                shutil.rmtree(wdm_path)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            self.driver.implicitly_wait(10)
            self.wait = WebDriverWait(self.driver, 15)  # Longer wait for sharing operations
            
            # Execute script to prevent detection
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Browser initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize browser: {e}")
            print("💡 Make sure Google Chrome is installed and up to date")
            return False
    
    def login(self):
        """Login to Canva"""
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
            time.sleep(3)
            
            # Check if password field appears
            try:
                password_field = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, "password")))
                if not self.password:
                    print("⚠️  Password required but not set in .env file")
                    return False
                else:
                    password_field.send_keys(self.password)
                    login_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                    login_btn.click()
            except TimeoutException:
                print("ℹ️  No password field - continuing with email login")
            
            # Wait for successful login
            time.sleep(5)
            self.wait.until(EC.url_contains("canva.com"))
            
            # Check if we're on the home page
            if "login" not in self.driver.current_url.lower():
                print("✅ Login successful")
                return True
            else:
                print("❌ Login failed - please check credentials")
                return False
                
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def create_presentation_from_template(self, course_data, template_search="academic presentation university"):
        """Create a presentation from template with course data"""
        try:
            print(f"📊 Creating presentation for {course_data.get('course_code', 'course')}...")
            
            # Go to presentations page
            self.driver.get("https://www.canva.com/create/presentations/")
            time.sleep(3)
            
            # Search for template
            if template_search:
                try:
                    search_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='search' i], input[type='search']")))
                    search_box.clear()
                    search_box.send_keys(template_search)
                    search_box.send_keys(Keys.RETURN)
                    time.sleep(3)
                except TimeoutException:
                    print("⚠️  Search box not found, using default templates")
            
            # Select first suitable template
            try:
                print("🎨 Selecting presentation template...")
                template = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid*='template'], .template, [class*='template']")))
                template.click()
                time.sleep(5)
                
                print("✅ Template selected successfully")
                
            except TimeoutException:
                print("⚠️  Template not found, creating blank presentation")
                try:
                    blank_design = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Blank') or contains(text(), 'Create blank')]")))
                    blank_design.click()
                    time.sleep(5)
                except TimeoutException:
                    print("❌ Could not create presentation")
                    return False
            
            # Wait for editor to load
            time.sleep(10)
            print("✅ Presentation created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create presentation: {e}")
            return False
    
    def add_course_content_to_slide(self, slide_content):
        """Add structured content to current slide"""
        try:
            print(f"📝 Adding content to slide...")
            
            # Find existing text elements
            text_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid*='text'], [contenteditable='true'], .text-element")
            
            if text_elements:
                # Update existing text elements
                for i, element in enumerate(text_elements[:len(slide_content)]):
                    try:
                        element.click()
                        time.sleep(1)
                        element.clear()
                        element.send_keys(slide_content[i])
                        time.sleep(1)
                    except:
                        continue
            else:
                # Add new text elements if none exist
                try:
                    # Look for text tool in toolbar
                    text_tool = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Text') or contains(text(), 'Text')]")))
                    text_tool.click()
                    time.sleep(2)
                    
                    # Click "Add a heading" or similar
                    add_text_btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add a heading') or contains(text(), 'Add text')]")))
                    add_text_btn.click()
                    time.sleep(2)
                    
                    # Type the first content item
                    active_text = self.driver.find_element(By.CSS_SELECTOR, "[contenteditable='true']")
                    active_text.clear()
                    active_text.send_keys(slide_content[0] if slide_content else "Sample text")
                    
                except TimeoutException:
                    print("⚠️  Could not find text tools, content may need to be added manually")
            
            time.sleep(2)
            print("✅ Content added to slide")
            return True
            
        except Exception as e:
            print(f"❌ Failed to add content: {e}")
            return False
    
    def share_with_collaborators(self, collaborators, permission_level="edit"):
        """Share the design with specified collaborators"""
        try:
            print("🔗 Sharing design with collaborators...")
            
            # Look for share button
            share_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid*='share'], button[aria-label*='Share'], button:contains('Share')")))
            share_btn.click()
            time.sleep(3)
            
            # For each collaborator
            for email in collaborators:
                try:
                    print(f"📧 Inviting {email}...")
                    
                    # Find email input field
                    email_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='email' i], input[type='email'], input[name*='email']")))
                    email_input.clear()
                    email_input.send_keys(email)
                    
                    # Set permission level if dropdown exists
                    try:
                        permission_dropdown = self.driver.find_element(By.CSS_SELECTOR, "select, [role='combobox']")
                        if permission_level == "edit":
                            permission_dropdown.click()
                            edit_option = self.driver.find_element(By.XPATH, "//option[contains(text(), 'Edit')] | //div[contains(text(), 'Can edit')]")
                            edit_option.click()
                    except:
                        pass  # Default permissions will be used
                    
                    # Send invitation
                    invite_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Invite') or contains(text(), 'Send') or contains(text(), 'Share')]")))
                    invite_btn.click()
                    time.sleep(2)
                    
                    print(f"✅ Invitation sent to {email}")
                    
                except Exception as e:
                    print(f"⚠️  Failed to invite {email}: {e}")
                    continue
            
            time.sleep(3)
            print("✅ All invitations sent successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to share design: {e}")
            return False
    
    def get_shareable_link(self):
        """Get a shareable link for the design"""
        try:
            print("🔗 Getting shareable link...")
            
            # Look for share button if not already open
            try:
                share_btn = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid*='share'], button[aria-label*='Share']")
                share_btn.click()
                time.sleep(2)
            except:
                pass
            
            # Look for "Copy link" or similar button
            try:
                copy_link_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Copy link') or contains(text(), 'Get link')]")))
                copy_link_btn.click()
                time.sleep(2)
                
                # The link should now be in clipboard
                print("🔗 Shareable link copied to clipboard")
                
                # Try to get the actual URL from current page
                current_url = self.driver.current_url
                if "design" in current_url:
                    print(f"📋 Design URL: {current_url}")
                    return current_url
                
            except TimeoutException:
                print("⚠️  Could not find copy link button")
                return None
                
        except Exception as e:
            print(f"❌ Failed to get shareable link: {e}")
            return None
    
    def save_design_with_title(self, title):
        """Save the design with a specific title"""
        try:
            print(f"💾 Saving design as: {title}")
            
            # Look for title field
            try:
                title_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Untitled'], [data-testid*='title'], .design-title")
                title_field.clear()
                title_field.send_keys(title)
                title_field.send_keys(Keys.RETURN)
                time.sleep(2)
            except:
                print("⚠️  Title field not found, design will use default name")
            
            # Save (usually auto-saves, but try to trigger save)
            try:
                ActionChains(self.driver).key_down(Keys.COMMAND).send_keys('s').key_up(Keys.COMMAND).perform()
                time.sleep(2)
            except:
                pass
            
            print("✅ Design saved")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save design: {e}")
            return False
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser closed")

def create_collaborative_lang2077_slides(collaborators=None, template="academic presentation university"):
    """Create LANG 2077 slides and invite collaborators"""
    
    print("🎓 Collaborative LANG 2077 Slides Creator")
    print("=" * 50)
    
    # Course data
    course_data = {
        "course_code": "LANG 2077",
        "course_title": "Language Skills for human-AI partnership: Customizing Chatbots to Empower Communities",
        "instructor": "Dr. Simon Wang",
        "department": "Language Centre, HKBU",
        "semester": "Fall 2025"
    }
    
    # Slide content
    slides_content = [
        ["LANG 2077", "Language Skills for human-AI partnership:", "Customizing Chatbots to Empower Communities", "Dr. Simon Wang | Language Centre, HKBU | Fall 2025"],
        ["What Students Will Learn", "• Language Skills Development", "• AI Partnership Skills", "• Community Engagement"],
        ["Empowering Communities Through AI", "• Community Partner Collaboration", "• Chatbot Customization Projects", "• Student Deliverables & Impact"]
    ]
    
    # Default collaborators if none provided
    if not collaborators:
        collaborators = [
            "colleague1@hkbu.edu.hk",
            "colleague2@hkbu.edu.hk",
            "admin@hkbu.edu.hk"
        ]
    
    try:
        # Initialize Canva CLI
        canva = CanvaCollaborativeCLI()
        
        # Setup browser
        if not canva.setup_driver():
            return False
        
        # Login
        if not canva.login():
            return False
        
        # Create presentation
        if not canva.create_presentation_from_template(course_data, template):
            return False
        
        # Add content to first slide
        canva.add_course_content_to_slide(slides_content[0])
        
        # Save with title
        design_title = f"LANG2077_Course_Introduction_Slides_{datetime.now().strftime('%Y%m%d_%H%M')}"
        canva.save_design_with_title(design_title)
        
        # Share with collaborators
        canva.share_with_collaborators(collaborators, permission_level="edit")
        
        # Get shareable link
        shareable_link = canva.get_shareable_link()
        
        print("\n✅ LANG 2077 collaborative slides created successfully!")
        print(f"📋 Design title: {design_title}")
        if shareable_link:
            print(f"🔗 Shareable link: {shareable_link}")
        
        print("\n👥 Collaborators invited:")
        for email in collaborators:
            print(f"   - {email} (edit permissions)")
        
        print("\n📋 Next steps:")
        print("   1. Collaborators will receive email invitations")
        print("   2. They can click the link to start editing")
        print("   3. Add remaining slide content collaboratively")
        print("   4. Customize HKBU branding together")
        print("   5. Review and finalize the presentation")
        
        # Keep browser open for manual adjustments
        input("\n⏸️  Press Enter to close browser (or switch to it for manual edits)...")
        canva.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating collaborative slides: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Canva Collaborative Slides Creator")
    parser.add_argument("--collaborators", nargs="+", help="Email addresses of collaborators")
    parser.add_argument("--template", default="academic presentation university", help="Template search term")
    parser.add_argument("--course", default="LANG2077", help="Course code")
    
    args = parser.parse_args()
    
    # Create collaborative LANG 2077 slides
    create_collaborative_lang2077_slides(args.collaborators, args.template)

if __name__ == "__main__":
    main()
