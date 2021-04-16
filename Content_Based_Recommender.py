# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 17:27:06 2021

@author: raj kumar seth 
"""
import re
import nltk
from nltk import word_tokenize
from collections import Counter
import string
import numpy as np
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#Collect Amazon product data from data.world
import datadotworld as dw
results = dw.query(
	'promptcloud/product-listing-from-amazon-india', 
    'SELECT * FROM marketing_sample_for_amazon_in_ecommerce_20191001_20191031_30k_data LIMIT 2000')
results_df = results.dataframe

#Dropping unnecessari columns 
df = results_df[['category','product_title','product_description','brand']]
df = pd.DataFrame(df)
#Summary of the dataframe
summary = df.describe()

#Data preprocessing
df['bow'] = df['category'] +' ' + df['product_title'] +' '+ df['product_description']
df['bow'] = df['bow'].str.lower()
df['bow'] = df['bow'].str.replace('[^A-Za-z0-9 ]+', ' ')
df['brand'] = df['brand'].str.replace('[^A-Za-z0-9 ]+', ' ')
df['brand']  = results_df['brand'].str.lower()
df['brand']= df['brand'].str.replace(" ","")
df = df.dropna()

df = df.set_index('brand')

# Initialize
#vectorizer = TfidfVectorizer(stop_words='english')
vectorizer = CountVectorizer(stop_words='english')
vec = vectorizer.fit_transform(df['bow'])

# Create dataFrame
bow = pd.DataFrame(vec.toarray().transpose(),
                   index=vectorizer.get_feature_names())
 

index = pd.Series(df.index)

index[:5]

cos_sim = cosine_similarity(vec,vec)

#############################################################
x  = results_df['brand'].str.lower()
x=x.str.replace('[^A-Za-z0-9 ]+', ' ')
x= x.str.replace(" ","")


#Creating a corpus (a flat document from the data frame)
corpus = ''
for i in range (len(x)):
    corpus += " ".join([str(x[i]),' '])

#Cleaning the bad character from the dataset
cleaned_corpus= re.sub('[^A-Za-z0-9 ]+', ' ', corpus)

#find out all the terms 
terms= nltk.word_tokenize(cleaned_corpus)
vocabs  = set(terms)
term_counts = Counter(terms)

'''
#frequency distribution of the corpus -analysis purpose 
data_analysis = pd.DataFrame(nltk.FreqDist(terms),index=[0])
nltk.FreqDist(terms).plot()
'''
total_count = float(sum(term_counts.values()))

#create dictionary to store the probabilities 
p_term = {terms: term_counts[terms] / total_count  for terms in term_counts.keys()}


#Create the edit operations

# Create permuterm index 
def permuterm(term):
  return [(term[:i], term[i:]) for i in range(len(term) + 1)]

#Delete operation
def delete(term):
  return [l + r[1:] for l,r in permuterm(term) if r]

#Swap oeration 
def swap(term):
  return [l + r[1] + r[0] + r[2:] for l, r in permuterm(term) if len(r)>1]


#Replace Operation 
def replace(term):
#find out all the characters in english dictionary
  letters = string.ascii_lowercase
  return [l + c + r[1:] for l, r in  permuterm(term)  if r for c in letters]

#Insert Operation
def insert(term):
  letters = string.ascii_lowercase
  return [l + c + r for l, r in permuterm(term)  for c in letters]

#print(insert('index'),end='')

#one edit distance for the correction 
def edit1(term):
  return set(delete(term) + swap(term) + replace(term) + insert(term))

#two edit distance to correction 
def edit2(term):
  return set(e2 for e1 in edit1(term) for e2 in edit1(e1))


#find out the best guess for a term based on probability 
def correct_spelling(term, vocabulary, probabilities):
  '''if term in vocabulary:
    print(term,' is already correctly spelt')
  return term
'''

  suggestions = edit1(term) or edit2(term) or [term]
  best_guesses = [w for w in suggestions if w in vocabulary]
  return [(w, probabilities[w]) for w in best_guesses]

#take user input to find out what is the suggestion / auto correction 
def term(term):
        corrections = correct_spelling(term, vocabs, p_term)
        
        if corrections:
          print(corrections)
          probs = np.array([c[1] for c in corrections])
          best_ix = np.argmax(probs)
          correct = corrections[best_ix][0]
          print('According to the input : ',term,'\n',
                ' you are looking for : ',correct )
        return correct 
#term('leeposh')
################################################################


def rec(item,cos_sim=cos_sim):
    rec_item =[]
    i = index[index ==item].index[0]
    score = pd.Series(cos_sim[i]).sort_values(ascending = True)
    top_item = list(score.iloc[1:10].index)
    for i in top_item:
        rec_item.append(list(df.index)[i])
    return rec_item


for i in range(5):
    user_input = input('Please enter the item name:')
    print('below are some items you could check :','\n',rec(term(user_input)))








