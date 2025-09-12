import xml.etree.ElementTree as ET
from graphviz import Digraph

def parse_sitemap(xml_file):
    """
    Parse the XML sitemap and extract a hierarchical structure.
    """
    try:
        # Parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Namespace to handle the XML tags
        ns = {
            'default': 'http://www.sitemaps.org/schemas/sitemap/0.9',
            'image': 'http://www.google.com/schemas/sitemap-image/1.1'
        }

        # Dictionary to store the hierarchy
        hierarchy = {}

        # Iterate over all <url> elements
        for url in root.findall('default:url', ns):
            # Extract the main URL
            loc = url.find('default:loc', ns).text

            # Extract associated images
            images = []
            for image in url.findall('image:image', ns):
                image_loc = image.find('image:loc', ns).text
                images.append(image_loc)

            # Add the URL and its images to the hierarchy
            hierarchy[loc] = images

        return hierarchy

    except Exception as e:
        print(f"Error parsing the XML file: {e}")
        return {}

def display_hierarchy(hierarchy):
    """
    Display the hierarchy in a tree-like format.
    """
    print("Hierarchical Structure of the Sitemap:")
    for url, images in hierarchy.items():
        print(f"URL: {url}")
        if images:
            print("  Associated Images:")
            for image in images:
                print(f"    - {image}")
        else:
            print("  No associated images.")
        print()

def visualize_hierarchy(hierarchy, output_file="sitemap_hierarchy"):
    """
    Generate a visual hierarchical map using Graphviz.
    """
    try:
        dot = Digraph()

        for url, images in hierarchy.items():
            dot.node(url, url)  # Add URL as a node
            for image in images:
                dot.node(image, image)  # Add image as a node
                dot.edge(url, image)  # Link URL to its images

        # Save the visualization as a PNG file
        dot.render(output_file, format='png', cleanup=True)
        print(f"Hierarchy visualization saved as '{output_file}.png'.")
    except Exception as e:
        print(f"Error generating visualization: {e}")

if __name__ == "__main__":
    # Path to the XML file
    xml_file = '/workspaces/lcwebsiteAnalytics/page-sitemap_backup.xml'

    # Parse the sitemap and generate the hierarchy
    print("Parsing sitemap XML file...")
    hierarchy = parse_sitemap(xml_file)

    if hierarchy:
        # Display the hierarchical structure
        display_hierarchy(hierarchy)

        # Visualize the hierarchy (optional)
        print("\nGenerating visual hierarchy map...")
        visualize_hierarchy(hierarchy)
    else:
        print("No hierarchy data found. Please check the XML file.")
