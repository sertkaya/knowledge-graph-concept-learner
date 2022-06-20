from rdflib import Graph, URIRef
from description_tree import DescriptionTree

base_URI = "http://example.org/"
# x1 = URIRef(base_URI + "x1")
# x2 = URIRef(base_URI + "x2")
# x3 = URIRef(base_URI + "x3")
# x4 = URIRef(base_URI + "x4")

a = URIRef(base_URI + "a")
b = URIRef(base_URI + "b")
c = URIRef(base_URI + "c")

g = Graph()
g.parse("test/example-iccs.ttl")
g.bind("ex", base_URI)

depth = 0
t1 = DescriptionTree(g)
t1.unravel(a, depth)
print("t1:")
t1.print(0, g)
print(t1.to_str(g))
