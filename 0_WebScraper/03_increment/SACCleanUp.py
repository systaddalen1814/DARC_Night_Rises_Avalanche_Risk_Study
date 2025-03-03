import os
import pandas as pd
import calendar

def fix_sac_files(src_folder, dest_folder):
    """
    Reads all CSV files with 'SAC' in the filename, checks if the 'day' column contains values between 1-12 or words (months),
    swaps 'Month' and 'Day' column names (case-insensitive) if the 'day' column has month-related values,
    removes any 'Unnamed' columns, and saves the corrected files in the destination folder.
    """

    # List of month names to check for
    month_names = [calendar.month_name[i].lower() for i in range(1, 13)]

    if not os.path.exists(src_folder):
        print(f"Source folder '{src_folder}' does not exist.")
        return
    
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for file_name in os.listdir(src_folder):
        if "SAC" in file_name and file_name.lower().endswith(".csv"):  # Only process SAC CSV files
            src_file = os.path.join(src_folder, file_name)

            try:
                df = pd.read_csv(src_file)

                # Standardize column names (convert to lowercase & strip spaces)
                df.columns = [col.strip().lower() for col in df.columns]

                # Remove 'Unnamed' columns (usually index columns or irrelevant columns)
                df = df.loc[:, ~df.columns.str.contains('^unnamed', case=False)]

                # Check if "month" and "day" exist in the corrected column names
                if "month" in df.columns and "day" in df.columns:
                    # Check if any value in 'day' is more than 12 (indicating it's likely a 'day' column)
                    if df['day'].apply(lambda x: isinstance(x, str) and x.lower() in month_names).any() or \
                       df['day'].apply(lambda x: isinstance(x, (int, float)) and x <= 12).any():
                        # If 'day' contains month names or valid month numbers (1-12), swap columns
                        df.rename(columns={"month": "day", "day": "month"}, inplace=True)
                        print(f"Fixed & saved: {file_name}")
                    else:
                        print(f"Skipping {file_name} - 'Day' column has values greater than 12, no need to swap.")
                    
                    # Save the corrected file
                    dest_file = os.path.join(dest_folder, file_name)
                    df.to_csv(dest_file, index=False)

                else:
                    print(f"Skipping {file_name} - Columns found: {list(df.columns)}")

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    print("\nAll SAC files processed successfully.")

# Define source and destination folders
source_folder = os.path.join(os.path.dirname(__file__), "..", "04_product")
destination_folder = os.path.join(os.path.dirname(__file__), "..", "04_product")

fix_sac_files(source_folder, destination_folder)
