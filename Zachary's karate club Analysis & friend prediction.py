# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 02:09:03 2021

@author: raj kumar seth 
"""
import pandas as pd 
import networkx as nx 
g = nx.read_gml(r'C:\Users\rajse\OneDrive\Documents\Python Scripts\Social Network Analysis\Data\karate\karate.gml',label = 'id')
nx.info(g)
import matplotlib.pyplot as plt

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
plt.scatter(details['node'], details['Eigenvalue_Centrality'],color='blue')
plt.show()
plt.scatter(details['node'], details['Betweenness_Centrality'],color='red')
plt.show()
plt.scatter(details['node'], details['Closeness_Centrality'],color='green')
plt.show()
plt.scatter(details['node'], details['Degree_Centrality'],color='yellow')
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
                                columns=(['Node_i','Node_j','adamic_adar_index']))



import networkx.algorithms.community as nxcom
communities = sorted(nxcom.greedy_modularity_communities(g), key=len, reverse=True)
    # Count the communities
print(f"The karate club has {len(communities)} communities.")


pos = nx.spring_layout(g, k=0.1)
plt.rcParams.update({'figure.figsize': (15, 10)})
nx.draw_networkx(
        g, 
        pos=pos, 
        node_size=0, 
        edge_color="#444444", 
        alpha=0.05, 
        with_labels=False)

plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams.update({'figure.figsize': (15, 10)})
cliques = list(nx.find_cliques(g))
max_clique = max(cliques, key=len)
node_color = [(0.5, 0.5, 0.5) for v in g.nodes()]
for i, v in enumerate(g.nodes()):
        if v in max_clique:
            node_color[i] = (0.5, 0.5, 0.9)
nx.draw_networkx(g, node_color=node_color)

def set_node_community(G, communities):
        '''Add community to node attributes'''
        for c, v_c in enumerate(communities):
            for v in v_c:
                # Add 1 to save 0 for external edges
                G.nodes[v]['community'] = c + 1

def set_edge_community(G):
        '''Find internal edges and add their community to their attributes'''
        for v, w, in G.edges:
            if G.nodes[v]['community'] == G.nodes[w]['community']:
                # Internal edge, mark with community
                G.edges[v, w]['community'] = G.nodes[v]['community']
            else:
                # External edge, mark as 0
                G.edges[v, w]['community'] = 0

def get_color(i, r_off=1, g_off=1, b_off=1):
        '''Assign a color to a vertex.'''
        r0, g0, b0 = 0, 0, 0
        n = 16
        low, high = 0.1, 0.9
        span = high - low
        r = low + span * (((i + r_off) * 3) % n) / (n - 1)
        g = low + span * (((i + g_off) * 5) % n) / (n - 1)
        b = low + span * (((i + b_off) * 7) % n) / (n - 1)
        return (r, g, b)            
#With this we now assign the community info to the elements:

    # Set node and edge communities
set_node_community(g, communities)
set_edge_community(g)

node_color = [get_color(g.nodes[v]['community']) for v in g.nodes]

    # Set community color for edges between members of the same community (internal) and intra-community edges (external)
external = [(v, w) for v, w in g.edges if g.edges[v, w]['community'] == 0]
internal = [(v, w) for v, w in g.edges if g.edges[v, w]['community'] > 0]
internal_color = ['black' for e in internal]
#A little plot now gives a better idea of how the karate club communities are:

karate_pos = nx.spring_layout(g)

plt.rcParams.update({'figure.figsize': (15, 10)})
    # Draw external edges
nx.draw_networkx(
        g,
        pos=karate_pos,
        node_size=0,
        edgelist=external,
        edge_color="silver")
    # Draw nodes and internal edges
nx.draw_networkx(
        g,
        pos=karate_pos,
        node_color=node_color,
        edgelist=internal,
        edge_color=internal_color)




#Jaccard_coeff.query('Jaccard_coeff>0.20 and Jaccard_coeff!=1 and Node_i == 23' )

def recom(id):
    print(list(Jaccard_coeff['Node_j'][(Jaccard_coeff['Node_i'] == id) & 
                              (Jaccard_coeff['Jaccard_coeff'] > .20)]))

    print(list(adamic_adar_index['Node_j'][(adamic_adar_index['Node_i'] == id) & 
                              (adamic_adar_index['adamic_adar_index'] > 0.4)]))
    




recom(3)
