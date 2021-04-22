# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 12:25:39 2021

@author: rajKumar Seth 

Collaborative filtering 

dataset:https://data.world/datafiniti/amazon-and-best-buy-electronics/workspace/query?filename=DatafinitiElectronicsProductData.csv&newQueryType=SQL&selectedTable=datafinitielectronicsproductdata&tempId=1618988925609
"""
import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
import datadotworld as dw
results = dw.query(
	'datafiniti/amazon-and-best-buy-electronics', 
    'SELECT asins,manufacturer,name,brand,reviews_rating,reviews_text,reviews_username FROM datafinitielectronicsproductdata')
df = results.dataframe

#User-Item collaborative filtering
rating_crosstab_UI = df.pivot_table(values='reviews_rating', index='reviews_username', columns='brand', fill_value=0)
rating_crosstab_UI.head()
X = rating_crosstab_UI.T

SVD = TruncatedSVD(n_components=12, random_state=5)
resultant_matrix = SVD.fit_transform(X)
resultant_matrix.shape

corr_mat = np.corrcoef(resultant_matrix)
corr_mat.shape

def user_item(item):
        col_idx = rating_crosstab_UI.columns.get_loc(item)
        corr_specific = corr_mat[col_idx]
        return pd.DataFrame({'corr_specific':corr_specific, 'Items': rating_crosstab_UI.columns})\
                                .sort_values('corr_specific', ascending=False)\
                                .head(10)

#user_item('Microsoft')

#User-user collaborative filtering 

rating_crosstab_UU = df.pivot_table(values='reviews_rating', index='brand', columns='reviews_username', fill_value=0)
rating_crosstab_UU.head()
X = rating_crosstab_UU.T
SVD = TruncatedSVD(n_components=12, random_state=5)
resultant_matrix = SVD.fit_transform(X)
resultant_matrix.shape

corr_mat = np.corrcoef(resultant_matrix)
corr_mat.shape
def user_user(name):
    col_idx = rating_crosstab_UU.columns.get_loc(name)
    corr_specific = corr_mat[col_idx]
    return pd.DataFrame({'corr_specific':corr_specific, 'Items': rating_crosstab_UU.columns})\
                            .sort_values('corr_specific', ascending=False)\
                            .head(5)


#user_user('Appa')

#User-review recommender
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

u_df = df[['reviews_username','reviews_text']]
u_df = pd.DataFrame(u_df)
#Summary of the dataframe
summary = df.describe()

#Data preprocessing
u_df['reviews_text'] = u_df['reviews_text'].str.lower()
u_df['reviews_text'] = u_df['reviews_text'].str.replace('[^A-Za-z]+', ' ')
u_df = u_df.dropna()
u_df = u_df.set_index('reviews_username')

vectorizer = CountVectorizer(stop_words='english')
vec = vectorizer.fit_transform(u_df['reviews_text'])


bow = pd.DataFrame(vec.toarray().transpose(),
                   index=vectorizer.get_feature_names())
                   
index = pd.Series(u_df.index)
#index[:5]
cos_sim = cosine_similarity(vec,vec)                                     
def rec(name,cos_sim=cos_sim):
    rec_name =[]
    i = index[index == name].index[0]
    score = pd.Series(cos_sim[i]).sort_values(ascending = True)
    top_item = list(score.iloc[1:5].index)
    for i in top_item:
        rec_name.append(list(u_df.index)[i])
    return rec_name                   
                   
#rec('Appa')   

#Plot a graph to find the community 
import networkx as nx 

results = dw.query(
	'datafiniti/amazon-and-best-buy-electronics', 
    'SELECT brand,reviews_username FROM datafinitielectronicsproductdata ')
net = results.dataframe
G = nx.from_pandas_edgelist(net,source ='reviews_username' ,target ='brand' )

nx.draw(G,with_labels = False)




















             
