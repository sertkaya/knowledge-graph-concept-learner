import unittest
import tempfile

import networkx as nx
from rdflib import Graph, Namespace, URIRef


class TestMVF(unittest.TestCase):

    def test_calculate_MVF(self):
        # Create a temporary turtle file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ttl') as tf:
            tf.write(b'''
            @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
            @prefix ex: <http://example.org/> .

            ex:x1 rdf:type ex:F .
            ex:x1 rdf:type ex:M .
            ex:x1 ex:r1 ex:y1 .
            ex:x1 ex:r2 ex:z1 .
            ex:y1 rdf:type ex:A .
            ex:z1 rdf:type ex:B .

            ex:x2 rdf:type ex:F .
            ex:x2 rdf:type ex:M .
            ex:x2 ex:r1 ex:y2 .
            ex:x2 ex:r2 ex:z2 .
            ex:y2 rdf:type ex:C .
            ex:z2 rdf:type ex:D .
            ''')
            tf.flush()

            # Calculate MVF for node: x1
            result = calculate_MVF("http://example.org/x1", tf.name)

            # Assert the result for node: x1
            self.assertEqual(result, 2)

            # Delete the temporary file
            # os.unlink(tf.name)


def calculate_MVF(v, ttl_file):
    # Read .ttl file and create a directed graph
    g = Graph()
    g.parse(ttl_file, format="turtle")

    # Create directed graph
    DG = nx.DiGraph()

    ex = Namespace("http://example.org/")
    rdf_type = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")

    for s, p, o in g:
        if p != rdf_type:
            DG.add_edge(str(s), str(o))

    def maxWeight(G, V, wgt, size):
        current = 0
        for W in [U for U in G if (V, U) in G.edges()]:
            if wgt[W] is None:
                current = max(current, maxWeight(G, W, wgt, size))
            else:
                current = max(current, wgt[W])
        wgt[V] = current + size[V]
        return wgt[V]

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


# Run the test
if __name__ == '__main__':
    unittest.main()
