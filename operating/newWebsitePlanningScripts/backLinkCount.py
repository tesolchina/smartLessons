import os
import pandas as pd

# Paths for source directories
BASE_DIR = "/workspaces/lcwebsiteAnalytics/existingWebpages"

def extract_folder_url(folder_name):
    """
    Generate the URL for a folder based on its name.
    Assumes the folder name corresponds to the URL path.
    """
    return f"https://lc.hkbu.edu.hk/main/{folder_name}/"

def find_backlinks(base_dir, folder_name, folder_url):
    """
    Find backlinks to a folder's URL in all other content.html files in the base directory.
    """
    backlinks = []
    for other_folder in os.listdir(base_dir):
        other_folder_path = os.path.join(base_dir, other_folder)
        if not os.path.isdir(other_folder_path) or other_folder == folder_name:
            continue

        # Check content.html in the other folder
        content_path = os.path.join(other_folder_path, "content.html")
        if not os.path.exists(content_path):
            continue

        with open(content_path, "r", encoding="utf-8") as file:
            content = file.read()
            if folder_url in content:
                backlinks.append(extract_folder_url(other_folder))
    return backlinks

def gather_data(base_dir):
    """
    Gather data from all folders and prepare for spreadsheet.
    """
    data = []
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        folder_url = extract_folder_url(folder_name)
        backlinks = find_backlinks(base_dir, folder_name, folder_url)
        # Prepare data for the current folder
        first_two_backlinks = backlinks[:2]
        row = {
            "Folder Name": folder_name,
            "Folder URL": folder_url,
            "Number of Backlinks": len(backlinks),
            "First Backlink": first_two_backlinks[0] if len(first_two_backlinks) > 0 else "",
            "Second Backlink": first_two_backlinks[1] if len(first_two_backlinks) > 1 else ""
        }
        data.append(row)
    return data

def create_spreadsheet(data, filename="backlinks_report.xlsx"):
    """
    Create a spreadsheet from the gathered data.
    """
    df = pd.DataFrame(data)
    # Write the DataFrame to an Excel file
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    print(f"Spreadsheet created: {filename}")

if __name__ == "__main__":
    # Gather data
    data = gather_data(BASE_DIR)
    # Create spreadsheet
    create_spreadsheet(data)