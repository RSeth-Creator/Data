# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 22:53:00 2021

@author: raj kumar seth 

Data : Dataset collected from data.world  
Goal:Predict the movie rating using linear regression model 
run : 'dw configure' in cmd shell & Provide access code 
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

#Remove all tha NA value with forward filling
results_df = results_df.fillna(method='ffill', axis=0)

# creating dataframe with  numerical attributes
df = results_df[['runtime_minutes','votes','revenue_millions',
                 'metascore','rating']]
df.head()

#Normalize  voting,runtime_minutes,revenue_millions using  z score

df['votes'] = (df['votes']- np.mean(df['votes']))/np.std(df['votes'])
df['runtime_minutes'] = (df['runtime_minutes']- np.mean(df['runtime_minutes']))/np.std(df['runtime_minutes'])
df['revenue_millions'] = (df['revenue_millions']- np.mean(df['revenue_millions']))/np.std(df['revenue_millions'])


#Reframe dataset : Add new Binary column Action, Thriller, Comedy, Romance, Drama

df['Action'] = results_df['genre'].str.contains('Action').astype(int)
df['Adventure'] = results_df['genre'].str.contains('Adventure').astype(int)
df['Sci-Fi'] = results_df['genre'].str.contains('Sci-Fi').astype(int)
df['Animation'] = results_df['genre'].str.contains('Animation').astype(int)
df['Comedy'] = results_df['genre'].str.contains('Comedy').astype(int)
df['Family'] = results_df['genre'].str.contains('Family').astype(int)
df['Drama'] = results_df['genre'].str.contains('Drama').astype(int)
df['Romance'] = results_df['genre'].str.contains('Romance').astype(int)
df['History'] = results_df['genre'].str.contains('History').astype(int)
df['Horror'] = results_df['genre'].str.contains('Horror').astype(int)
df['Thriller'] = results_df['genre'].str.contains('Thriller').astype(int)


#analysis of the data 
Summary = df.describe()

genre = ['Action', 'Adventure', 'Sci-Fi', 'Animation', 'Comedy',
         'Family', 'Drama', 'Romance', 'History', 'Horror','Thriller']
no = [sum(df['Action']),sum(df['Adventure']),sum(df['Sci-Fi']),sum(df['Animation'])
            ,sum(df['Comedy']),sum(df['Family']),sum(df['Drama']),sum(df['Romance']),
             sum(df['History']),sum(df['Horror']),sum(df['Thriller'])]
plt.bar(genre,no)
plt.show()

#Visualization (histogram)
plt.hist2d(df['rating'],df['metascore'])
plt.hist(df['rating'])
plt.hist(df['metascore'])
plt.hist(df['runtime_minutes'])
plt.hist(df['votes'])
plt.hist(df['revenue_millions'])

#Comparing ratings with other attributes 
plt.scatter(df['rating'], df['runtime_minutes'])
plt.show()
plt.scatter(df['rating'], df['votes'])
plt.show()
plt.scatter(df['rating'], df['revenue_millions'])
plt.show()

#Creating Input set/independent attribute 
x = df[['Action', 'Adventure', 'Sci-Fi', 'Animation', 'Comedy',
         'Family', 'Drama', 'Romance', 'History', 'Horror','Thriller'
         ,'runtime_minutes','votes','revenue_millions']]
x = df[['Action', 'Adventure', 'Sci-Fi', 'Animation', 'Comedy','Family', 'Drama', 'Romance', 'History', 'Horror','Thriller']]
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
predictions = model.predict(x_test)
plt.scatter(y_test, predictions)
comp = pd.DataFrame(list(y_test), list(predictions))
plt.hist(y_test - predictions)
plt.hist2d(y_test,predictions)


#Evaluation (Error in prediction)
MAE = metrics.mean_absolute_error(y_test, predictions)
MSE =  metrics.mean_squared_error(y_test, predictions)
RMSE = np.sqrt(metrics.mean_squared_error(y_test, predictions))
print('Errors are :','\n','Mean Absolute Error = ',MAE,
      '\n','Mean Square Error = ',MSE,'\n',
      'Root Mean Square Error = ',RMSE)


#Implementation of decision tree in movie dataset 
dfr = pd.DataFrame()
dfr['Action'] = results_df['genre'].str.contains('Action')#.astype(int)
dfr['Adventure'] = results_df['genre'].str.contains('Adventure')#.astype(int)
dfr['Sci-Fi'] = results_df['genre'].str.contains('Sci-Fi')#.astype(int)
dfr['Animation'] = results_df['genre'].str.contains('Animation')#.astype(int)
dfr['Comedy'] = results_df['genre'].str.contains('Comedy')#.astype(int)
dfr['Family'] = results_df['genre'].str.contains('Family')#.astype(int)
dfr['Drama'] = results_df['genre'].str.contains('Drama')#.astype(int)
dfr['Romance'] = results_df['genre'].str.contains('Romance')#.astype(int)
dfr['History'] = results_df['genre'].str.contains('History')#.astype(int)
dfr['Horror'] = results_df['genre'].str.contains('Horror')#.astype(int)
dfr['Thriller'] = results_df['genre'].str.contains('Thriller')#.astype(int)
dfr['Score'] = df['rating']
dfr['votes'] = df['votes']
dfr['runtime_minutes'] = df['runtime_minutes']
dfr['revenue_millions'] = df['revenue_millions']

xr=df[['Action', 'Adventure', 'Sci-Fi', 'Animation', 'Comedy',
         'Family', 'Drama', 'Romance', 'History', 'Horror','Thriller']]
        # ,'runtime_minutes','votes','revenue_millions']]
         
yr = dfr['Score']
# import the regressor
from sklearn.tree import DecisionTreeRegressor 
xr_train, xr_test, yr_train, yr_test = train_test_split(xr, yr, test_size = 0.2) 
# create a regressor object
regressor = DecisionTreeRegressor(random_state = 0) 
  
# fit the regressor with X and Y data

regressor.fit(xr_train, yr_train)

prediction_d = regressor.predict(xr_test)

plt.scatter(yr_test, prediction_d)
d_comp = pd.DataFrame(list(yr_test), list(prediction_d))

#Evaluation (Error in prediction)
MAE = metrics.mean_absolute_error(yr_test, prediction_d)
MSE =  metrics.mean_squared_error(yr_test, prediction_d)
RMSE = np.sqrt(metrics.mean_squared_error(yr_test, prediction_d))
print('Errors are :','\n','Mean Absolute Error = ',MAE,
      '\n','Mean Square Error = ',MSE,'\n',
      'Root Mean Square Error = ',RMSE)


from sklearn.ensemble import RandomForestRegressor
xf_train, xf_test, yf_train, yf_test = train_test_split(xr, yr, test_size = 0.2)
rf = RandomForestRegressor()
rf.fit(xf_train, yf_train)

prediction_rf = rf.predict(xf_test)

plt.scatter(y_test, prediction_rf)
r_comp = pd.DataFrame(list(yf_test), list(prediction_rf))

MAE = metrics.mean_absolute_error(yf_test, prediction_rf)
MSE =  metrics.mean_squared_error(yf_test, prediction_rf)
RMSE = np.sqrt(metrics.mean_squared_error(yf_test, prediction_rf))
print('Errors are :','\n','Mean Absolute Error = ',MAE,
      '\n','Mean Square Error = ',MSE,'\n',
      'Root Mean Square Error = ',RMSE)
