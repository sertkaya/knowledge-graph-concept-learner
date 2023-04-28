from rdflib import URIRef

from description_graph import DescriptionGraph

class TestDescriptionTree:
    from rdflib import URIRef

    global base_URI
    base_URI = "http://example.org/"

    def test_description_tree(self):
        a = URIRef(base_URI + "a")
        b = URIRef(base_URI + "b")
        c = URIRef(base_URI + "c")
        dg = DescriptionGraph("test_files/unravel-test-4.ttl")
        depth = 1
        dt = dg.unravel(a, depth)
        print("dt:" + dt.to_str())
        print("labels:" + str(dt.labels))
        print("edges:" + str(dt.edges))
        dt.print(0)

    def test_binary_product(self):
        dg = DescriptionGraph("test_files/example-product-5.ttl")
        x1 = URIRef(base_URI + "x1")
        x2 = URIRef(base_URI + "x2")
        depth = 2
        dt1= dg.unravel(x1, depth)
        dt2= dg.unravel(x2, depth)
        p = dt1.binary_product(dt2)
        print(p.to_str())
