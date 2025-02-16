import os
import pandas as pd

# Define input folder where the scraped CSV files are stored
input_folder = os.path.join(os.path.dirname(__file__), "..", "03_increment")

# Define output folder for categorized files
output_folder = os.path.join(os.path.dirname(__file__), "..", "04_product")
os.makedirs(output_folder, exist_ok=True)

# Define avalanche risk levels in priority order (highest first)
risk_levels = ["EXTREME", "HIGH", "CONSIDERABLE", "MODERATE", "LOW"]
categorized_data = {level: [] for level in risk_levels}

# Get all CSV files from input folder
csv_files = [f for f in os.listdir(input_folder) if f.endswith("_forecast_data.csv")]

# Process each CSV file
for file in csv_files:
    file_path = os.path.join(input_folder, file)
    print(f"Processing {file_path}...")

    # Read CSV file
    df = pd.read_csv(file_path)

    # Ensure the required columns exist
    if not {"Month", "Day", "Year", "Danger Message"}.issubset(df.columns):
        print(f"Skipping {file} - Missing required columns")
        continue

    # Categorize each row based on the highest danger level found in uppercase
    for _, row in df.iterrows():
        message = str(row["Danger Message"])

        # Check for the highest uppercase danger level
        highest_level = "LOW"  # Default if no risk level is found
        for level in risk_levels[:-1]:  # Exclude "LOW" from search
            if f" {level} " in f" {message} ":  # Ensure whole word matching
                highest_level = level
                break  # Stop once the highest level is found

        categorized_data[highest_level].append(row)

# Write categorized data to separate CSV files
for level, rows in categorized_data.items():
    if rows:  # Only create a file if there is data for that category
        output_file = os.path.join(output_folder, f"Utah_{level}_risk_avalanche_forecasts.csv")
        pd.DataFrame(rows).to_csv(output_file, index=False)
        print(f"Saved {level} risk data to {output_file}")
