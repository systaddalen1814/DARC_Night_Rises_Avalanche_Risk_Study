from typing import Tuple, List, Dict
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

    input_path = "../../5_TFIDF/54_product"
    output_path = "../65_datavis"
    files = []
    for file in os.listdir(input_path):
        if file.endswith(".csv"):
            files.append(os.path.join(input_path, file))

    for file in files:
        words_tfidf_avg : Dict[str,float]= {}
        with open(file, "r", encoding="utf-8") as f:
            data = pd.read_csv(f)
            for col in data.columns.tolist():
                avg_tfidf = data[col].sum()/data[col].shape[0]
                words_tfidf_avg[col] = avg_tfidf

            series : pd.Series = pd.Series(words_tfidf_avg)
            top30 : pd.Series = series.sort_values(ascending=False).head(15)
            name = os.path.basename(file).strip(".csv")
            # Create the plot
            plt.figure(figsize=(10, 8))
            # Sorting by value in ascending order for a cleaner horizontal bar plot layout
            top30_sorted = top30.sort_values(ascending=True)
            bars = plt.barh(top30_sorted.index, top30_sorted.values, color="skyblue", edgecolor="grey")

            plt.title(f"Top 15 TF-IDF Scores for {name}", fontsize=16, fontweight="bold")
            plt.xlabel("TF-IDF Score", fontsize=14)
            plt.ylabel("Terms", fontsize=14)
            plt.tight_layout()


            # Save and close the figure
            output_file = os.path.join(output_path, f"{name}_top30.png")
            plt.savefig(output_file)
            plt.close()





if __name__ == "__main__":
    main()