# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 23:39:52 2021

@author: raj kumar seth 

"""
import networkx as nx 
import matplotlib.pyplot as plt 

#initialize graph 
g=nx.gnp_random_graph(123,0.3)
deg = nx.degree(g)
#print the degree of each individual nodes
print(deg)

#find out all the degree of all nodes 
all_deg = list(dict(deg).values())
all_deg

#find out all the unique degree 
u_deg = list(set(all_deg))

cnt =[]

for i in u_deg:
    x = all_deg.count(i)
    cnt.append(x)


plt.plot(u_deg,cnt)
plt.show()


# now make it as a function 

def degree_dist(g):
        deg = nx.degree(g)
        all_deg = list(dict(deg).values()) 
        u_deg = list(set(all_deg))
        
        cnt =[]
        
        for i in u_deg:
            x = all_deg.count(i)
            cnt.append(x)
        
        plt.plot(u_deg,cnt)
        plt.xlabel('Degrees')
        plt.ylabel('Count')
        plt.title('Degree distribution')
        plt.time()
        plt.show()


degree_dist(g)


import pandas as pd 
df =  pd.DataFrame(u_deg,cnt)
df


#Find out the density of the graph 
den = nx.density(g)
print('Density of the graph is : ',den)

#Measiuring clustering coefficent

clu = nx.clustering(g)
cc=sorted(clu.items(),key=lambda x:x[1],reverse=True)[:5]
print('top 10 nodes with max clustering coefficient  :', cc)

#Measiuring clustering coefficent
a_clu = nx.average_clustering(g)
print('Average clustering coefficient  :', a_clu)


#Diameter of the network 

d=nx.diameter(g)
print('Diameter of the network: ',d)


















