import networkx as nx
from rdflib import Graph, Namespace, URIRef
'''
The below code is a python script for Computing MVF algorithm via Lemma 6 using rdflib
'''

# Read .ttl file and create a directed graph
g = Graph()
g.parse("C:/Users/prana/Desktop/Masters Thesis/test_files/example-product-1.ttl", format="turtle")

# Create directed graph
DG = nx.DiGraph()

ex = Namespace("http://example.org/")
rdf_type = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")

for s, p, o in g:
    if p != rdf_type:
        DG.add_edge(str(s), str(o))


# Define maxWeight function
def maxWeight(G, V, wgt, size):
    current = 0
    for W in [U for U in G if (V, U) in G.edges()]:
        if wgt[W] is None:
            current = max(current, maxWeight(G, W, wgt, size))
        else:
            current = max(current, wgt[W])
    wgt[V] = current + size[V]
    return wgt[V]


# Implementing the Algorithm
def calculate_MVF(v):
    SCC = list(nx.strongly_connected_components(DG))
    node_to_scc_map = {node: i for i, comp in enumerate(SCC) for node in comp}
    scc_size_map = {i: len(comp) for i, comp in enumerate(SCC)}
    SCC_graph = nx.DiGraph()
    for node in node_to_scc_map:
        SCC_graph.add_node(node_to_scc_map[node])
    for edge in DG.edges():
        if node_to_scc_map[edge[0]] != node_to_scc_map[edge[1]]:
            SCC_graph.add_edge(node_to_scc_map[edge[0]], node_to_scc_map[edge[1]])
    wgt = {node: None for node in SCC_graph.nodes()}
    mvf = maxWeight(SCC_graph, node_to_scc_map[v], wgt, scc_size_map)
    return mvf


# Calculate MVF for node: x1
print("The MVF of node is : ", calculate_MVF("http://example.org/x1"))
