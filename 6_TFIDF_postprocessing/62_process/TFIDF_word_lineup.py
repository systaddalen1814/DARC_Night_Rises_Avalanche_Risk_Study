from typing import Tuple, List, Dict
import matplotlib.pyplot as plt
import pandas as pd
import os


def main():
    input_path = "../../5_TFIDF/54_product"
    output_path = "../64_product"

    # Get list of CSV files in the input path.
    files = [os.path.join(input_path, file) for file in os.listdir(input_path) if file.endswith(".csv")]

    series_list = []

    for file in files:
        words_tfidf_avg: Dict[str, float] = {}
        # Read CSV directly without opening manually
        data = pd.read_csv(file, encoding="utf-8")

        # Calculate average tf-idf for each column
        for col in data.columns:
            avg_tfidf = data[col].sum() / len(data[col])
            words_tfidf_avg[col] = avg_tfidf

        # Use os.path.splitext to properly remove the file extension
        file_name = os.path.splitext(os.path.basename(file))[0]

        series: pd.Series = pd.Series(words_tfidf_avg, name=file_name)
        top30: pd.Series = series.sort_values(ascending=False).head(30)
        series_list.append(pd.Series(top30.index, name=file_name))

    # Concatenate the Series objects into a DataFrame (columns represent files)
    df = pd.concat(series_list, axis=1)

    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Save the resulting DataFrame to a CSV file
    df.to_csv(os.path.join(output_path, "TF-IDF-comp.csv"))
if __name__ == "__main__":
    main()