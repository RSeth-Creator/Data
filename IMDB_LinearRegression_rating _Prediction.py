# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 22:53:00 2021

@author: rajseth 
Data : Dataset collected from data.world  
Goal:Predict the movie rating using linear regression based on attributes(rank,title,genre,description
    director,actors,year,runtime_minutes,rating,votes,revenue_millions,metascore
) 
run : 'dw configure' in cmd shell 
and give the access code 
Data set link: https://data.world/promptcloud/imdb-data-from-2006-to-2016/workspace/file?filename=IMDB-Movie-Data.csv
"""
import pandas as pd 
import numpy as np 
import datadotworld as dw
from matplotlib import pyplot as plt 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics


#Import IMDB Movie dataset from dataworld 

results = dw.query(
	'promptcloud/imdb-data-from-2006-to-2016', 
    'SELECT * FROM imdb_movie_data')
results_df = results.dataframe
results_df.head()

results_df = results_df.fillna(method='ffill', axis=0)

# creating dataframe with  numerical attributes
df = results_df[['rank','runtime_minutes','votes','revenue_millions',
                 'metascore','rating']]
df.head()

#analysis of the data 
plt.hist2d(df['rating'],df['metascore'])
plt.hist(df['rating'])
plt.hist(df['metascore'])
plt.hist(df['runtime_minutes'])
plt.hist(df['votes'])
plt.hist(df['revenue_millions'])

#Comparing ratings with other attributes 
plt.scatter(df['rating'], df['metascore'])
plt.show()
plt.scatter(df['rating'], df['rank'])
plt.show()
plt.scatter(df['rating'], df['runtime_minutes'])
plt.show()
plt.scatter(df['rating'], df['votes'])
plt.show()
plt.scatter(df['rating'], df['revenue_millions'])
plt.show()

#Creating Input set/independent attribute 
x = results_df[['rank','runtime_minutes','votes','revenue_millions',
                 'metascore']]
#Dependent Attribute 
y = df['rating']

#Find the correlation matrix df 
cor_df = pd.DataFrame(df.corr())
cor_df

#Mathematical way to find the coefficients 
#[w] = [Inverse([x]T*[x])*([x]T*r)]
coeff = np.dot(np.linalg.inv(np.dot(np.transpose(x),x)),np.dot(np.transpose(x),df['rating']))


#Linear regression Mmodel Using sklearn 

#Create training and testing dataset  
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)
model = LinearRegression()

#Use fit method to train the model 
model.fit(x_train, y_train)
m_intercept = model.intercept_
m_coef = pd.DataFrame(model.coef_, x.columns, columns = ['Coeff'])

# prediction the output from test data 
#x_test = ([10,8,9,10,8],[2,1,3,4,5])

predictions = model.predict(x_test)
plt.scatter(y_test, predictions)
comp = pd.DataFrame(list(y_test), list(predictions))
plt.hist(y_test - predictions)

 #Evaluation (Error in prediction)
MAE = metrics.mean_absolute_error(y_test, predictions)
MSE =  metrics.mean_squared_error(y_test, predictions)
RMSE = np.sqrt(metrics.mean_squared_error(y_test, predictions))
print('Errors are :','\n','Mean Absolute Error = ',MAE,
      '\n','Mean Square Error = ',MSE,'\n',
      'Root Mean Square Error = ',RMSE)