from typing import Dict
import matplotlib.pyplot as plt
import pandas as pd
import os

def main():
    plt.rcParams.update({
        'font.size': 16,  # General font size
        'axes.titlesize': 20,  # Title font size
        'axes.labelsize': 16,  # Axis label font size
        'xtick.labelsize': 14,  # X tick label size
        'ytick.labelsize': 18  # Y tick label size
    })

    # Get the current working directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Define the input and output paths
    input_path = os.path.join(current_dir, "../../5_TFIDF/54_product")
    output_path = os.path.join(current_dir, "../65_datavis")

    # Find files that contain 'Joined' in their name
    files = []
    for file in os.listdir(input_path):
        if file.endswith(".csv") and "Joined" in file:
            files.append(os.path.join(input_path, file))

    # Create a 1x3 grid for the plots
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))  # Adjusted size for side-by-side layout

    # Loop through the files and create individual plots on each axis
    for idx, file in enumerate(files):
        words_tfidf_avg: Dict[str, float] = {}
        with open(file, "r", encoding="utf-8") as f:
            data = pd.read_csv(f)
            for col in data.columns.tolist():
                avg_tfidf = data[col].sum() / data[col].shape[0]
                words_tfidf_avg[col] = avg_tfidf

            series: pd.Series = pd.Series(words_tfidf_avg)
            top30: pd.Series = series.sort_values(ascending=False).head(15)

            # Extract part of the filename to display in the x-axis label
            name = os.path.basename(file).strip(".csv")
            file_label = name.split("TF-IDF-")[1].split("-Joined")[0]  # Extract part of the filename

            # Set the current axis to the subplot's axis
            ax = axes[idx]  # Select the corresponding subplot axis
            top30_sorted = top30.sort_values(ascending=True)
            ax.barh(top30_sorted.index, top30_sorted.values, color="skyblue", edgecolor="grey")

            # Update x-axis label with extracted file name part
            ax.set_xlabel(f"TF-IDF Score for {file_label}", fontsize=14)
            ax.set_ylabel("Terms", fontsize=14)

    # Add a master title for the entire figure
    fig.suptitle("Top 15 TF-IDF Scores for Joined Files", fontsize=20, fontweight="bold")

    # Adjust layout to prevent overlap
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjusting layout for the master title

    # Save the final plot as a single image
    output_file = os.path.join(output_path, "joined_files_1x3_grid.png")
    plt.savefig(output_file)
    plt.close()

if __name__ == "__main__":
    main()
