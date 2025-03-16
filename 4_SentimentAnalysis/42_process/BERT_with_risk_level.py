import pandas as pd
import nltk
import re
import string
import torch
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import BertTokenizer, BertForSequenceClassification
from scipy.special import softmax
from nltk.corpus import stopwords
from wordcloud import WordCloud

nltk.download('stopwords')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device

file_paths = {
    "Low": "/content/avalanche_messages_1_low.csv",
    "Moderate": "/content/avalanche_messages_2_moderate.csv",
    "Considerable": "/content/avalanche_messages_3_considerable.csv",
    "High": "/content/avalanche_messages_4_high.csv",
    "Extreme": "/content/avalanche_messages_5_extreme.csv",
}

dataframes = []
for risk, path in file_paths.items():
    df = pd.read_csv(path)
    df["Risk_Level"] = risk
    dataframes.append(df)

df = pd.concat(dataframes, ignore_index=True)

MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME).to(device)

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

def get_sentiment(text):
    encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors="pt").to(device)
    with torch.no_grad():
        output = model(**encoded_input)
    scores = output.logits[0].cpu().numpy()
    scores = softmax(scores)
    sentiment_labels = ['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive']
    return sentiment_labels[scores.argmax()]

df['Cleaned_Message'] = df['Message'].apply(preprocess_text)
df['Sentiment'] = df['Cleaned_Message'].apply(get_sentiment)

sentiment_mapping = {'Very Negative': -2, 'Negative': -1, 'Neutral': 0, 'Positive': 1, 'Very Positive': 2}
df['Sentiment_Score'] = df['Sentiment'].map(sentiment_mapping)

plt.figure(figsize=(10, 6))
sns.countplot(x=df['Sentiment'], hue=df['Risk_Level'], order=['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive'])
plt.title('Sentiment Distribution Across Risk Levels')
plt.xticks(rotation=45)
plt.legend(title='Risk Level')
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(x=df['Sentiment'], hue=df['Source'], order=['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive'])
plt.title('Sentiment Distribution Across Websites')
plt.xticks(rotation=45)
plt.legend(title='Source')
plt.show()

text_data = ' '.join(df['Cleaned_Message'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title('Word Cloud of Messages')
plt.show()

df.to_csv("/processed_data/processed_avalanche_data.csv", index=False)

