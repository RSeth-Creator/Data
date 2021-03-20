# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 22:27:29 2021

@author: raj kumar seth 

"""
#Facebdata analysis (SNAP data )
import networkx as nx 
import matplotlib.pyplot as plt
g = nx.read_edgelist(r'C:\Users\rajse\OneDrive\Documents\Python Scripts\Social Network Analysis\Data\facebook_combined\facebook_combined.txt')
g.nodes()
nx.info(g)
nx.draw_circular(g)
plt.show()

#Plotting degree distribution graph 
deg = nx.degree(g)
d = list(dict(nx.degree(g)).values())
u_deg = list(set(d))

l=[]

for i in u_deg:
    x = d.count(i)
    l.append(x)

plt.plot(u_deg,l)
plt.xlabel('Degree')
plt.ylabel('Pk')
plt.title('Degree distribution')
plt.show()
#graph showing that it follows power law distribution

#Find out the density of the graph 
den = nx.density(g)

#Measiuring clustering coefficent
clu = nx.clustering(g)
cc=sorted(clu.items(),key=lambda x:x[1],reverse=True)[:10]

#Measiuring clustering coefficent
a_clu = nx.average_clustering(g)

#Diameter of the network 
d=nx.diameter(g)


td=sorted(g.degree(),key=lambda x:x[1],reverse=True)[:10]

#Degree centrality 
dc = nx.degree_centrality(g)

#Top 10 nodes 
tdc=sorted(dc.items(),key=lambda x:x[1],reverse=True)[:10]

#Closeness centrality 
cc = nx.closeness_centrality(g)

#Top 10 nodes 
tcc=sorted(cc.items(),key=lambda x:x[1],reverse=True)[:10]

#Betwenness centrality 
bc = nx.betweenness_centrality(g)
#print('Closeness centrality of the graph G is :', bc)
#Top 10 nodes 
bcc=sorted(bc.items(),key=lambda x:x[1],reverse=True)[:10]

#Eigenvalue centrality 
ec = nx.eigenvector_centrality_numpy(g)
#print('Closeness centrality of the graph G is :', ec)
#Top 10 nodes
ecc=sorted(ec.items(),key=lambda x:x[1],reverse=True)[:10]

#Jaccard similarity cofficient
jc=nx.jaccard_coefficient(g)
#load the value into dictionary
pred={}
for u,v,p in jc:
    pred[(u,v)]=p
#Top 10 nodes    
jsc=sorted(pred.items(),key=lambda x:x[1],reverse=True)[:10]


clustering_coeff = nx.clustering(g)
c_coeff= sorted(clustering_coeff.items(),key=lambda x:x[1],reverse=True)[:10]

#presenting the key points 
print(nx.average_shortest_path_length(g))
print('Diameter of the network: ',d)
print('Density of the graph is : ',den) 
print('Information summary of the graph: ', nx.info(g))
print('top 10 nodes with max clustering coefficient  :', cc)
print('Average clustering coefficient  :', a_clu)
print('top 10 nodes with max degree/ connection :',td)
print('top 10 nodes with max degree centrality :', tdc)
print('top 10 nodes with max Closeness centrality :', tcc)
print('top 10 nodes with max Betwenness centrality :', bcc)
print('top 10 nodes with max Eigenvalue centrality  :', ecc)
print('top 10 nodes with max Jaccard similarity cofficient :', jsc)
print('top 10 nodes with max clustering  cofficient :', c_coeff)
import pandas as pd 
tbl = pd.DataFrame(jsc,columns=('node','Jaccard_similarity'))
tbl


