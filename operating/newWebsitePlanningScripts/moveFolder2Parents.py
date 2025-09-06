import os
import shutil
import pandas as pd

# Define the base directory and the path to the spreadsheet
BASE_DIR = "/workspaces/lcwebsiteAnalytics/existingWebpages"
SPREADSHEET_PATH = "/workspaces/lcwebsiteAnalytics/backlinks_report.xlsx"

def is_subfolder(parent, child):
    """ Check if child is a subfolder of parent based on URL structure. """
    parent_url = parent.replace(os.sep, '/')
    child_url = child.replace(os.sep, '/')
    return child_url.startswith(parent_url) and parent_url != child_url

def move_subfolder(parent_folder, subfolder):
    """ Move the subfolder into the parent folder. """
    new_path = os.path.join(parent_folder, os.path.basename(subfolder))
    shutil.move(subfolder, new_path)
    print(f"Moved {subfolder} to {new_path}")
    return new_path

def update_notes_file(folder_path, subfolder_name):
    """ Update notes.md in the specified folder with information about the subfolder. """
    notes_path = os.path.join(folder_path, "notes.md")
    note_content = f"Subfolder added: {subfolder_name}\n"
    if not os.path.exists(notes_path):
        with open(notes_path, 'w', encoding='utf-8') as file:
            file.write("# Notes\n")
            file.write(note_content)
    else:
        with open(notes_path, 'a', encoding='utf-8') as file:
            file.write(note_content)
    print(f"Updated notes.md in {folder_path}")

def update_spreadsheet(spreadsheet_path, parent_folder, subfolder_name):
    """ Update the Excel spreadsheet to reflect the changes in folder structure. """
    df = pd.read_excel(spreadsheet_path)
    filtered_df = df[df['Folder URL'].str.contains(os.path.basename(parent_folder))]

    if not filtered_df.empty:
        parent_index = filtered_df.index[0]
        if 'Subfolders' in df.columns:
            existing_subfolders = df.at[parent_index, 'Subfolders']
            updated_subfolders = f"{existing_subfolders}, {subfolder_name}" if pd.notna(existing_subfolders) else subfolder_name
            df.at[parent_index, 'Subfolders'] = updated_subfolders
        else:
            df['Subfolders'] = pd.NA  # Initialize the column if it doesn't exist
            df.at[parent_index, 'Subfolders'] = subfolder_name
        df.to_excel(spreadsheet_path, index=False)
        print(f"Updated spreadsheet {spreadsheet_path} with new subfolder info for {parent_folder}")
    else:
        print(f"No entries found in spreadsheet for {parent_folder}. Please check the 'Folder URL' column for correct entries.")

def process_folders(base_dir, spreadsheet_path):
    """ Process each folder to find and manage subfolder relationships. """
    folders = [os.path.join(base_dir, name) for name in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, name))]
    for parent_folder in folders:
        for subfolder in folders:
            if parent_folder != subfolder and is_subfolder(parent_folder, subfolder):
                new_path = move_subfolder(parent_folder, subfolder)
                update_notes_file(parent_folder, os.path.basename(new_path))
                update_spreadsheet(spreadsheet_path, parent_folder, os.path.basename(new_path))

if __name__ == "__main__":
    process_folders(BASE_DIR, SPREADSHEET_PATH)