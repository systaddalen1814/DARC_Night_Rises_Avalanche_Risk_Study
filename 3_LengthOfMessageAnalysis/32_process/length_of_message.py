import pandas as pd
import matplotlib.pyplot as plt
import os


def get_avg_length(column : pd.Series):
    total = 0
    for data in column.values:
        print(data)
        total += len(data)
    if column.empty:
        return 0
    return total / column.size

def main():
    directory = "../../2_DataCombination/24_product"
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            # Read the CSV file into a DataFrame
            print(f"Processing file: {filename}")
            combo_dataframe = pd.read_csv(file_path)
            dict_of_message_len_by_center = {"caic":0, "SAC":0, "Ogden":0, "SLA":0, "Logan":0, "Provo":0}
            for key in dict_of_message_len_by_center.keys():
                dict_of_message_len_by_center[key] = get_avg_length(combo_dataframe[combo_dataframe["Source"] == key]["Message"])

            plt.bar(dict_of_message_len_by_center.keys(), dict_of_message_len_by_center.values())

            # Add text labels on top of each bar
            for i, value in enumerate(dict_of_message_len_by_center.values()):
                plt.text(i, value, str(round(value, 0)), ha='center', va='bottom')
            plt.ylabel("Average Message Length")
            plt.xlabel("Message Source")
            plt.title("Average Message Length from Different Sources")
            plt.savefig(f"../35_datavis/{filename}.png")
            plt.show()


if __name__ == '__main__':
    main()