import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import pandas as pd

def parse_sitemap_to_dataframe(file_path):
    # Load and parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Namespace handling
    namespaces = {
        'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'image': 'http://www.google.com/schemas/sitemap-image/1.1'
    }

    # List to hold all URLs and their details
    urls = []

    # Iterate through each URL entry in the sitemap
    for url_elem in root.findall('ns:url', namespaces):
        loc = url_elem.find('ns:loc', namespaces).text
        parsed_url = urlparse(loc)
        path = parsed_url.path
        
        # Split path to determine hierarchy
        path_parts = [part for part in path.split('/') if part]
        hierarchy = ' > '.join(path_parts)
        
        # Append URL and its hierarchy to the list
        urls.append({
            "URL": loc,
            "Hierarchy": hierarchy,
            "Depth": len(path_parts)
        })

    # Convert list to DataFrame
    df = pd.DataFrame(urls)
    return df

# File path to the XML sitemap
file_path = "/workspaces/lcwebsiteAnalytics/page-sitemap_backup.xml"

# Parse the sitemap and get data as a DataFrame
df = parse_sitemap_to_dataframe(file_path)

# Save to CSV
df.to_csv("sitemap_urls.csv", index=False)

# Save to Excel
df.to_excel("sitemap_urls.xlsx", index=False)

print("Files have been saved: sitemap_urls.csv and sitemap_urls.xlsx")