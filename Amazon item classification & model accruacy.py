# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 18:34:27 2021

@author: raj kumar seth 

Item classification from amazon data 
Dataset collected from data.world:
 product_title,product_description,category
  product_title,product_description--> string data type
  category---> multiclass 
  Applying techniques:Logistic Regression, Multinomial naive bays , support vector machine 
"""
#Collect the data from data world 
import datadotworld as dw
results = dw.query(
	'promptcloud/product-listing-from-amazon-india', 
    'SELECT * FROM marketing_sample_for_amazon_in_ecommerce_20191001_20191031_30k_data LIMIT 2000')
results_df = results.dataframe

# create a custom dataframe for analysis the text data 
import pandas as pd 

df =results_df[['category']]
df['product_title_desc'] = results_df['product_title']#+' ' +results_df['product_description']

df['category_id'] = df['category'].factorize()[0]

# Data preprocessing 

#externally classify different kind of  item categoryies 
category_id_df = df[['category', 'category_id']].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'category']].values)

df['product_title_desc'] = df['product_title_desc'].fillna(' ')
#np.nan is an invalid document, expected byte or unicode string.
df['product_title_desc']=df['product_title_desc'].astype('U')
df.head()

#plotting item vs individual catagory 
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(8,6))
df.groupby('category').product_title_desc.count().plot.bar(ylim=0)
plt.show()

#Removing Stop words set the catageory in 0,1,2,3,4,5....
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer( ngram_range=(1, 2), stop_words='english')
features = tfidf.fit_transform(df.product_title_desc).toarray()
labels = df.category_id
features.shape

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

#Train and test data set created below 
X_train, X_test, y_train, y_test = train_test_split(df['product_title_desc'], df['category'], random_state = 0)

#Creating a sparse matrix bag of word
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
#print(X_train_counts)

#Create a tf-idf matrix from X_train_counts
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
#print(X_train_tfidf)


#Applying naive bay's model to the dataset
#fitting input and targe into the model
from sklearn.naive_bayes import MultinomialNB 
clf = MultinomialNB().fit(X_train_tfidf, y_train)

#Calculate the accuracy of the model along with the classification report
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import confusion_matrix

y_pred = clf.predict(count_vect.transform(X_test))
conf_mat = confusion_matrix(y_test, y_pred)
print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

#Plotting the confusion matrix 
import seaborn as sns
fig, ax = plt.subplots(figsize=(10,10))
sns.heatmap(conf_mat, annot=True, fmt='d',
            xticklabels=category_id_df.category.values, yticklabels=category_id_df.category.values)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

#check the model 
print(clf.predict(count_vect.transform(["Harveys Crunchy  Creame Gourmet Delicacies Cream Wafer Biscuit 110 g Pouch Pack  Chocolate Flavoured "])))



#Checking which classification model is giving best accuracy on top of the amazon data 
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
#Create a list with required model name 
models = [
    RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0),
    LinearSVC(),
    MultinomialNB(),
    LogisticRegression(random_state=0),
]
#Assing the level of cross validation to find the best accuracy
CV = 5  #cross validation number here it os 5 
cv_df = pd.DataFrame(index=range(CV * len(models)))
entries = []
for model in models:
  model_name = model.__class__.__name__
  accuracies = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)
  for fold_idx, accuracy in enumerate(accuracies):
    entries.append((model_name, fold_idx, accuracy))
cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])

#Showing which model giving the best accuracy
import seaborn as sns
sns.boxplot(x='model_name', y='accuracy', data=cv_df)
sns.stripplot(x='model_name', y='accuracy', data=cv_df, 
              size=8, jitter=True, edgecolor="gray", linewidth=2)
plt.show()

#finding out the accuracy mean for all the classification model 
cv_df.groupby('model_name').accuracy.mean()

#Check if the model is doing good
svc = LinearSVC().fit(X_train_tfidf, y_train)
print(svc.predict(count_vect.transform(["Harveys Crunchy  Creame Gourmet Delicacies Cream Wafer Biscuit 110 g Pouch Pack  Chocolate Flavoured "])))

#Applying SVC to the dataset as it has the highest accuracy
model_svc = LinearSVC()
X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index, test_size=0.33, random_state=0)
model_svc.fit(X_train, y_train)
y_pred = model_svc.predict(X_test)

from sklearn.metrics import confusion_matrix
conf_mat = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(10,10))
sns.heatmap(conf_mat, annot=True, fmt='d',
            xticklabels=category_id_df.category.values, yticklabels=category_id_df.category.values)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))



#Applying Naive bays 
clf = MultinomialNB()
#X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index, test_size=0.33, random_state=0)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

from sklearn.metrics import confusion_matrix
conf_mat = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(10,10))
sns.heatmap(conf_mat, annot=True, fmt='d',
            xticklabels=category_id_df.category.values, yticklabels=category_id_df.category.values)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
