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


#loading the data
file_path = "../../4_NLP/41_input/Master_Avalanche_Data.csv"
df = pd.read_csv(file_path)


#BERT model and tokenizer
MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME).to(device)

#helpers
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


#preprocessing/sentiment
df['Cleaned_Message'] = df['Message'].apply(preprocess_text)
df['Sentiment'] = df['Cleaned_Message'].apply(get_sentiment)

sentiment_mapping = {'Very Negative': -2, 'Negative': -1, 'Neutral': 0, 'Positive': 1, 'Very Positive': 2}
df['Sentiment_Score'] = df['Sentiment'].map(sentiment_mapping)
correlation = df[['Sentiment_Score', 'Risk_Level']].corr()


#visualizations
plt.figure(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation between Sentiment Score and Risk Level')
plt.show()

plt.figure(figsize=(8, 6))
sns.countplot(x=df['Sentiment'], order=['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive'])
plt.title('Distribution of Sentiments')
plt.xticks(rotation=45)
plt.show()

text_data = ' '.join(df['Cleaned_Message'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title('Word Cloud of Messages')
plt.show()