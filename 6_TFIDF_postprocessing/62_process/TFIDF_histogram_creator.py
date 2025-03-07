from typing import Tuple, List, Dict
import matplotlib.pyplot as plt
import pandas as pd
import os



def main():
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
            top30 : pd.Series = series.sort_values(ascending=False).head(30)
            name = os.path.basename(file).strip(".csv")
            top30.plot(kind="bar", figsize=(20,10), xlabel="Words", ylabel="TFIDF", title=f"{name}")
            # Plot using a horizontal bar chart for clarity
            plt.tight_layout()

            plt.savefig(os.path.join(output_path, f"{name}.png"))





if __name__ == "__main__":
    main()