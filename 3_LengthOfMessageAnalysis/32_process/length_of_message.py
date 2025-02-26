import pandas as pd
import matplotlib.pyplot as plt


def get_avg_length(column : pd.Series):
    total = 0
    for row in column.iterrows():
        total += row[1]

    return total / column.shape[0]

def main():
    input_path = "../../2_DataCombonation/24_product/data.csv"
    combo_dataframe = pd.read_csv(input_path)
    dict_of_message_len_by_center = {"ciac":0, "SAC":0, "Ogden":0, "SLA":0, "Logan":0, "Provo":0}
    for key in dict_of_message_len_by_center.keys():
        dict_of_message_len_by_center[key] = get_avg_length(combo_dataframe[combo_dataframe["Source"] == key]["Danger Message"])

    plt.bar(dict_of_message_len_by_center.keys(), dict_of_message_len_by_center.values())
    plt.show()


if __name__ == '__main__':
    main()