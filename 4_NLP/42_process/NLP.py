import os
import pandas as pd
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from wordcloud import WordCloud, STOPWORDS
import os

# Load the dataset
file_path = "../../2_DataCombination/24_product/Master_Avalanche_Data.csv"
df = pd.read_csv(file_path)

# Selecting relevant columns
messages = df['Message']
sentiments = df['Risk_Level']  # Assuming Risk_Level represents sentiment

# Function for text preprocessing
def text_cleaning(text):
    soup = BeautifulSoup(text, "html.parser")
    text = re.sub(r'\[[^]]*\]', '', soup.get_text())
    pattern = r"[^a-zA-Z0-9\s,']"
    text = re.sub(pattern, '', text)
    return text.lower()

# Clean text
df['Cleaned_Message'] = df['Message'].apply(text_cleaning)

# Split dataset
x_train, x_test, y_train, y_test = train_test_split(
    df['Cleaned_Message'], sentiments, test_size=0.2, stratify=sentiments, random_state=42)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_tfidf = vectorizer.fit_transform(x_train)
X_test_tfidf = vectorizer.transform(x_test)

# Model initialization (Naive Bayes)
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Evaluation
y_pred = model.predict(X_test_tfidf)
print("Classification Report:\n", classification_report(y_test, y_pred))

# Visualization: Word Cloud
def generate_wordcloud(text, title):
    all_text = " ".join(text)
    wordcloud = WordCloud(width=800, height=400, stopwords=set(STOPWORDS), background_color='black').generate(all_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(title)
    plt.show()

positive = df[df['Risk_Level'] == 1]['Cleaned_Message'].tolist()
generate_wordcloud(positive, 'Positive Messages')

negative = df[df['Risk_Level'] == 0]['Cleaned_Message'].tolist()
generate_wordcloud(negative, 'Negative Messages')













# import os
# import shutil
# import tarfile
# import tensorflow as tf
# from transformers import BertTokenizer, TFBertForSequenceClassification
# import pandas as pd
# from bs4 import BeautifulSoup
# import re
# import matplotlib.pyplot as plt
# import plotly.express as px
# import plotly.offline as pyo
# import plotly.graph_objects as go
# from wordcloud import WordCloud, STOPWORDS
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report



# # Get the current working directory
# current_folder = os.getcwd()

# dataset = tf.keras.utils.get_file(
#     fname ="aclImdb.tar.gz", 
#     origin ="http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz",
#     cache_dir=  current_folder,
#     extract = True)

# dataset_path = os.path.dirname(dataset)
# # Check the dataset
# os.listdir(dataset_path)

# train_dir = os.path.join(dataset_dir,'train')
# os.listdir(train_dir)


# for file in os.listdir(train_dir):
#     file_path = os.path.join(train_dir, file)
#     # Check if it's a file (not a directory)
#     if os.path.isfile(file_path): 
#         with open(file_path, 'r', encoding='utf-8') as f:
#             first_value = f.readline().strip()
#             print(f"{file}: {first_value}")
#     else:
#         print(f"{file}: {file_path}")



# def load_dataset(directory):
#     data = {"sentence": [], "sentiment": []}
#     for file_name in os.listdir(directory):
#         print(file_name)
#         if file_name == 'pos':
#             positive_dir = os.path.join(directory, file_name)
#             for text_file in os.listdir(positive_dir):
#                 text = os.path.join(positive_dir, text_file)
#                 with open(text, "r", encoding="utf-8") as f:
#                     data["sentence"].append(f.read())
#                     data["sentiment"].append(1)
#         elif file_name == 'neg':
#             negative_dir = os.path.join(directory, file_name)
#             for text_file in os.listdir(negative_dir):
#                 text = os.path.join(negative_dir, text_file)
#                 with open(text, "r", encoding="utf-8") as f:
#                     data["sentence"].append(f.read())
#                     data["sentiment"].append(0)
            
#     return pd.DataFrame.from_dict(data)


# # Load the dataset from the train_dir
# train_df = load_dataset(train_dir)
# print(train_df.head())


# test_dir = os.path.join(dataset_dir,'test')

# # Load the dataset from the train_dir
# test_df = load_dataset(test_dir)
# print(test_df.head())




# sentiment_counts = train_df['sentiment'].value_counts()

# fig =px.bar(x= {0:'Negative',1:'Positive'},
#             y= sentiment_counts.values,
#             color=sentiment_counts.index,
#             color_discrete_sequence =  px.colors.qualitative.Dark24,
#             title='<b>Sentiments Counts')

# fig.update_layout(title='Sentiments Counts',
#                   xaxis_title='Sentiment',
#                   yaxis_title='Counts',
#                   template='plotly_dark')

# # Show the bar chart
# fig.show()
# pyo.plot(fig, filename = 'Sentiments Counts.html', auto_open = True)


# def text_cleaning(text):
#     soup = BeautifulSoup(text, "html.parser")
#     text = re.sub(r'\[[^]]*\]', '', soup.get_text())
#     pattern = r"[^a-zA-Z0-9\s,']"
#     text = re.sub(pattern, '', text)
#     return text


# # Train dataset
# train_df['Cleaned_sentence'] = train_df['sentence'].apply(text_cleaning).tolist()
# # Test dataset
# test_df['Cleaned_sentence'] = test_df['sentence'].apply(text_cleaning)


# # Function to generate word cloud
# def generate_wordcloud(text,Title):
#     all_text = " ".join(text)
#     wordcloud = WordCloud(width=800, 
#                           height=400,
#                           stopwords=set(STOPWORDS), 
#                           background_color='black').generate(all_text)
#     plt.figure(figsize=(10, 5))
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis("off")
#     plt.title(Title)
#     plt.show()



# positive = train_df[train_df['sentiment']==1]['Cleaned_sentence'].tolist()
# generate_wordcloud(positive,'Positive Review')


# negative = train_df[train_df['sentiment']==0]['Cleaned_sentence'].tolist()
# generate_wordcloud(negative,'Negative Review')


# # Training data
# #Reviews = "[CLS] " +train_df['Cleaned_sentence'] + "[SEP]"
# Reviews = train_df['Cleaned_sentence']
# Target = train_df['sentiment']

# # Test data
# #test_reviews =  "[CLS] " +test_df['Cleaned_sentence'] + "[SEP]"
# test_reviews = test_df['Cleaned_sentence']
# test_targets = test_df['sentiment']


# x_val, x_test, y_val, y_test = train_test_split(test_reviews,
#                                                     test_targets,
#                                                     test_size=0.5, 
#                                                     stratify = test_targets)

# #Tokenize and encode the data using the BERT tokenizer
# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)


# max_len= 128
# # Tokenize and encode the sentences
# X_train_encoded = tokenizer.batch_encode_plus(Reviews.tolist(),
#                                               padding=True, 
#                                               truncation=True,
#                                               max_length = max_len,
#                                               return_tensors='tf')

# X_val_encoded = tokenizer.batch_encode_plus(x_val.tolist(), 
#                                               padding=True, 
#                                               truncation=True,
#                                               max_length = max_len,
#                                               return_tensors='tf')

# X_test_encoded = tokenizer.batch_encode_plus(x_test.tolist(), 
#                                               padding=True, 
#                                               truncation=True,
#                                               max_length = max_len,
#                                               return_tensors='tf')


# k = 0
# print('Training Comments -->>',Reviews[k])
# print('\nInput Ids -->>\n',X_train_encoded['input_ids'][k])
# print('\nDecoded Ids -->>\n',tokenizer.decode(X_train_encoded['input_ids'][k]))
# print('\nAttention Mask -->>\n',X_train_encoded['attention_mask'][k])
# print('\nLabels -->>',Target[k])



# # Intialize the model
# model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)


# # Compile the model with an appropriate optimizer, loss function, and metrics
# optimizer = tf.keras.optimizers.Adam(learning_rate=2e-5)
# loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
# metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
# model.compile(optimizer=optimizer, loss=loss, metrics=[metric])


# # Step 5: Train the model
# history = model.fit(
#     [X_train_encoded['input_ids'], X_train_encoded['token_type_ids'], X_train_encoded['attention_mask']],
#     Target,
#     validation_data=(
#       [X_val_encoded['input_ids'], X_val_encoded['token_type_ids'], X_val_encoded['attention_mask']],y_val),
#     batch_size=32,
#     epochs=3
# )


# #Evaluate the model on the test data
# test_loss, test_accuracy = model.evaluate(
#     [X_test_encoded['input_ids'], X_test_encoded['token_type_ids'], X_test_encoded['attention_mask']],
#     y_test
# )
# print(f'Test loss: {test_loss}, Test accuracy: {test_accuracy}')



# path = '/content'
# # Save tokenizer
# tokenizer.save_pretrained(path +'/Tokenizer')

# # Save model
# model.save_pretrained(path +'/Model')

# # This code is modified by Susobhan Akhuli


# # Load tokenizer
# bert_tokenizer = BertTokenizer.from_pretrained(path +'/Tokenizer')

# # Load model
# bert_model = TFBertForSequenceClassification.from_pretrained(path +'/Model')


# pred = bert_model.predict(
#     [X_test_encoded['input_ids'], X_test_encoded['token_type_ids'], X_test_encoded['attention_mask']])

# # pred is of type TFSequenceClassifierOutput
# logits = pred.logits

# # Use argmax along the appropriate axis to get the predicted labels
# pred_labels = tf.argmax(logits, axis=1)

# # Convert the predicted labels to a NumPy array
# pred_labels = pred_labels.numpy()

# label = {
#     1: 'positive',
#     0: 'Negative'
# }

# # Map the predicted labels to their corresponding strings using the label dictionary
# pred_labels = [label[i] for i in pred_labels]
# Actual = [label[i] for i in y_test]

# print('Predicted Label :', pred_labels[:10])
# print('Actual Label    :', Actual[:10])


# print("Classification Report: \n", classification_report(Actual, pred_labels))


# def Get_sentiment(Review, Tokenizer=bert_tokenizer, Model=bert_model):
#     # Convert Review to a list if it's not already a list
#     if not isinstance(Review, list):
#         Review = [Review]

#     Input_ids, Token_type_ids, Attention_mask = Tokenizer.batch_encode_plus(Review,
#                                                                              padding=True,
#                                                                              truncation=True,
#                                                                              max_length=128,
#                                                                              return_tensors='tf').values()
#     prediction = Model.predict([Input_ids, Token_type_ids, Attention_mask])

#     # Use argmax along the appropriate axis to get the predicted labels
#     pred_labels = tf.argmax(prediction.logits, axis=1)

#     # Convert the TensorFlow tensor to a NumPy array and then to a list to get the predicted sentiment labels
#     pred_labels = [label[i] for i in pred_labels.numpy().tolist()]
#     return pred_labels


# Review ='''Bahubali is a blockbuster Indian movie that was released in 2015. 
# It is the first part of a two-part epic saga that tells the story of a legendary hero who fights for his kingdom and his love. 
# The movie has received rave reviews from critics and audiences alike for its stunning visuals, 
# spectacular action scenes, and captivating storyline.'''
# Get_sentiment(Review)
