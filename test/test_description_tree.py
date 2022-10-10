from description_graph import DescriptionGraph

class TestDescriptionTree:
    from rdflib import URIRef

    base_URI = "http://example.org/"

    global a, b, c, dg
    a = URIRef(base_URI + "a")
    b = URIRef(base_URI + "b")
    c = URIRef(base_URI + "c")
    dg = DescriptionGraph("test_files/unravel-test-4.ttl")

    def test_description_tree(self):
        depth = 1
        dt = dg.unravel(a, depth)
        print("dt:" + dt.to_str())
        print("labels:" + str(dt.labels))
        print("edges:" + str(dt.edges))
        dt.print(0)