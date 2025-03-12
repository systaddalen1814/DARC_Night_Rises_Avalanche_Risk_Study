from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import os
import re
from typing import List, Tuple, Dict

def remove_digits(text):
    # Remove all digits from the text
    return re.sub(r'\d+', '', text)

def main():
    input_path = "../../2_DataCombination/24_product"
    output_path = "../54_product"
    vectorizer = TfidfVectorizer(preprocessor=remove_digits, stop_words='english')
    for file in os.listdir(input_path):
        if file.endswith(".csv"):
            try:
                risk_level = re.search(r"\d", file).group()
            except:
                risk_level = "Joined-Risk"
            with open(os.path.join(input_path, file), "r", encoding="utf-8") as file:
                data = pd.read_csv(file)
            classes = data["Source"].unique().tolist()
            source_to_message : Dict[str, List[str]] = {}
            for c in classes:
                source_to_message[c] = [str(x).lower() for x in data[data["Source"] == c]["Message"]]
                X = vectorizer.fit_transform(source_to_message[c])
                feature_names = vectorizer.get_feature_names_out()
                pd.DataFrame(X.toarray(), columns=feature_names).to_csv(f"{output_path}/TF-IDF-{c}-{risk_level}.csv", index=False)






if __name__ == '__main__':
    main()
