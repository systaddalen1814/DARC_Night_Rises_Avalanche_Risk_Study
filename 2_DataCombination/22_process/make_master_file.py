import os
import pandas as pd

"""MUST first run file 'datacombination.py' to run this file"""

def create_master_file(src_folder, master_file):
    """Combines all risk level CSVs into a single master file with a 'Risk_Level' column."""
    
    if not os.path.exists(src_folder):
        print(f"Source folder '{src_folder}' does not exist.")
        return
    
    risk_files = {
        "avalanche_messages_1_low.csv": 1,
        "avalanche_messages_2_moderate.csv": 2,
        "avalanche_messages_3_considerable.csv": 3,
        "avalanche_messages_4_high.csv": 4,
        "avalanche_messages_5_extreme.csv": 5
    }

    all_data = []

    for file_name, risk_level in risk_files.items():
        src_file = os.path.join(src_folder, file_name)

        if os.path.isfile(src_file):
            try:
                df = pd.read_csv(src_file)
                df["Risk_Level"] = risk_level  # Add risk level column
                all_data.append(df)
                print(f"Added: {file_name} (Risk Level {risk_level})")

            except Exception as e:
                print(f"Error processing {src_file}: {e}")

    if all_data:
        master_df = pd.concat(all_data, ignore_index=True)
        master_df.to_csv(master_file, index=False)
        print(f"Master file saved: {master_file}")
    else:
        print("No valid files found. Master file not created.")

# Set input folder and output file
source_folder = os.path.join(os.path.dirname(__file__), "..", "24_product")
master_output_file = os.path.join(source_folder, "Master_Avalanche_Data.csv")

create_master_file(source_folder, master_output_file)
