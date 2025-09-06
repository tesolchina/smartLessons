import os
import pandas as pd

def generate_folder_report(base_dir, output_file, links_file):
    """ Generate a report of all folders and subfolders in the specified directory, including URLs. """
    data = []  # List to store the folder details
    folders_with_subfolders = []  # List to store URLs of folders with subfolders

    for root, dirs, files in os.walk(base_dir):
        # Process each directory
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            url = folder_path.replace(base_dir, "https://lc.hkbu.edu.hk/")

            data.append({
                "Folder Name": dir,
                "Path": folder_path,
                "URL": url
            })

            # Check if this directory contains subdirectories
            subdirs = next(os.walk(folder_path))[1]
            if subdirs:
                folders_with_subfolders.append(url)

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)

    # Write the DataFrame to an Excel file
    df.to_excel(output_file, index=False)
    print(f"Report generated: {output_file}")

    # Write folders with subfolders to a text file
    with open(links_file, 'w') as file:
        for url in folders_with_subfolders:
            file.write(url + '\n')
    print(f"URLs of folders with subfolders written to: {links_file}")

if __name__ == "__main__":
    BASE_DIR = "/workspaces/lcwebsiteAnalytics/existingWebpages"  # Adjust as necessary
    OUTPUT_FILE = "folder_structure_report.xlsx"
    LINKS_FILE = "/workspaces/lcwebsiteAnalytics/existingWebpages/links.txt"
    generate_folder_report(BASE_DIR, OUTPUT_FILE, LINKS_FILE)