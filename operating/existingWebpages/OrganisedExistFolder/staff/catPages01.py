import os
import shutil
from bs4 import BeautifulSoup

# Paths for source and destination folders
BASE_DIR = "/workspaces/lcwebsiteAnalytics/existingWebpages"
DEST_DIR = "/workspaces/lcwebsiteAnalytics/OrganisedExistFolder"

# Website structure for categorization
CATEGORY_STRUCTURE = {
    "About Us": ["Mission", "Staff", "Job Vacancies", "Contact Us"],
    "Courses": ["English", "Chinese", "Putonghua", "Foreign Languages"],
    "Self-Regulated Learning": ["Examination", "Tutorial Services", "Activities", "Professional Development"],
    "Staff Corner": ["Leadership", "Research", "Staff Development", "Social"]
}

def extract_title_from_notes(notes_path):
    """
    Extract the Title from the notes.md file.
    """
    try:
        with open(notes_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("- Title:"):
                    return line.split(":")[1].strip()
    except Exception as e:
        print(f"[ERROR] Failed to read {notes_path}: {e}")
    return None

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
                if folder_url in content:  # Check if the folder URL is referenced
                    backlinks.append(other_folder)
        except Exception as e:
            print(f"[ERROR] Failed to read {content_path}: {e}")

    return backlinks

def update_notes_with_backlinks(folder_path, backlinks):
    """
    Update the notes.md file with backlinks.
    """
    notes_path = os.path.join(folder_path, "notes.md")
    try:
        with open(notes_path, "a", encoding="utf-8") as notes_file:
            notes_file.write("\n## Backlinks\n")
            if backlinks:
                for backlink in backlinks:
                    notes_file.write(f"- {backlink}\n")
            else:
                notes_file.write("No backlinks found.\n")
        print(f"[INFO] Backlinks updated in {notes_path}")
    except Exception as e:
        print(f"[ERROR] Failed to update backlinks in {notes_path}: {e}")

def categorize_folders(base_dir, dest_dir):
    """
    Categorize folders into the new website structure based on their Title.
    """
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)

        # Skip if it's not a folder
        if not os.path.isdir(folder_path):
            continue

        # Read the notes.md file
        notes_path = os.path.join(folder_path, "notes.md")
        if not os.path.exists(notes_path):
            print(f"[WARNING] notes.md not found in {folder_path}, skipping...")
            continue

        # Extract the Title
        title = extract_title_from_notes(notes_path)
        if not title:
            print(f"[WARNING] Title not found in {notes_path}, skipping...")
            continue

        # Determine the category based on the Title
        destination_folder = None
        for category, subcategories in CATEGORY_STRUCTURE.items():
            if title in subcategories:
                destination_folder = os.path.join(dest_dir, category, title)
                break

        if destination_folder:
            # Ensure the destination folder exists
            os.makedirs(destination_folder, exist_ok=True)

            # Move the folder to the destination
            dest_folder_path = os.path.join(destination_folder, folder_name)
            shutil.move(folder_path, dest_folder_path)
            print(f"[INFO] Moved folder: {folder_name} -> {dest_folder_path}")
        else:
            print(f"[WARNING] No matching category for Title: {title}, skipping...")

def process_folders(base_dir):
    """
    Process each folder to find backlinks and categorize them.
    """
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)

        # Skip if it's not a folder
        if not os.path.isdir(folder_path):
            continue

        # Read content.html to find backlinks
        content_path = os.path.join(folder_path, "content.html")
        if not os.path.exists(content_path):
            print(f"[WARNING] content.html not found in {folder_path}, skipping...")
            continue

        # Assume the folder URL is the base folder_name
        folder_url = f"/{folder_name}/"
        backlinks = find_backlinks(base_dir, folder_name, folder_url)

        # Update notes.md with backlinks
        update_notes_with_backlinks(folder_path, backlinks)

if __name__ == "__main__":
    # Ensure the destination directory exists
    os.makedirs(DEST_DIR, exist_ok=True)

    # Step 1: Process folders to find backlinks and update notes.md
    process_folders(BASE_DIR)

    # Step 2: Categorize folders into the new website structure
    categorize_folders(BASE_DIR, DEST_DIR)