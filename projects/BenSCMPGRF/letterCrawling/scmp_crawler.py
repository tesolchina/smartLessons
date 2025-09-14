"""
Web crawler for SCMP Letters to the Editor
Fetches letters from https://www.scmp.com/comment/letters
Not behind paywall. Intended for regular (e.g. weekly) crawling.
"""
import requests
from bs4 import BeautifulSoup
import datetime
import os
import time
import json

BASE_URL = "https://www.scmp.com/comment/letters"
OUTPUT_DIR = "scmp_letters_output"


def fetch_letters_page(url=BASE_URL):
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def fetch_letter_content(url):
    """Fetch the full content of an individual letter"""
    from bs4 import Tag
    full_url = f"https://www.scmp.com{url}" if url.startswith('/') else url
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        resp = requests.get(full_url, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Extract letter content using multiple strategies
        content = ""
        
        # Strategy 1: Look for all paragraphs and filter for content
        all_paragraphs = soup.find_all("p")
        content_paragraphs = []
        
        for p in all_paragraphs:
            text = p.get_text(strip=True)
            # Filter out short paragraphs, navigation, ads, etc.
            if (len(text) > 30 and 
                not any(skip_word in text.lower() for skip_word in [
                    'advertisement', 'subscribe', 'cookie', 'privacy policy', 
                    'terms of service', 'newsletter', 'follow us', 'share',
                    'reading time:', 'published:', 'feel strongly about these letters'
                ])):
                content_paragraphs.append(text)
        
        # Take the substantial middle paragraphs (skip first few and last few which might be metadata)
        if len(content_paragraphs) > 4:
            content = "\n\n".join(content_paragraphs[2:-2])
        elif len(content_paragraphs) > 0:
            content = "\n\n".join(content_paragraphs)
        
        # Strategy 2: If no content found, try to get all text and clean it
        if not content:
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text from the page
            page_text = soup.get_text()
            lines = [line.strip() for line in page_text.splitlines() if line.strip()]
            
            # Find content between header and footer patterns
            content_lines = []
            in_content = False
            for line in lines:
                if "letters@scmp.com" in line.lower() or "google form" in line.lower():
                    in_content = True
                    continue
                elif ("subscribe" in line.lower() or "privacy policy" in line.lower() or 
                      "advertisement" in line.lower()):
                    break
                elif in_content and len(line) > 30:
                    content_lines.append(line)
            
            if content_lines:
                content = "\n\n".join(content_lines)
        
        # Extract publication date
        date_elem = soup.find("time")
        pub_date = ""
        if date_elem and isinstance(date_elem, Tag):
            pub_date = date_elem.get("datetime", "")
        
        # Extract author if available
        author = ""
        byline = soup.find("div", class_="byline") or soup.find("span", class_="author")
        if byline:
            author = byline.get_text(strip=True)
        
        return {
            "content": content,
            "publication_date": pub_date,
            "author": author,
            "url": full_url
        }
    except Exception as e:
        print(f"Error fetching {full_url}: {e}")
        return {
            "content": "",
            "publication_date": "",
            "author": "",
            "url": full_url,
            "error": str(e)
        }


def parse_letters(html):
    soup = BeautifulSoup(html, "html.parser")
    import re
    letters = []
    # Find all anchor tags that link to /opinion/letters/article/
    from bs4 import Tag
    for a in soup.find_all("a", href=re.compile(r"/opinion/letters/article/\d+")):
        if isinstance(a, Tag):
            link = a.get("href", "")
            title = a.get_text(strip=True)
            summary = ""
            parent = a.parent
            if parent:
                next_sib = parent.find_next_sibling()
                if next_sib and isinstance(next_sib, Tag) and next_sib.name == "p":
                    summary = next_sib.get_text(strip=True)
                elif isinstance(parent, Tag) and parent.name == "p":
                    summary = parent.get_text(strip=True)
            letters.append({
                "title": title,
                "link": link,
                "summary": summary
            })
    return letters


def save_letters(letters, output_dir=OUTPUT_DIR):
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.date.today().isoformat()
    out_path = os.path.join(output_dir, f"letters_{date_str}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(letters, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(letters)} letters to {out_path}")


def main():
    print("Fetching letters list from SCMP...")
    html = fetch_letters_page()
    letters = parse_letters(html)
    print(f"Found {len(letters)} letters")
    
    # Test with first 3 letters only for debugging
    test_letters = letters[:3]
    print(f"Testing with first {len(test_letters)} letters...")
    
    # Fetch content for each letter
    for i, letter in enumerate(test_letters):
        print(f"Fetching letter {i+1}/{len(test_letters)}: {letter['title'][:50]}...")
        letter_data = fetch_letter_content(letter['link'])
        letter.update(letter_data)
        
        # Show a preview of the content
        if letter_data['content']:
            preview = letter_data['content'][:200] + "..." if len(letter_data['content']) > 200 else letter_data['content']
            print(f"  Content preview: {preview}")
        else:
            print(f"  No content extracted")
        
        # Be respectful to the server - add a small delay
        time.sleep(2)
    
    # Save test results
    date_str = datetime.date.today().isoformat()
    test_output_path = os.path.join(OUTPUT_DIR, f"test_letters_{date_str}.json")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(test_output_path, "w", encoding="utf-8") as f:
        json.dump(test_letters, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(test_letters)} test letters to {test_output_path}")


if __name__ == "__main__":
    main()
