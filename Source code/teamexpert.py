# -*- coding: utf-8 -*-
"""TeamExpert.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PX5up5arRzdt3UbX5EDBnpVX1io3z4gU
"""

from google.colab import drive
drive.mount('/content/drive', force_remount=True)

from google.colab import drive
drive.mount('/content/drive')

pwd



#import library
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelBinarizer
# from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from wordcloud import WordCloud,STOPWORDS
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize,sent_tokenize
from bs4 import BeautifulSoup
import spacy
import re,string,unicodedata
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.stem import LancasterStemmer,WordNetLemmatizer
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from textblob import TextBlob
from textblob import Word
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split
import tensorflow.keras.layers as L
from tensorflow.keras.losses import MeanAbsoluteError
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import plot_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

import plotly.express as px

import os
import warnings
warnings.filterwarnings('ignore')

# seed_value = 1337
# np.random.seed(seed_value)
# tf.random.set_seed(seed_value)
# rn.seed(seed_value)

data = pd.read_csv('/content/drive/MyDrive/projdata/tripadvisor_hotel_reviews.csv')
data.head(10)

data.describe

# #correct spelling
# def correct_spell(text):
#   text = TextBlob(text)
#   text = text.correct()
#   return text
# for i in range(2):
#   print(data['Review'][100+i])
#   data['Review'][100+i] = correct_spell(data['Review'][100+i])
#   print(data['Review'][100+i])
# # data["Review"] = pd.Series("auto corrrect this sentance")

# # t.apply(correct_spell)
# # data.head(10)

#analyze the data
plot = px.histogram(data, x="Rating")
plot.update_traces(marker_color="lightblue", marker_line_color="black", marker_line_width=1)
plot.update_layout(title="Rating Counts")
plot.show()

#change to all lower cases for review text
def lower_case(text):
  return text.lower()
# t = pd.Series(['HAHA', 'AAaa', 'HEllo'])
data["Review"] = data["Review"].apply(lower_case)

#remove special characters from review text
# print(data["Review"][20])
def remove_special(text):
  text = re.sub("[^A-Za-z0-9\s]", "", text)
  return text
# t = pd.Series("Hello%^*)123[.,")
data["Review"] = data["Review"].apply(remove_special)
# print(data["Review"][20])

#remove stop words
# print(data["Review"][20])
def remove_stopwords(text):
  stop_words = nltk.corpus.stopwords.words("english")
  word_token = word_tokenize(text)
  text = " ".join(w for w in word_token if not w in stop_words)
  return text
# t = pd.Series("This is the best tool in a while")
data["Review"] = data["Review"].apply(remove_stopwords)
# print(data["Review"][20])

for i in range(10):
  print(data['Review'][i])

# Stemming
def simple_stemmer(text):
  ps = nltk.porter.PorterStemmer()
  
  #text = ' '.join([ps.stem(word) for word in text.split()])
  words = word_tokenize(text)
  text = ' '.join([ps.stem(word) for word in words])
  return text

# No stemming
print(data["Review"][628])

# Apply stemming
print(simple_stemmer(data["Review"][628]))

#print(nltk.porter.PorterStemmer().stem("seattle"))

#Lemmatization
def lemmatize_word(text):
  lemmatizer = WordNetLemmatizer()
  word_token = word_tokenize(text)
  text = " ".join(lemmatizer.lemmatize(w) for w in word_token)
  return text
#no lemmatization 
print(data["Review"][618])

# Apply lemmatization
print(lemmatize_word(data["Review"][618]))

# t = pd.Series("girls playing plays played studies caring cares cared")
# data["Review"] = data["Review"].apply(lemmatize_word)
# # data.head(20)

#most frequent words for rating1
frequent_words1=pd.Series(" ".join(data["Review"][data["Rating"]==1]).split()).value_counts()[:20].index.tolist()

#most frequent words for rating2
frequent_words2=pd.Series(" ".join(data["Review"][data["Rating"]==2]).split()).value_counts()[:20].index.tolist()

#most frequent words for rating3
frequent_words3=pd.Series(" ".join(data["Review"][data["Rating"]==3]).split()).value_counts()[:20].index.tolist()

#most frequent words for rating4
frequent_words4=pd.Series(" ".join(data["Review"][data["Rating"]==4]).split()).value_counts()[:20].index.tolist()

#most frequent words for rating5
frequent_words5=pd.Series(" ".join(data["Review"][data["Rating"]==5]).split()).value_counts()[:20].index.tolist()
print(frequent_words5)

#find the most common words among all 5 ratings
common_words = set(frequent_words1)&set(frequent_words2)&set(frequent_words3)&set(frequent_words4)&set(frequent_words5)
print(common_words)

# Remove most frequent words?? Not sure if this is required
top5 = [" hotel ", " room ", " hotels ", " rooms ", " nt ", " s "," day ", " time ", " stay ", " night ", " stayed "]
for top in top5:
  for i in range(len(data["Review"])):
    data["Review"][i] = data["Review"][i].replace(top, " ")
print(data["Review"][9])

data["Review"][10000]

#visualize the most common words for rating 1
rating1_words = " ".join([text for text in data["Review"][data["Rating"]==1]])
wordcloud = WordCloud(width = 900, height = 900).generate(rating1_words)
plt.figure(figsize = (10,10))
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Most common Words in Rating 1")

#visualize the most common words for rating 2
rating1_words = " ".join([text for text in data["Review"][data["Rating"]==2]])
wordcloud = WordCloud(width = 900, height = 900).generate(rating1_words)
plt.figure(figsize = (10,10))
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Most common Words in Rating 2")

#visualize the most common words for rating 3
rating1_words = " ".join([text for text in data["Review"][data["Rating"]==3]])
wordcloud = WordCloud(width = 900, height = 900).generate(rating1_words)
plt.figure(figsize = (10,10))
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Most common Words in Rating 3")

#visualize the most common words for rating 4
rating1_words = " ".join([text for text in data["Review"][data["Rating"]==4]])
wordcloud = WordCloud(width = 900, height = 900).generate(rating1_words)
plt.figure(figsize = (10,10))
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Most common Words in Rating 4")

#visualize the most common words for rating 5
rating1_words = " ".join([text for text in data["Review"][data["Rating"]==5]])
wordcloud = WordCloud(width = 900, height = 900).generate(rating1_words)
plt.figure(figsize = (10,10))
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Most common Words in Rating 5")

# Save data_copy into a csv file, so that read the data directly in the future
data.to_csv("/content/drive/MyDrive/projdata/tripadvisor_hotel_reviews_copy.csv", index = False)

# Read data from file for sentimental polarity analysis and overall rating prediction
data_copy = pd.read_csv("/content/drive/MyDrive/projdata/tripadvisor_hotel_reviews_copy.csv")

# Valence Aware Dictionary and Sentiment Reasoner (VADER) sentiment analysis
# Reference: https://deepnote.com/@abid/Trip-Advisor-Data-AnalysisML-f6060b39-d76c-4579-9648-a54bc8b5ffb5
!pip install vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Create sentimental polarity
# This function will score a review in scale [-1,1], where "1" means most positive
# "-1" means most negative
sentiment_analyzer = SentimentIntensityAnalyzer()

def compound_score(text):
  return sentiment_analyzer.polarity_scores(text)["compound"]

# Define "postive, negative, neutral" sentiments
def sentiment(score):
  emotion = ""
  if (score >= 0.5):
    emotion = "Positive"
  elif (score <= -0.5):
    emotion = "Negative"
  else:
    emotion = "Neutral"
  return emotion

## Create sentiment score
polarity_scores = data_copy["Review"].astype("str").apply(compound_score)
data_copy["Sentiment_Score"] = polarity_scores

data_copy["Sentiment"] = data_copy["Sentiment_Score"].apply(sentiment)

## Visualize sentiment score
print(data_copy["Sentiment"][100:102])
print(data_copy["Sentiment_Score"][100:102])
print(data_copy["Review"][101])

# plot the count of "positive", "negative", and "neutral"
sns.countplot (data = data_copy, x = "Sentiment", palette = "tab10")

# plot the count of sentiment for each overall rating
viz = data_copy[['Rating', 'Sentiment']].value_counts().rename_axis(['Rating', 'Sentiment']).reset_index(name='counts')
figure = px.bar(x = viz.Rating, y = viz.counts, color = viz.Sentiment, color_discrete_sequence=px.colors.qualitative.Pastel,
                title = "Sentiment for Ratings", labels = {'x': 'Ratings', 'y': 'Total Number'})
figure.show()

## Overall rating prediction
# Possible models:
# Long Short Term Memory(LSTM):https://deepnote.com/@abid/Trip-Advisor-Data-AnalysisML-f6060b39-d76c-4579-9648-a54bc8b5ffb5
# Support Vector Machine (SVM)
# Ordinal logistic Regression: Coursera Week 11 Video 11.7 Last page
# Categorical Naive Bayes

# Subject to memory limitation
N = 5000

# data_copy = data[0:N]
data_copy = data.copy()
print(data_copy["Review"].shape)
#it_train = itoken(train$review, preprocessor = tolower, tokenizer = word_tokenizer)

from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse  import csr_matrix

## establish a document-term matrix
# Parameters require tunning
count_vect = CountVectorizer(ngram_range = (1,4), 
                             max_features = 10000,
                             min_df = 0.001,
                             max_df = 0.5, 
                             analyzer = "word")
X_train_counts = count_vect.fit_transform(data_copy["Review"])

# fit_transform returns one-dimensional array
X_train_counts.shape

# reshape into two-dimensional array
#X_train_counts = X_train_counts.reshape(N, -1)

# MUST convert csr_parse matrix to np.array! 
X_train_counts = X_train_counts.toarray()
print(X_train_counts.shape)

# combine X_train_counts and label

Y_train = np.array(data_copy["Rating"])
# Y_train = Y_train.reshape(,1)
print(X_train_counts.shape)

print(Y_train.shape)


print(type(X_train_counts))

# when two np.arrays have difference shape, must use np.concatenate(), instead of np.hstack()
#X_train = np.concatenate((X_train_counts, Y_train), axis = 1)
#print(X_train.shape) # should have one more column
#print(X_train[2,-1])

# Split training and test data
# Split 10% of total dataset as test data
# Split the remain 90% of total dataset into N folds. Use N-1 folds as training and the last 1 fold as test

# split training and test dataset using sklearn function train_test_split()
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_train_counts, Y_train, test_size=0.1, random_state=0)

#xpeng added session:
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
# Models
#from sklearn.tree import DecisionTreeClassifier
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.svm import SVC
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.naive_bayes import BernoulliNB

#tfid = TfidfVectorizer()
#train_tfid_matrix = tfid.fit_transform(X_train)
#test_tfid_matrix = tfid.transform(X_test)

#new_models = [DecisionTreeClassifier(),
#              RandomForestClassifier(),
#              SVC(),
#              KNeighborsClassifier(),
#              BernoulliNB()]

#accuracy = []

#for model in new_models:
#    cross_val = cross_val_score(model, train_tfid_matrix, y_train, scoring='accuracy',cv=StratifiedKFold(10)).mean()
#    accuracy.append(cross_val)

#models_name = ['DecisionTreeClassifier', 'RandomForestClassifier', 'SVC',
#        'KNeighborsClassifier', 'BernoulliNB']

#acc = pd.DataFrame({'Model': models_name, 'Accuracy': accuracy})
#acc

from sklearn.linear_model import LogisticRegression
# perform training
#lg = LogisticRegression(multi_class='ovr')
#lg = LogisticRegression(multi_class='multinomial')
lg = LogisticRegression(multi_class='auto')

lg_model = lg.fit(X_train, y_train)

# perform prediction
y_pred = lg_model.predict(X_test)



## evaluate prediction results
# return the mean accuracy 
print("The mean accuracy on the test set is: ",lg_model.score(X_test,y_test))

from sklearn.metrics import confusion_matrix
print("Below is confusion matrix. Entry at (i,j) denotes that the true value is i, but predicted as j.")
print("Number on diagonal are the ones correctly predicted.")

sns.color_palette("Blues", as_cmap=True)
sns.heatmap(confusion_matrix(y_test, y_pred), annot = True, cmap="Blues", fmt='g')
plt.show()



# 2-star is the most difficult to predict, followed by 3-star and 4-star

coefficients = pd.DataFrame(lg.coef_)
coefficients.to_csv("lg_coefficients.csv", index = True)

ngrams = pd.DataFrame(count_vect.get_feature_names_out())
ngrams.to_csv("lg_ngrams.csv", index= True)

# Try different lambda (regularization coefficient)


#lambda_set = [0.001, 0.01, 0.1, 1, 10, 100]
#lambda_set = [0.0001]
#for lambda_temp in lambda_set:
#  lg = LogisticRegression(multi_class='auto', C = 1/lambda_temp)
#  lg_model = lg.fit(X_train, y_train)

#  # perform prediction
#  y_pred = lg_model.predict(X_test)

#  print(confusion_matrix(y_test, y_pred))

# Let's change the rating to be more general and easier to understand
def rating(score):
    if score > 3:
        return 'Good'
    elif score == 3:
        return 'Netral'
    else:
        return 'Bad'

df = data_copy.copy()
df['Rating'] = df['Rating'].apply(rating)
X_train, X_test, y_train, y_test = train_test_split(df['Review'], df['Rating'], test_size=0.2)

X_train, X_test, y_train, y_test = train_test_split(data_copy['Review'], data_copy['Rating'], test_size=0.2)

import pickle
from tensorflow.keras.regularizers import l1, l2

#Tokenize the data
# tokenizer = Tokenizer()
# tokenizer.fit_on_texts(data["Review"].values)
# X=tokenizer.texts_to_sequences(data["Review"].values)
# X=pad_sequences(X, padding='post', maxlen=350)

# encoding = {1: 0,
#             2: 1,
#             3: 2,
#             4: 3,
#             5: 4
#            }

# labels = ['1', '2', '3', '4', '5']
           
# y = data['Rating'].copy()
# y.replace(encoding, inplace=True)

# #parameters for LSTM
# vocab_size = 49536
# print(vocab_size)
# embedding_dim = 16
# num_epochs=3
# batch_size=100
# units = 76

tokenizer = Tokenizer(num_words=10000, oov_token='<OOV>')

tokenizer.fit_on_texts(X_train)
# print(tokenizer.word_index)
total_word = len(tokenizer.word_index)
print('Total distinct words: {}'.format(total_word))

train_seq = tokenizer.texts_to_sequences(X_train)
train_padded = pad_sequences(train_seq)

test_seq = tokenizer.texts_to_sequences(X_test)
test_padded = pad_sequences(test_seq)

# One hot encoding the label
lb = LabelBinarizer()
train_labels = lb.fit_transform(y_train)
test_labels = lb.transform(y_test)

pickle.dump(tokenizer, open('tokenizer.pkl', 'wb'))
pickle.dump(lb, open('label.pkl', 'wb'))

model3 = tf.keras.models.Sequential([tf.keras.layers.Embedding(total_word, 8),
                                    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(16)),
                                    tf.keras.layers.Dropout(0.5),
                                    tf.keras.layers.Dense(8, kernel_regularizer=l2(0.001),
                                                          bias_regularizer=l2(0.001), activation='relu'),
                                    tf.keras.layers.Dropout(0.5),
                                    tf.keras.layers.Dense(3, activation='softmax')])

model3.summary()



#model3.compile(optimizer=tf.optimizers.Adam(learning_rate=0.05), loss='categorical_crossentropy', metrics=['accuracy'])

#model3.fit(train_padded, train_labels, epochs=3, validation_data=(test_padded, test_labels))

model1 = tf.keras.models.Sequential([tf.keras.layers.Embedding(total_word, 8),
                                    tf.keras.layers.LSTM(16),
                                    tf.keras.layers.Dense(3, activation='softmax')])

model1.summary()

#model1.compile(optimizer=tf.optimizers.Adam(learning_rate=0.05), loss='categorical_crossentropy', metrics=['accuracy'])

#model1.fit(train_padded, train_labels, epochs=3, validation_data=(test_padded, test_labels))

model2 = tf.keras.models.Sequential([tf.keras.layers.Embedding(total_word, 8),
                                    tf.keras.layers.LSTM(16),
                                    tf.keras.layers.Dropout(0.5),
                                    tf.keras.layers.Dense(3, activation='softmax')])

model2.summary()

#model2.compile(optimizer=tf.optimizers.Adam(learning_rate=0.05), loss='categorical_crossentropy', metrics=['accuracy'])

#model2.fit(train_padded, train_labels, epochs=3, validation_data=(test_padded, test_labels))

pred2 = model3.predict(test_padded)
true_labels = np.argmax(test_labels, axis=-1)
pred_labels = np.argmax(pred2, axis=-1)
print(confusion_matrix(true_labels, pred_labels))
print(classification_report(true_labels, pred_labels))

pred2 = model1.predict(test_padded)
true_labels = np.argmax(test_labels, axis=-1)
pred_labels = np.argmax(pred2, axis=-1)
print(confusion_matrix(true_labels, pred_labels))
print(classification_report(true_labels, pred_labels))

pred2 = model2.predict(test_padded)
true_labels = np.argmax(test_labels, axis=-1)
pred_labels = np.argmax(pred2, axis=-1)
print(confusion_matrix(true_labels, pred_labels))
print(classification_report(true_labels, pred_labels))