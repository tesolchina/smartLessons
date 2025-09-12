import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import pandas as pd

def parse_sitemap_to_dataframe(file_path):
    """
    Parse the XML sitemap file and convert it into a pandas DataFrame.
    Extracts URL, hierarchy, depth, and last modified date.
    """
    try:
        # Load and parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame

    # Namespace handling
    namespaces = {
        'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'image': 'http://www.google.com/schemas/sitemap-image/1.1'
    }

    # List to hold all URLs and their details
    urls = []

    # Iterate through each URL entry in the sitemap
    for i, url_elem in enumerate(root.findall('ns:url', namespaces)):
        try:
            # Extract the URL
            loc = url_elem.find('ns:loc', namespaces).text
            parsed_url = urlparse(loc)
            path = parsed_url.path

            # Split path to determine hierarchy
            path_parts = [part for part in path.split('/') if part]
            hierarchy = ' > '.join(path_parts)

            # Extract additional metadata (e.g., lastmod)
            lastmod_elem = url_elem.find('ns:lastmod', namespaces)
            lastmod = lastmod_elem.text if lastmod_elem is not None else "N/A"

            # Append URL and its hierarchy to the list
            urls.append({
                "URL": loc,
                "Hierarchy": hierarchy,
                "Depth": len(path_parts),
                "Last Modified": lastmod
            })

            # Log progress every 100 URLs
            if i % 100 == 0:
                print(f"Processed {i} URLs...")

        except Exception as e:
            print(f"Error processing URL element: {e}")

    # Convert list to DataFrame
    df = pd.DataFrame(urls)
    return df

# File path to the XML sitemap
file_path = "/workspaces/lcwebsiteAnalytics/page-sitemap_backup.xml"

# Parse the sitemap and get data as a DataFrame
df = parse_sitemap_to_dataframe(file_path)

# Verify data was extracted
if not df.empty:
    # Save to CSV
    df.to_csv("sitemap_urls.csv", index=False)

    # Save to Excel
    df.to_excel("sitemap_urls.xlsx", index=False)

    # Save to JSON
    df.to_json("sitemap_urls.json", orient="records", indent=2)

    print("Files have been saved: sitemap_urls.csv, sitemap_urls.xlsx, and sitemap_urls.json")
else:
    print("No data extracted from the sitemap.")