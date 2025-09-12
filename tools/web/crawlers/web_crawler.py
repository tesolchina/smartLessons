import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from docx import Document

def create_folder_structure(base_path, url):
    """
    Create a folder structure that reflects the URL hierarchy.
    """
    parsed_url = urlparse(url)
    path = parsed_url.path.strip('/')
    folder_path = os.path.join(base_path, path.replace('/', os.sep))
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def save_to_word(folder_path, filename, text):
    """
    Save the extracted text into a Word document.
    """
    file_path = os.path.join(folder_path, f"{filename}.docx")
    document = Document()
    document.add_paragraph(text)
    document.save(file_path)
    print(f"Saved Word document: {file_path}")

def fetch_text_from_url(url):
    """
    Fetch the HTML content of a URL and extract meaningful text.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract meaningful text (e.g., <p>, <h1>, <h2>, etc.)
        text = ""
        for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):
            text += tag.get_text(strip=True) + "\n"

        return text
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return ""

def is_valid_url(base_url, link):
    """
    Check if a link is valid and belongs to the same domain as the base URL.
    """
    full_url = urljoin(base_url, link)
    parsed_base = urlparse(base_url)
    parsed_link = urlparse(full_url)
    return parsed_link.netloc == parsed_base.netloc and parsed_link.scheme in ['http', 'https']

def crawl_website(base_url, base_path, visited=None, progress_count=0):
    """
    Crawl the website starting from the base URL and save pages as Word documents.
    """
    if visited is None:
        visited = set()

    # If we've already visited this URL, skip it
    if base_url in visited:
        return progress_count
    visited.add(base_url)

    # Print progress update
    progress_count += 1
    print(f"[{progress_count}] Crawling: {base_url}")

    # Fetch text content from the current page
    text = fetch_text_from_url(base_url)
    if text:
        folder_path = create_folder_structure(base_path, base_url)
        save_to_word(folder_path, "index", text)

    # Parse links on the current page
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links on the page
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)

            # Check if the link is valid and belongs to the same domain
            if is_valid_url(base_url, href) and full_url not in visited:
                progress_count = crawl_website(full_url, base_path, visited, progress_count)
    except Exception as e:
        print(f"Failed to crawl {base_url}: {e}")

    return progress_count

if __name__ == "__main__":
    # Base URL to start crawling
    base_url = "https://lc.hkbu.edu.hk/main/"

    # Base folder path to save Word documents
    base_path = "/workspaces/lcwebsiteAnalytics/.vscode/results"

    # Start crawling
    print("Starting crawl...")
    os.makedirs(base_path, exist_ok=True)
    total_pages = crawl_website(base_url, base_path)
    print(f"Crawling complete. Total pages crawled: {total_pages}")