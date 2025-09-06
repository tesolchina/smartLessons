import os
import shutil

# Paths for source and destination folders
BASE_DIR = "/workspaces/lcwebsiteAnalytics/existingWebpages"
DEST_DIR = "/workspaces/lcwebsiteAnalytics/OrganisedExistFolder/staff"

def move_folders_based_on_title(base_dir, dest_dir, keyword="Staff"):
    """
    Read the notes.md file in each folder and move folders with the specified keyword in the Title.
    """
    # Ensure the destination directory exists
    os.makedirs(dest_dir, exist_ok=True)

    # Iterate through all folders in the base directory
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)

        # Skip if it's not a folder
        if not os.path.isdir(folder_path):
            continue

        # Path to the notes.md file
        notes_file_path = os.path.join(folder_path, "notes.md")

        # Skip if notes.md does not exist
        if not os.path.exists(notes_file_path):
            print(f"[WARNING] notes.md not found in {folder_path}, skipping...")
            continue

        # Read the notes.md file
        try:
            with open(notes_file_path, "r", encoding="utf-8") as notes_file:
                notes_content = notes_file.read()

                # Check if the Title contains the specified keyword
                if f"Title: {keyword}" in notes_content:
                    # Move the folder to the destination directory
                    dest_folder_path = os.path.join(dest_dir, folder_name)
                    shutil.move(folder_path, dest_folder_path)
                    print(f"[INFO] Moved folder: {folder_name} -> {dest_folder_path}")
        except Exception as e:
            print(f"[ERROR] Failed to process {notes_file_path}: {e}")

if __name__ == "__main__":
    # Move folders with "Staff" in the Title to the destination directory
    move_folders_based_on_title(BASE_DIR, DEST_DIR)