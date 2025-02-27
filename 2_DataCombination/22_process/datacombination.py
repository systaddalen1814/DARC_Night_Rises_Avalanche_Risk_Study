import os
import pandas as pd

def combine(src_folder, dest_folder):
    """Combines CSV files by avalanche risk level and saves them separately."""

    if not os.path.exists(src_folder):
        print(f"Source folder '{src_folder}' does not exist.")
        return
    
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Dictionary to store DataFrames categorized by risk level
    risk_levels = {str(i): [] for i in range(1, 6)}

    # Mapping for risk level names (numeric level to description)
    risk_mapping = {
        "1": "low",
        "2": "moderate",
        "3": "considerable",
        "4": "high",
        "5": "extreme"
    }

    for file_name in os.listdir(src_folder):
        src_file = os.path.join(src_folder, file_name)

        # Process only CSV files
        if os.path.isfile(src_file) and file_name.lower().endswith('.csv'):
            try:
                df = pd.read_csv(src_file)

                # Assign file to appropriate risk level based on filename keywords
                assigned = False
                for level, keywords in risk_mapping.items():
                    if any(keyword in file_name.lower() for keyword in [level, keywords]):
                        risk_levels[level].append(df)
                        assigned = True
                        break  # Stop checking after the first match
                
                if not assigned:
                    print(f"WARNING: {file_name} did not match any risk level!")

            except Exception as e:
                print(f"ERROR: Could not process {file_name}: {e}")

    # Save combined CSVs for each risk level
    for level, dfs in risk_levels.items():
        if dfs:  # Only save if there's data
            combined_df = pd.concat(dfs, ignore_index=True)
            risk_name = risk_mapping.get(level, "unknown")
            dest_file = os.path.join(dest_folder, f"avalanche_messages_{level}_{risk_name}.csv")
            combined_df.to_csv(dest_file, index=False)
            print(f"Saved: {dest_file} ({len(combined_df)} rows)")

    print("\nAll CSV files processed and saved successfully.")

# Define source and destination folders
source_folder = os.path.join(os.path.dirname(__file__), "..", "21_input")
destination_folder = os.path.join(os.path.dirname(__file__), "..", "24_product")

combine(source_folder, destination_folder)
