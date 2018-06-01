import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite


B = nx.Graph()

B.add_nodes_from([1, 2, 3, 4], bipartite=0)
B.add_nodes_from(['a', 'b', 'c'], bipartite=1)
B.add_edges_from([(1, 'a'), (1, 'b'), (2, 'b'), (2, 'c'), (3, 'c'), (4, 'a')])

plt.figure(figsize=(8, 8))

X, Y = bipartite.sets(B)
pos = dict()
pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
pos.update( (n, (2, i)) for i, n in enumerate(Y) ) # put nodes from Y at x=2

nx.draw(B, pos=pos, node_size=40, alpha=0.5, node_color="blue", with_labels=False)
plt.axis('equal')
plt.show()