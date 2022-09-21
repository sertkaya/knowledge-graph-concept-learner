from rdflib import Graph, URIRef
from description_graph import DescriptionGraph

base_URI = "http://example.org/"
# x1 = URIRef(base_URI + "x1")
# x2 = URIRef(base_URI + "x2")
# x3 = URIRef(base_URI + "x3")
# x4 = URIRef(base_URI + "x4")

a = URIRef(base_URI + "a")
b = URIRef(base_URI + "b")
c = URIRef(base_URI + "c")

dg = DescriptionGraph("test_files/unravel-test-0.ttl")
depth = 3
dt = dg.unravel(a, depth)
# print("dt:")
# dt.print(0)
print(dt.to_str())