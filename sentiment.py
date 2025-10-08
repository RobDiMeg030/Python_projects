#### Import
import pandas as  p
import matplotlib.pyplot as plt
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Sentiment berechnen

def get_sentiment(text):
    blob = TextBlob(str(text))
    return blob.sentiment.polarity  # Wert zwischen -1 (negativ) und +1 (positiv)
## daten ziehen


daten =p.read_csv("sentiment_analysis.csv", encoding="utf-8")

vectorizer = CountVectorizer()

bow_matrix = vectorizer.fit_transform(daten["text"].astype(str))
labels=daten["sentiment"]

X_train, X_test, y_train, y_test = train_test_split(bow_matrix, labels, test_size=0.3, random_state=42)

decisionTree = DecisionTreeClassifier(random_state=99)

decisionTree.fit(X_train ,y_train)
answer=decisionTree.predict(X_test)
for i in range(10):
    idx = y_test.index[i]  # Index aus dem Original-Dataset
    print(f"Text: {daten['text'].iloc[idx]}")
    print(f"True Label: {y_test.iloc[i]}")
    print(f"Predicted Label: {answer[i]}")
    print(f"Sentiment: {get_sentiment(daten['text'].iloc[idx])}")
    print("-" * 40)
