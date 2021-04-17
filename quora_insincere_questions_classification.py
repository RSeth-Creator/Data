# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 23:07:10 2021

@author: raj kumar seth 

quora_insincere_questions classification 
Data collected from : Kaggle 
data feild: qid,question_text,target
question_text: string data format 
target: banary 1/0
Classification techniques: Naive bays ,Logistic regression
"""

import pandas as pd 
df_raw = pd.read_csv(r'C:\Users\rajse\OneDrive\Documents\Python Scripts\Machine Learning\data\quora_insincere_questions.csv')

df=df_raw.head(5000)
#plotting item vs individual catagory 
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(8,6))
df.groupby('target').question_text.count().plot.bar(ylim=0)
plt.show()

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer( ngram_range=(1, 2), stop_words='english')
features = tfidf.fit_transform(df.question_text).toarray()
labels = df.target
features.shape

#Applying naive bay's model to the dataset
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

X_train, X_test, y_train, y_test = train_test_split(df['question_text'], df['target'], random_state = 0)

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)


tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)


clf = MultinomialNB().fit(X_train_tfidf, y_train)


#Calculate the accuracy of the model along with the classification report
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import confusion_matrix
 
y_pred = clf.predict(count_vect.transform(X_test))
conf_mat = confusion_matrix(y_test, y_pred)
print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

import seaborn as sns
fig, ax = plt.subplots(figsize=(10,10))
sns.heatmap(conf_mat, annot=True, fmt='d')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()


from sklearn.linear_model import LogisticRegression

glm = LogisticRegression().fit(X_train_tfidf, y_train)

from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import confusion_matrix
 
y_pred = glm.predict(count_vect.transform(X_test))
conf_mat = confusion_matrix(y_test, y_pred)
print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

import seaborn as sns
fig, ax = plt.subplots(figsize=(10,10))
sns.heatmap(conf_mat, annot=True, fmt='d')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

