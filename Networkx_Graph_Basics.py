#import networkx for use 
import networkx as nx

#Initialize a graph 
g =nx.Graph()

#Creating a simple graph G(V,E)

#adding nodes to a graph 
g.add_node(1)
g.add_node(2)
g.add_node(3)
g.add_node(4)
print(g.nodes)

#ading edges to the graph 
g.add_edge(1,2)
g.add_edge(1,3)
g.add_edge(1,4)
g.add_edge(2,2)
g.add_edge(2,3)
g.add_edge(4,2)
print(g.edges)

#visualize the graph 
import matplotlib.pyplot as plt 
nx.draw(g)
plt.show()

print('Total number of nodes present in the graph: ',g.order())
print('Total number of edges present in the graph:',g.size())

#Creating various type of graphs :
    

#Creating complete graph with 8 vertices

cg = nx.complete_graph(3)
nx.draw(cg)
plt.show()

#Creating bi-pertite graph with 10 vertices:
bg = nx.complete_bipartite_graph(10,3)
nx.draw(bg)
plt.show()

#Creating planer graph :
pg = nx.path_graph(10)
pos = nx.planar_layout(pg)
nx.draw(pg)
plt.show()

#Creating a random graph with 20 nodes
    
rg = nx.gnp_random_graph(100,0.2)
nx.draw(rg,with_labels=1)
plt.show()

#find the degree of a graph :
n = int(input('Select one node: '))
print('Degree of node-',n,'is :',rg.degree(9))

#finf the neighbous of a perticular node 
print('neighbour of  node ',n,'is',rg.neighbors(n))

#Creating a complement of a graph 
u1 = nx.complete_graph(4)
u2 = nx.complement(u1)
nx.draw(u2)
plt.show()

x = nx.complement(rg)
nx.draw(x)
plt.show()

#union of two graph 
d =nx.disjoint_union(x,rg)
nx.draw(d)
plt.show()

#information related to a graph
print('summary : ',nx.info(rg))

#changing to circular layout
l = nx.circular_layout(rg)
nx.draw(rg,pos=l,with_labels=1)
plt.show()

y=nx.circular_layout(cg)
cg = nx.complete_graph(18)
nx.draw(cg,pos=y,with_labels=1)
plt.show()



