# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 20:49:24 2021

@author: rajkumarseth 
"""

import pandas as pd
import numpy as np 
from collections import Counter
import string
import re
import nltk  


#Import english word dictionary from data world
df = pd.read_csv('https://query.data.world/s/65ofulqys6udqlx3gwqvdkis7xqjlr')
df.head()


#Creating a corpus (a flat document from the data frame)
corpus = ''
for i in range (len(df)):
    corpus += " ".join([str(df.iloc[i][0]), str(df.iloc[i][1]),
                   str(df.iloc[i][2]), str(df.iloc[i][3])])

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

#one edit distance for the correction 
def edit1(term):
  return set(delete(term) + swap(term) + replace(term) + insert(term))

#two edit distance to correction 
def edit2(term):
  return set(e2 for e1 in edit1(term) for e2 in edit1(e1))


#find out the best guess for a term based on probability 
def correct_spelling(term, vocabulary, probabilities):
  if term in vocabulary:
    print(term,' is already correctly spelt')
    return 

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
          print(correct, 'is suggested for', term)
        
