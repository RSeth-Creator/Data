# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 22:27:29 2021

@author: raj kumar seth 

"""
#Facebdata analysis (SNAP data )
import pandas as pd 
import networkx as nx 
import matplotlib.pyplot as plt
g = nx.read_edgelist(r'C:\Users\rajse\OneDrive\Documents\Python Scripts\Social Network Analysis\Data\facebook_combined\facebook_combined.txt')
g.nodes()
nx.info(g)
nx.draw_circular(g)
plt.show()


g.nodes()
nx.draw(g,with_labels =True)
plt.show()

nx.info(g)

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
cc=sorted(clu.items(),key=lambda x:x[1],reverse=True)#[:10]

#Measiuring clustering coefficent
a_clu = nx.average_clustering(g)

#Diameter of the network 
d=nx.diameter(g)

t_deg=pd.DataFrame(sorted(g.degree(),key=lambda x:x[1],reverse=True)
                   ,columns=(['node','Degree']))#[:10]

#Degree centrality 
dc = nx.degree_centrality(g)
t_dc=pd.DataFrame(sorted(dc.items(),key=lambda x:x[1],reverse=True)
                  ,columns=(['node','Degree_Centrality']))#[:10]

#Closeness centrality 
cc = nx.closeness_centrality(g)

#Top 10 nodes 
t_cc=pd.DataFrame(sorted(cc.items(),key=lambda x:x[1],reverse=True)
                  ,columns=(['node','Closeness_Centrality']))#[:10]

#Betwenness centrality 
bc = nx.betweenness_centrality(g)
#print('Closeness centrality of the graph G is :', bc)
#Top 10 nodes 
t_bcc=pd.DataFrame(sorted(bc.items(),key=lambda x:x[1],reverse=True)
                 ,columns=(['node','Betweenness_Centrality']))#[:10])

#Eigenvalue centrality 
ec = nx.eigenvector_centrality_numpy(g)
#print('Closeness centrality of the graph G is :', ec)
#Top 10 nodes
t_ecc=pd.DataFrame(sorted(ec.items(),key=lambda x:x[1],reverse=True)
                 ,columns=(['node','Eigenvalue_Centrality']))#[:10]


clustering_coeff = nx.clustering(g)
c_coeff= pd.DataFrame(sorted(clustering_coeff.items(),key=lambda x:x[1],reverse=True)
                      ,columns = (['node','Clustering_Coeff']))#[:10]


# Single table with all the centrality measure  merge/ join
df1= pd.merge(t_cc, t_bcc, on='node', how='left')
df2= pd.merge(df1, t_dc, on='node', how='left')
df3= pd.merge(df2, t_ecc, on='node', how='left')
df4= pd.merge(df3, t_deg, on='node', how='left')
details=pd.merge(df4, c_coeff, on='node', how='left')

plt.scatter(details['node'], details['Eigenvalue_Centrality'],color='blue',alpha=0.6)
plt.scatter(details['node'], details['Betweenness_Centrality'],color='red')
plt.scatter(details['node'], details['Closeness_Centrality'],color='green')
plt.scatter(details['node'], details['Degree_Centrality'],color='yellow')
plt.show()
plt.scatter(details['node'], details['Clustering_Coeff'],color='red')
plt.show()





#common neighbour
targets = nx.non_edges(g)
common_neighbors = [(e[0],e[1],len(list(nx.common_neighbors(g,e[0],e[1]))))
                    for e in targets ]
common_neighbour = pd.DataFrame(sorted(common_neighbors,key=lambda x:x[2],reverse=True),
                                columns=(['Node_i','Node_j','Common_Nighbour']))


#Jaccard similarity cofficient
Jaccard_coeff = list(nx.jaccard_coefficient(g))
Jaccard_coeff = pd.DataFrame(sorted(Jaccard_coeff,key=lambda x:x[2],reverse=True),
                                columns=(['Node_i','Node_j','Jaccard_coeff']))


#Adamic -ADAR - Index
adamic_adar_index = list(nx.adamic_adar_index(g))
adamic_adar_index = pd.DataFrame(sorted(adamic_adar_index,key=lambda x:x[2],reverse=True),
                                columns=(['Node_i','Node_j','Node_j']))


#Jaccard_coeff.query('Jaccard_coeff>0.20 and Jaccard_coeff!=1 and Node_i == 23' )

def recom(id):
    print(list(Jaccard_coeff['Node_j'][(Jaccard_coeff['Node_i'] == id) & 
                              (Jaccard_coeff['Jaccard_coeff'] > .20)]))

    print(list(adamic_adar_index['Node_j'][(adamic_adar_index['Node_i'] == id) & 
                              (adamic_adar_index['adamic_adar_index'] > .20)]))


import networkx.algorithms.community as nxcom
communities = sorted(nxcom.greedy_modularity_communities(g), key=len, reverse=True)
    # Count the communities
print(f"Number of communities {len(communities)} communities.")





