import os
import shutil

# Source and target directories
NO_BACK_LINKS_DIR = "/workspaces/lcwebsiteAnalytics/existingWebpages/OrganisedExistFolder/No_Back_Links"
STAFF_DIR = "/workspaces/lcwebsiteAnalytics/existingWebpages/OrganisedExistFolder/staff"
TARGET_DIR = "/workspaces/lcwebsiteAnalytics/existingWebpages"

def move_folders(source_dir, target_dir):
    """
    Move all folders from the source directory to the target directory.
    """
    moved_count = 0

    # Iterate through all folders in the source directory
    for folder_name in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder_name)

        # Skip if it's not a folder
        if not os.path.isdir(folder_path):
            continue

        # Move the folder to the target directory
        target_path = os.path.join(target_dir, folder_name)
        if os.path.exists(target_path):
            print(f"[WARNING] Target folder already exists: {target_path}, skipping...")
            continue

        shutil.move(folder_path, target_path)
        print(f"[INFO] Moved folder: {folder_name} -> {target_path}")
        moved_count += 1

    print(f"\n[INFO] Total folders moved from {source_dir}: {moved_count}")

if __name__ == "__main__":
    # Move folders from No_Back_Links
    print("[INFO] Moving folders from No_Back_Links...")
    move_folders(NO_BACK_LINKS_DIR, TARGET_DIR)

    # Move folders from staff
    print("[INFO] Moving folders from staff...")
    move_folders(STAFF_DIR, TARGET_DIR)