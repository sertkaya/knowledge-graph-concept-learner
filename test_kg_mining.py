from description_tree import DescriptionTree
from rdflib import Graph, URIRef
from kg_mining import KgMining
#
# base_URI = "http://example.org/"
# a = URIRef(base_URI + "a")
# b = URIRef(base_URI + "b")
# c = URIRef(base_URI + "c")
# d = URIRef(base_URI + "d")
# e = URIRef(base_URI + "e")
#
# kg = KgMining("test/example-ekaw.ttl")
# depth = 2
# # M = kg.compute_attributes({a, b, c, d, e}, depth)
# # print("---Attributes---" + str(len(M)))
# # for m in M:
# #     # m.print(0, kg.graph)
# #     print(m.to_str(kg.graph))
#
# fc = kg.build_formal_context({a, b, c, d, e}, depth)
# l = fc.lattice.graphviz(view=True)
# # l = fc.lattice

base_URI = "http://www.wikidata.org/entity/"
germany = URIRef(base_URI + "Q183")
poland = URIRef(base_URI + "Q36")
france = URIRef(base_URI + "Q142")
#
kg = KgMining("test/test-eu-members-rdf.ttl")
depth = 2
fc = kg.build_formal_context({germany, poland, france}, depth)
l = fc.lattice
# l = fc.lattice.graphviz(view=True)
print(len(fc.objects))
print(len(fc.properties))
print(fc.properties)
print(len(l))

# for c in l:
#    print(c)
