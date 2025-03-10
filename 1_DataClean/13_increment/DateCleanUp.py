import os
import pandas as pd

### Not needed. Was used as checker for the dates

def process_csv(df):
    """
    Modify this function to make edits to each CSV file.
    This version prints the max and min year from the 'Year' column.
    """

    if "Year" in df.columns:
        try:
            df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
            max_year = df["Year"].max()
            min_year = df["Year"].min()
            print(f"Year Range: {min_year} - {max_year}")
            
        except Exception as e:
            print(f"Error processing Year column: {e}")
    else:
        print("No 'Year' column found.")

    return df

def process_csv_files(src_folder, dest_folder):
    """
    Loops through CSV files in the source folder, applies transformations, 
    and saves them in the destination folder.
    """

    if not os.path.exists(src_folder):
        print(f"Source folder '{src_folder}' does not exist.")
        return
    
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Process each CSV file
    for file_name in os.listdir(src_folder):
        if file_name.lower().endswith('.csv'):
            src_path = os.path.join(src_folder, file_name)
            dest_path = os.path.join(dest_folder, file_name)

            try:
                df = pd.read_csv(src_path)  # Read CSV file
                df = process_csv(df)  # Apply custom edits
                #df.to_csv(dest_path, index=False)  # Save edited CSV
                #print(f"Processed & saved: {file_name}")

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    print("\nProcessing complete!")

# Set source and destination folders
source_folder = os.path.join(os.path.dirname(__file__), "..", "14_product")
destination_folder = os.path.join(os.path.dirname(__file__), "..", "14_product")

# Run the processing function
process_csv_files(source_folder, destination_folder)
