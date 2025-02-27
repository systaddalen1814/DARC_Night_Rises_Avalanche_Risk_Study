import os
import pandas as pd
import calendar

def standardize_columns(df):
    """Ensure the DataFrame has the correct columns and format."""
    
    # Normalize column names (convert to lowercase and strip spaces)
    df.columns = df.columns.str.lower().str.strip()

    # Handle Date Columns
    if 'Month' in df.columns:
        df['Month'] = df['Month'].astype(str).str.capitalize()  # Standardize capitalization
        df['Month'] = df['Month'].apply(lambda x: str(list(calendar.month_name).index(x)) if x in calendar.month_name else x)
    elif 'date' in df.columns:
        # Convert 'date' column to 'Month', 'Day', 'Year'
        df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Convert to datetime
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['year'] = df['date'].dt.year
        df.drop(columns=['date'], inplace=True)  # Remove original date column
    else:
        # If neither format is present, create empty columns
        df['month'], df['day'], df['year'] = None, None, None
    
    # Standardize Message Column
    possible_message_columns = ['danger message', 'message', 'description', 'info']
    for col in possible_message_columns:
        if col in df.columns:
            df.rename(columns={col: 'message'}, inplace=True)
            break
    if 'message' not in df.columns:
        df['message'] = None  # Ensure column exists

    # Remove unnamed or unnecessary index columns
    df = df.loc[:, ~df.columns.str.contains('^unnamed')]  # Drop unnamed index columns

    # Ensure Source Column Exists
    if 'source' not in df.columns:
        df['source'] = None  # Ensure column exists

    # Keep only the required columns (ensure proper casing)
    df = df[['month', 'day', 'year', 'message', 'source']]
    df.columns = ['Month', 'Day', 'Year', 'Message', 'Source']  # Standardize column case

    return df

def clean_and_copy_csv(src_folder, dest_folder):
    """Cleans and standardizes CSV files before copying them to dest_folder."""
    
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
                # Load CSV
                df = pd.read_csv(src_file)

                # Standardize columns
                df_cleaned = standardize_columns(df)
                df_cleaned = df_cleaned.dropna(how='any') # want to drop rows with missing values

                # Skip if DataFrame is empty
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

    print("CSV files cleaned, standardized, and copied successfully.")

source_folder = os.path.join(os.path.dirname(__file__), "..", "11_input")
destination_folder = os.path.join(os.path.dirname(__file__), "..", "14_product")

clean_and_copy_csv(source_folder, destination_folder)
