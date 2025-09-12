import os
import shutil

def organize_mds(source_dir, output_dir):

    # This part creates an output directory if it doesn't exist.
    os.makedirs(output_dir, exist_ok=True)
    
    # Responsible for traversing all directories and files in source_dir
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith('.md'):
                # what is the parent folder name?
                folder_name = os.path.basename(root)
                
                # Generation of new filename with the folder name of the Zotero item prepended to it
                new_filename = f"{folder_name}_{file}"
                
                # Creating paths for source and destination for final copying
                src_path = os.path.join(root, file)
                dst_path = os.path.join(output_dir, new_filename)
                
                # Copying over the file from the everything-folder to the output folder on my laptop
                try:
                    shutil.copy2(src_path, dst_path)
                    print(f"Copied: {src_path} -> {dst_path}")
                except Exception as e:
                    print(f"Error copying {src_path}: {e}")

if __name__ == "__main__":
    # Setting the source and output directory addresses here.
    source_directory = "D:\\minerU_outputs"
    output_directory = "D:\\mineru_mds_sorted_by_script"

    organize_mds(source_directory, output_directory)
    print("MD organization complete!")