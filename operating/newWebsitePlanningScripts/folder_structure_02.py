import os

def read_url_mappings(file_path):
    """ Read the mappings from a markdown file and return a dictionary of folder names to URLs. """
    mappings = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip().startswith('URL:'):
                    url = line.split('URL:')[1].strip()
                    folder_name = url.split('/')[-2]  # Assuming URL format ends with /foldername/
                    mappings[folder_name] = url
    except FileNotFoundError:
        print("Mapping file not found.")
    return mappings

def check_folder_movements(base_dir, mappings):
    """ Check the current folders against the mappings and report any that have moved. """
    current_folders = {folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))}
    mapped_folders = set(mappings.keys())

    missing_folders = mapped_folders - current_folders
    new_folders = current_folders - mapped_folders

    if missing_folders:
        print("Folders that have moved or are missing:")
        for folder in missing_folders:
            print(f"{folder} mapped to {mappings[folder]}")
    
    if new_folders:
        print("New folders that are not mapped:")
        for folder in new_folders:
            print(folder)

if __name__ == "__main__":
    BASE_DIR = "/workspaces/lcwebsiteAnalytics/existingWebpages"
    MAPPING_FILE = "/workspaces/lcwebsiteAnalytics/existingWebpages/notes.md"
    url_mappings = read_url_mappings(MAPPING_FILE)
    check_folder_movements(BASE_DIR, url_mappings)