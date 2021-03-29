# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 09:22:40 2021

@author: rajseth
"""
import re 
import pandas as pd 
import nltk
df = pd.read_csv('tweet.txt', delimiter = "\t",header=None)
df.columns = ['doc_id','tweets']
df.head()
#preprocessing
df['tweets'] = df['tweets'].str.lower()
df['tweets'] = df['tweets'] .map(lambda x: re.sub(r'[^A-Za-z0-9]+', ' ', x))

#WhitespaceTokenizer used to tokenize the words in a sentence
# WordNetLemmatizer used to find the root words
#Creating posting list for the corpus

w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()
posting_list = {}
for i, doc in enumerate(df['tweets']):
    for term in w_tokenizer.tokenize(doc):
         l_term = lemmatizer.lemmatize(term)
         if l_term in posting_list:
            posting_list[l_term].add(df['doc_id'][i])
         else: posting_list[l_term] = {df['doc_id'][i]}
         
posting_list = {key: val for key, val in sorted(posting_list.items(),
                                                key = lambda x: x[0])}


#Function to find out the posting list for any item

def item(text):
    x = list(posting_list[text])
    return x

#Merge Algorithm for AND operation

def merge_and(list1,list2):
    
    out=[]
    for i in range(len(list1)):
        for j in range(len(list2)):
            if list1[i] == list2[j]:
                out.append(list1[i])
            
    return out

merge_and(item('egg'),item('cheese')) 
item('egg')
item('cheese')
