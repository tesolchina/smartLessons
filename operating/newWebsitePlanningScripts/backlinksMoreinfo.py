import os
from bs4 import BeautifulSoup

# Path to the base directory containing folders
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

        try:
            with open(content_path, "r", encoding="utf-8") as file:
                content = file.read()
                # Check if the folder URL is referenced in the content
                if folder_url in content:
                    backlinks.append(extract_folder_url(other_folder))  # Store the URL of the referring page
        except Exception as e:
            print(f"[ERROR] Failed to read {content_path}: {e}")

    return backlinks

def update_notes_with_backlinks(folder_path, backlinks):
    """
    Update the notes.md file with backlink information under the # Notes section.
    """
    notes_path = os.path.join(folder_path, "notes.md")
    try:
        # Read the existing notes.md content
        with open(notes_path, "r", encoding="utf-8") as notes_file:
            notes_content = notes_file.readlines()

        # Find where the # Notes section ends
        notes_end_index = -1
        for i, line in enumerate(notes_content):
            if line.strip() == "# Notes":
                notes_end_index = i + 1
                break

        if notes_end_index == -1:
            print(f"[WARNING] # Notes section not found in {notes_path}, skipping...")
            return

        # Build the backlink info
        backlink_info = [
            f"- no. of backlinks: {len(backlinks)}\n"
        ]
        if backlinks:
            backlink_info.append("- list of backlinks:\n")
            for backlink in backlinks:
                backlink_info.append(f"  - {backlink}\n")
        else:
            backlink_info.append("- list of backlinks: None\n")

        # Insert the backlink info right after the # Notes section
        notes_content[notes_end_index:notes_end_index] = backlink_info

        # Write the updated content back to notes.md
        with open(notes_path, "w", encoding="utf-8") as notes_file:
            notes_file.writelines(notes_content)

        print(f"[INFO] Updated backlinks in {notes_path}")
    except Exception as e:
        print(f"[ERROR] Failed to update backlinks in {notes_path}: {e}")

def process_folders(base_dir):
    """
    Process each folder to find backlinks and update notes.md.
    """
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)

        # Skip if it's not a folder
        if not os.path.isdir(folder_path):
            continue

        # Skip if notes.md doesn't exist
        notes_path = os.path.join(folder_path, "notes.md")
        if not os.path.exists(notes_path):
            print(f"[WARNING] notes.md not found in {folder_path}, skipping...")
            continue

        # Assume the folder URL is the base folder_name
        folder_url = extract_folder_url(folder_name)

        # Find backlinks
        backlinks = find_backlinks(base_dir, folder_name, folder_url)

        # Update notes.md with backlink information
        update_notes_with_backlinks(folder_path, backlinks)

if __name__ == "__main__":
    # Process folders to find backlinks and update notes.md
    process_folders(BASE_DIR)