import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
import pandas as pd

def parse_sitemap(xml_file):
    """
    Parse the sitemap XML file and extract URLs and associated images.
    """
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Namespace to handle the XML tags
    ns = {
        'default': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'image': 'http://www.google.com/schemas/sitemap-image/1.1'
    }

    # Extract data
    data = []
    for url in root.findall('default:url', ns):
        loc = url.find('default:loc', ns).text  # Get the main URL
        images = []
        for image in url.findall('image:image', ns):
            image_loc = image.find('image:loc', ns).text
            images.append(image_loc)
        data.append({'url': loc, 'images': images})
    return data

def fetch_metadata(url):
    """
    Fetch metadata (status code, title, and meta description) for a given URL.
    """
    try:
        response = requests.get(url, timeout=10)
        status_code = response.status_code

        # Parse the HTML content if the response is OK
        if status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string if soup.title else "No Title"
            description_tag = soup.find('meta', attrs={'name': 'description'})
            description = description_tag['content'] if description_tag else "No Description"
        else:
            title = "No Title"
            description = "No Description"

        return status_code, title, description
    except Exception as e:
        # Handle exceptions (e.g., timeout, connection error)
        return "Error", "Error", f"Error: {e}"

def generate_spreadsheet(data, output_file):
    """
    Generate a spreadsheet with URL, associated images, and metadata.
    """
    rows = []
    for entry in data:
        url = entry['url']
        images = ", ".join(entry['images'])  # Join images as a string
        status_code, title, description = fetch_metadata(url)  # Fetch metadata
        rows.append({
            'URL': url,
            'Associated Images': images,
            'HTTP Status': status_code,
            'Page Title': title,
            'Meta Description': description
        })

    # Create a DataFrame
    df = pd.DataFrame(rows)

    # Save to an Excel file
    df.to_excel(output_file, index=False)
    print(f"Spreadsheet saved as {output_file}")

if __name__ == "__main__":
    # Path to the XML file
    xml_file = '/workspaces/lcwebsiteAnalytics/page-sitemap_backup.xml'

    # Parse the sitemap
    print("Parsing sitemap XML file...")
    data = parse_sitemap(xml_file)

    # Generate the spreadsheet
    print("Generating spreadsheet with metadata...")
    output_file = 'sitemap_links.xlsx'
    generate_spreadsheet(data, output_file)