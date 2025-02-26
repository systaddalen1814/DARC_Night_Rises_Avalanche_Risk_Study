import os
import pandas as pd

def clean_and_copy_csv(src_folder, dest_folder):
    """Copies CSV files from src_folder to dest_folder after removing rows with missing data.
       Skips files if they become empty after cleaning.
    """
    
    if not os.path.exists(src_folder):
        print(f"Source folder '{src_folder}' does not exist.")
        return
    
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    for file_name in os.listdir(src_folder):
        src_file = os.path.join(src_folder, file_name)

        # Process only CSV files
        if os.path.isfile(src_file) and file_name.lower().endswith('.csv'):
            try:
                # Load CSV, drop missing data
                df = pd.read_csv(src_file)
                df_cleaned = df.dropna()  # Remove rows with missing values
                
                # Skip if DataFrame is empty after cleaning
                if df_cleaned.empty:
                    print(f"Skipping {file_name} (all rows were removed).")
                    continue

                # Create new filename with "Cleaned_" prefix
                cleaned_file_name = f"Cleaned_{file_name}"
                dest_file = os.path.join(dest_folder, cleaned_file_name)

                # Save the cleaned CSV to the destination
                df_cleaned.to_csv(dest_file, index=False)
                print(f"Cleaned & copied: {src_file} -> {dest_file}")
            
            except Exception as e:
                print(f"Error processing {src_file}: {e}")

    print("CSV files cleaned and copied successfully.")

source_folder = os.path.join(os.path.dirname(__file__), "..", "11_input")
destination_folder = os.path.join(os.path.dirname(__file__), "..", "14_product")

clean_and_copy_csv(source_folder, destination_folder)
