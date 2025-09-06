import os
import requests
from bs4 import BeautifulSoup

# Path to the text file with links
TEXT_FILE_PATH = "/workspaces/lcwebsiteAnalytics/existingWebpages/links.txt"

# Base directory to save all folders and files
BASE_DIR = "/workspaces/lcwebsiteAnalytics/existingWebpages"

def create_folder_for_link(base_dir, link):
    """
    Create a folder for the given link. The folder name is the last part of the URL.
    """
    # Extract the last part of the URL to use as the folder name
    folder_name = link.rstrip('/').split('/')[-1]
    folder_path = os.path.join(base_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def extract_metadata_and_links(html_content, url):
    """
    Extract metadata, links, and text content from the HTML page.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract title
    title = soup.title.string.strip() if soup.title else "No title"

    # Extract meta tags
    meta_tags = []
    for meta in soup.find_all("meta"):
        meta_name = meta.get("name", "N/A")
        meta_content = meta.get("content", "N/A")
        meta_tags.append(f"{meta_name}: {meta_content}")

    # Extract all links in the page
    links = []
    for a_tag in soup.find_all("a", href=True):
        links.append(a_tag["href"])

    # Extract readable text content
    text_content = soup.get_text(separator="\n").strip()

    return {
        "title": title,
        "meta_tags": meta_tags,
        "links": links,
        "text_content": text_content
    }

def save_markdown_file(folder_path, url, metadata, has_more_links, has_text_content):
    """
    Save a notes.md file in the folder with tags for categorization and metadata.
    """
    notes_file_path = os.path.join(folder_path, "notes.md")
    with open(notes_file_path, "w", encoding="utf-8") as notes_file:
        notes_file.write(f"# Notes\n")
        notes_file.write(f"- URL: {url}\n")
        notes_file.write(f"- Title: {metadata['title']}\n")
        notes_file.write(f"- has_more_links: {has_more_links}\n")
        notes_file.write(f"- has_text_content: {has_text_content}\n")
        notes_file.write("\n## Metadata\n")
        for meta in metadata["meta_tags"]:
            notes_file.write(f"- {meta}\n")
        notes_file.write("\n## Links Found\n")
        for link in metadata["links"]:
            notes_file.write(f"- {link}\n")
        notes_file.write("\n## Text Content\n")
        notes_file.write(metadata["text_content"][:1000])  # Limit to first 1000 characters for brevity
    print(f"[INFO] Markdown file created: {notes_file_path}")

def fetch_and_save_html(link, folder_path):
    """
    Fetch the HTML content of a link and save it as content.html in the folder.
    """
    try:
        print(f"[INFO] Fetching HTML for: {link}")
        response = requests.get(link, timeout=10)
        response.raise_for_status()
        html_file_path = os.path.join(folder_path, "content.html")
        with open(html_file_path, "w", encoding="utf-8") as html_file:
            html_file.write(response.text)
        print(f"[SUCCESS] HTML content saved: {html_file_path}")
        return response.text  # Return the HTML content for further processing
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch {link}: {e}")
        return None

def process_links(file_path, base_dir):
    """
    Read links from the text file and process them into folders.
    """
    total_links = 0
    failed_links = 0

    with open(file_path, "r", encoding="utf-8") as file:
        links = file.readlines()

    print(f"[INFO] Total links to process: {len(links)}")

    for i, line in enumerate(links, start=1):
        # Skip empty lines
        link = line.strip()
        if not link:
            continue

        print(f"\n[INFO] Processing link {i}/{len(links)}: {link}")

        # Create a folder for the link
        folder_path = create_folder_for_link(base_dir, link)

        # Fetch the HTML content
        html_content = fetch_and_save_html(link, folder_path)
        if not html_content:
            print(f"[ERROR] Skipping {link} due to fetch failure")
            failed_links += 1
            continue  # Skip if the page could not be fetched

        # Extract metadata, links, and text content
        metadata = extract_metadata_and_links(html_content, link)

        # Determine flags for `has_more_links` and `has_text_content`
        has_more_links = "true" if metadata["links"] else "false"
        has_text_content = "true" if metadata["text_content"] else "false"

        # Save metadata and categorization info to notes.md
        save_markdown_file(folder_path, link, metadata, has_more_links, has_text_content)

        # Increment the total links processed
        total_links += 1

    print(f"\n[INFO] Processing completed.")
    print(f"[INFO] Total links processed successfully: {total_links}")
    print(f"[INFO] Total links failed: {failed_links}")

if __name__ == "__main__":
    # Ensure the base directory exists
    os.makedirs(BASE_DIR, exist_ok=True)

    # Process the links from the text file
    process_links(TEXT_FILE_PATH, BASE_DIR)