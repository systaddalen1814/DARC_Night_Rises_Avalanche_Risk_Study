import os
import shutil

def copy_files(src_folder, dest_folder):
    """Copies all files from src_folder to dest_folder."""
    if not os.path.exists(src_folder):
        print(f"Source folder '{src_folder}' does not exist.")
        return
    
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    for file_name in os.listdir(src_folder):
        src_file = os.path.join(src_folder, file_name)
        dest_file = os.path.join(dest_folder, file_name)
        
        if os.path.isfile(src_file):
            shutil.copy2(src_file, dest_file)
            print(f"Copied: {src_file} -> {dest_file}")
    
    print("All files copied successfully.")


source_folder = os.path.join(os.path.dirname(__file__), "..", "..", "2_DataCombination", "24_product")
destination_folder = os.path.join(os.path.dirname(__file__))

copy_files(source_folder, destination_folder)
