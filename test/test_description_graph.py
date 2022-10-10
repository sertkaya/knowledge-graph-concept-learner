from rdflib import Graph, URIRef
from description_graph import DescriptionGraph

class TestDescriptionGraph:

    def test_unravel(self):
        base_URI = "http://example.org/"
        a = URIRef(base_URI + "a")
        b = URIRef(base_URI + "b")
        c = URIRef(base_URI + "c")

        dg = DescriptionGraph("test_files/unravel-test-0.ttl")
        depth = 1
        dt = dg.unravel(a, depth)
        print(dt.to_str())
        assert True
