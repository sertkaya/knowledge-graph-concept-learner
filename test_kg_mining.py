from description_tree import DescriptionTree
from rdflib import Graph, URIRef
from kg_mining import KgMining

base_URI = "http://example.org/"
a = URIRef(base_URI + "a")
b = URIRef(base_URI + "b")
c = URIRef(base_URI + "c")
d = URIRef(base_URI + "d")
e = URIRef(base_URI + "e")

kg = KgMining("test/example-iccs.ttl")
depth = 2
M = kg.compute_attributes({a, b, c, d, e}, depth)
print("---Attributes---" + str(len(M)))
for m in M:
    # m.print(0, kg.graph)
    print(m.to_str(kg.graph))
