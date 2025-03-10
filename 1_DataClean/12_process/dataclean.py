import os
import pandas as pd
import calendar

def standardize_columns(df, YEAR_MIN, YEAR_MAX):
    """Ensure the DataFrame has the correct columns and format."""
    
    # Normalize column names (convert to lowercase and strip spaces)
    df.columns = df.columns.str.lower().str.strip()

    # Handle Date Columns
    if 'month' in df.columns:
        df['month'] = df['month'].astype(str).str.capitalize()  # Standardize capitalization
        df['month'] = df['month'].apply(lambda x: str(list(calendar.month_name).index(x)) if x in calendar.month_name else x)
    elif 'date' in df.columns:
        # Convert 'date' column to 'Month', 'Day', 'Year'
        df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Convert to datetime
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['year'] = df['date'].dt.year
        df.drop(columns=['date'], inplace=True)  # Remove original date column
    else:
        df['month'], df['day'], df['year'] = None, None, None

    # Convert Month, Day, and Year columns to integers
    df['month'] = df['month'].astype(int, errors='ignore')  # Convert month to int
    df['day'] = df['day'].astype(int, errors='ignore')      # Convert day to int
    df['year'] = df['year'].astype(int, errors='ignore')    # Convert year to int
        
    # Standardize Message Column (combine 'danger message', 'description', etc.)
    possible_message_columns = ['danger message', 'message', 'description', 'info']
    for col in possible_message_columns:
        if col in df.columns:
            df.rename(columns={col: 'message'}, inplace=True)
            break
    if 'message' not in df.columns:
        df['message'] = None  # Ensure column exists

    # Ensure Source Column Exists
    if 'source' not in df.columns:
        df['source'] = None  # Ensure column exists

    # Remove unnamed or unnecessary index columns
    df = df.loc[:, ~df.columns.str.contains('^unnamed')]  # Drop unnamed index columns

    # Keep only the required columns
    df = df[['month', 'day', 'year', 'message', 'source']]
    df.columns = ['Month', 'Day', 'Year', 'Message', 'Source']  # Standardize column case

    df = df[(df["Year"] >= YEAR_MIN) & (df["Year"] <= YEAR_MAX)]

    return df

def clean_and_copy_csv(src_folder, dest_folder, min = 2000, max = 2030):
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
                print(f"\nProcessing: {file_name}")
                
                # Load CSV
                df = pd.read_csv(src_file)
                print(f"Original data shape: {df.shape}")
                print(f"Columns before standardization: {df.columns.tolist()}")

                # Standardize columns
                df_cleaned = standardize_columns(df, min, max)
                print(f"Columns after standardization: {df_cleaned.columns.tolist()}")
                print(f"Data after standardization (first few rows):\n{df_cleaned.head()}")
            
                # Strip leading/trailing spaces
                df_cleaned["Message"] = df_cleaned["Message"].str.strip()

                # Drop rows with empty messages
                df_cleaned = df_cleaned[df_cleaned["Message"].notnull()]  # Remove NaN
                df_cleaned = df_cleaned[df_cleaned["Message"] != ""]      # Remove empty strings

                # Drop rows with missing values
                df_cleaned = df_cleaned.dropna(how='any')
                print(f"Data shape after cleaning: {df_cleaned.shape}")
                
                # Remove problematic rows manually
                # I cannot figure out why nothing else catches these two observations
                # I've tried different encodings, different regex methods, idk what's going on
                for index, row in df_cleaned.iterrows():
                    if row['Month'] == 11 and row['Day'] == 13 and row['Year'] == 2014 and row['Source'] == 'Logan':
                        print(f"Removing row {index} - matching (11, 13, 2014, Logan)")
                        df_cleaned = df_cleaned.drop(index)
                    if row['Month'] == 10 and row['Day'] == 4 and row['Year'] == 2014 and row["Source"] == "Logan":
                        print(f"Removing row {index} - matching (10, 4, 2014, Logan)")
                        df_cleaned = df_cleaned.drop(index)

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

    print("\nCSV files cleaned, standardized, and copied successfully.")

source_folder = os.path.join(os.path.dirname(__file__), "..", "11_input")
destination_folder = os.path.join(os.path.dirname(__file__), "..", "14_product")

clean_and_copy_csv(source_folder, destination_folder, 2014, 2024)