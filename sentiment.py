#### Import
import pandas as  p
import matplotlib.pyplot as plt
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score




# Sentiment berechnen

def get_sentiment(text):
    blob = TextBlob(str(text))
    return blob.sentiment.polarity  # Wert zwischen -1 (negativ) und +1 (positiv)

## sentimnet wert ein label geben
def sentiment_to_label(polarity):
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"



## daten ziehen




daten =p.read_csv("sentiment_analysis.csv", encoding="utf-8")

#bag of words
vectorizer = CountVectorizer()

bow_matrix = vectorizer.fit_transform(daten["text"].astype(str))
labels=daten["sentiment"]

#trainungs und testdaten erstellen
X_train, X_test, y_train, y_test = train_test_split(bow_matrix, labels, test_size=0.3, random_state=42)

#decisiontree
decisionTree = DecisionTreeClassifier(random_state=99)

decisionTree.fit(X_train ,y_train)
answer=decisionTree.predict(X_test)

#sentiment werte
daten["sentiment_score"] = daten["text"].apply(get_sentiment)


# 10 werte ausgespuckt
for i in range(10):
    idx = y_test.index[i]  # Index aus dem Original-Dataset
    print(f"Text: {daten['text'].iloc[idx]}")
    print(f"True Label: {y_test.iloc[i]}")
    print(f"Predicted Label: {answer[i]}")
    print(f"Sentiment: {daten['sentiment_score'].iloc[idx]}")
    print("-" * 40)


#plot
daten["polarity"] = daten["text"].apply(get_sentiment)

# Nur Testdaten extrahieren
test_indices = y_test.index
sentiments = daten.loc[test_indices, "text"].apply(get_sentiment)
sentiment_preds = sentiments.apply(sentiment_to_label)


fig, axs = plt.subplots(1, 2, figsize=(14, 6))
label1=sorted(set(y_test))
all_labels = sorted(set(y_test) | set(sentiment_preds))

# Confusion Matrix
cm = confusion_matrix(y_test, answer,labels=label1)
disp = ConfusionMatrixDisplay(confusion_matrix=cm,display_labels=label1)
disp.plot(ax=axs[0], cmap="Blues")
axs[0].set_title("Confusion Matrix - Decison Tree")

# Sentiment-Verteilung




cm_sentiment = confusion_matrix(y_test, sentiment_preds, labels=all_labels)
disp_sentiment = ConfusionMatrixDisplay(confusion_matrix=cm_sentiment, display_labels=all_labels)
disp_sentiment.plot(ax=axs[1], cmap="Oranges", colorbar=False)
axs[1].set_title("Confusion Matrix – TextBlob Sentiment")





plt.tight_layout()
plt.show()

