import os
import shutil

# Paths for source and destination directories
BASE_DIR = "/workspaces/lcwebsiteAnalytics/existingWebpages"
DEST_DIR = "/workspaces/lcwebsiteAnalytics/OrganisedExistFolder/No_Back_Links"

def check_no_backlinks(notes_path):
    """
    Check if the 'notes.md' file contains 'No backlinks found'.
    """
    try:
        with open(notes_path, "r", encoding="utf-8") as file:
            notes_content = file.read()
            # Check if the backlinks section indicates no backlinks
            if "## Backlinks" in notes_content and "No backlinks found." in notes_content:
                return True
    except Exception as e:
        print(f"[ERROR] Failed to read {notes_path}: {e}")
    return False

def move_no_backlinks_folders(base_dir, dest_dir):
    """
    Move folders with no backlinks to the destination directory.
    """
    # Ensure the destination directory exists
    os.makedirs(dest_dir, exist_ok=True)

    # Counter for folders moved
    moved_count = 0

    # Iterate through all folders in the base directory
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)

        # Skip if it's not a folder
        if not os.path.isdir(folder_path):
            continue

        # Path to the notes.md file
        notes_path = os.path.join(folder_path, "notes.md")

        # Skip if notes.md does not exist
        if not os.path.exists(notes_path):
            print(f"[WARNING] notes.md not found in {folder_path}, skipping...")
            continue

        # Check if the folder has no backlinks
        if check_no_backlinks(notes_path):
            # Move the folder to the destination directory
            dest_folder_path = os.path.join(dest_dir, folder_name)
            shutil.move(folder_path, dest_folder_path)
            print(f"[INFO] Moved folder: {folder_name} -> {dest_folder_path}")
            moved_count += 1

    print(f"\n[INFO] Total folders moved: {moved_count}")

if __name__ == "__main__":
    # Move folders with no backlinks to the No_Back_Links folder
    move_no_backlinks_folders(BASE_DIR, DEST_DIR)