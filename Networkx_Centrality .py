# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 20:03:43 2021

@author: raj kumar seth
"""
import networkx as nx 
import matplotlib.pyplot as plt 
g=nx.gnp_random_graph(123,0.3)
nx.draw(g,with_labels=1)
plt.show()

print(nx.info(g))

td=sorted(g.degree(),key=lambda x:x[1],reverse=True)[:10]
print('top 10nodes with max degree/ connection :',td)
#Degree centrality 

dc = nx.degree_centrality(g)
print('degree centrality of the graph G is :', dc)
plt.hist(dc, alpha=0.5)
plt.yscale('log')
plt.title('degree centrality')
plt.show()
#Top 10 nodes 
tdc=sorted(dc.items(),key=lambda x:x[1],reverse=True)[:10]
print('top 10 nodes with max degree centrality :', tdc)


#Closeness centrality 
cc = nx.closeness_centrality(g)
print('Closeness centrality of the graph G is :', cc)
#Top 10 nodes 
tcc=sorted(cc.items(),key=lambda x:x[1],reverse=True)[:10]
print('top 10 nodes with max Closeness centrality :', tcc)

#Betwenness centrality 
bc = nx.betweenness_centrality(g)
print('Closeness centrality of the graph G is :', bc)
#Top 10 nodes 
bcc=sorted(bc.items(),key=lambda x:x[1],reverse=True)[:10]
print('top 10 nodes with max Betwenness centrality :', bcc)


#Eigenvalue centrality 
ec = nx.eigenvector_centrality_numpy(g)
print('Closeness centrality of the graph G is :', ec)
#Top 10 nodes
ecc=sorted(ec.items(),key=lambda x:x[1],reverse=True)[:10]
print('top 10 nodes with max Eigenvalue centrality  :', ecc)


#Jaccard similarity cofficient
jc=nx.jaccard_coefficient(g)
#load the value into dictionary
pred={}
for u,v,p in jc:
    pred[(u,v)]=p
#Top 10 nodes    
jsc=sorted(pred.items(),key=lambda x:x[1],reverse=True)[:10]
print('top 10 nodes with max Jaccard similarity cofficient :', jsc)
    