import os
import shutil
import pandas as pd

# Define the base directory and the path to the spreadsheet
BASE_DIR = "/workspaces/lcwebsiteAnalytics/existingWebpages"
SPREADSHEET_PATH = "/workspaces/lcwebsiteAnalytics/backlinks_report.xlsx"

def update_notes_file(folder_path, message):
    """ Update or create notes.md in the specified folder with a given message. """
    notes_path = os.path.join(folder_path, "notes.md")
    if not os.path.exists(notes_path):
        with open(notes_path, 'w', encoding='utf-8') as file:
            file.write("# Notes\n")
    with open(notes_path, 'a', encoding='utf-8') as file:
        file.write(message + "\n")
    print(f"Updated notes.md in {folder_path}")

def move_folder_to_backlink(base_dir, folder_name, target_folder_name):
    """ Move the specified folder to the directory of its backlink. """
    folder_path = os.path.join(base_dir, folder_name)
    target_folder_path = os.path.join(base_dir, target_folder_name)
    if os.path.exists(target_folder_path) and os.path.isdir(folder_path):
        new_path = os.path.join(target_folder_path, os.path.basename(folder_path))
        shutil.move(folder_path, new_path)
        print(f"Moved {folder_path} to {new_path}")
        update_notes_file(new_path, f"Moved to {new_path} from {folder_path}")
        update_notes_file(target_folder_path, f"Subfolder {folder_name} moved here from {folder_path}")
        return True
    else:
        print(f"Target folder {target_folder_path} does not exist or source folder {folder_path} does not exist.")
    return False

def process_folders_with_single_backlink(base_dir, spreadsheet_path):
    try:
        df = pd.read_excel(spreadsheet_path)
        # Ensure required columns are present
        required_columns = ['Folder Name', 'Number of Backlinks', 'First Backlink']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"One or more required columns are missing: {required_columns}")

        # Process rows where the number of backlinks is exactly one
        for index, row in df[df['Number of Backlinks'] == 1].iterrows():
            folder_name = row['Folder Name']
            first_backlink = row['First Backlink']
            backlink_folder_name = first_backlink.split('/')[-1]  # Assuming the URL segment or path logic holds
            if move_folder_to_backlink(base_dir, folder_name, backlink_folder_name):
                print(f"Successfully moved {folder_name} to {backlink_folder_name}")
            else:
                print(f"Failed to move {folder_name} to {backlink_folder_name}")
    except Exception as e:
        print(f"Error processing folders: {e}")

if __name__ == "__main__":
    process_folders_with_single_backlink(BASE_DIR, SPREADSHEET_PATH)