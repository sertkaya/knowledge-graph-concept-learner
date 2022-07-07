from description_tree import DescriptionTree
from rdflib import Graph, URIRef
from kg_mining import KgMining
import time

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
kingdom_netherlands = URIRef(base_URI + "Q29999")
czech_republic = URIRef(base_URI + "Q213")
estonia = URIRef(base_URI + "Q191")
latvia = URIRef(base_URI + "Q211")
slovakia = URIRef(base_URI + "Q214")
slovenia = URIRef(base_URI + "Q215")
belgium = URIRef(base_URI + "Q31")
croatia = URIRef(base_URI + "Q224")
cyprus = URIRef(base_URI + "Q229")
malta = URIRef(base_URI + "Q233")
ireland = URIRef(base_URI + "Q27")
hungary = URIRef(base_URI + "Q28")
spain = URIRef(base_URI + "Q29")
luxembourg = URIRef(base_URI + "Q32")
finland = URIRef(base_URI + "Q33")
sweden = URIRef(base_URI + "Q34")
denmark = URIRef(base_URI + "Q34")
romania = URIRef(base_URI + "Q218")
bulgaria = URIRef(base_URI + "Q219")
#
kg = KgMining("test/test-eu-members-rdf.ttl")
print("Parsed input")
depth = 1
start_time = time.time()
print("Started timing")
# fc = kg.build_formal_context({germany, poland, france}, depth)
# fc = kg.build_formal_context({germany, poland, france, kingdom_netherlands}, depth)
fc = kg.build_formal_context({germany, poland, france, kingdom_netherlands, czech_republic }, depth)
# fc = kg.build_formal_context({germany, poland, france, kingdom_netherlands, czech_republic, estonia, latvia, slovakia, slovenia, belgium}, depth)
# fc = kg.build_formal_context({germany, poland, france, kingdom_netherlands, czech_republic, estonia, latvia, slovakia, slovenia, belgium, croatia,
#                              ireland, sweden, finland, denmark, luxembourg}, depth)
# fc = kg.build_formal_context({germany, poland, france, kingdom_netherlands, czech_republic, estonia, latvia, slovakia, slovenia, belgium, croatia,
#                               cyprus, malta, ireland, sweden, finland, denmark, luxembourg, spain, romania, hungary}, depth)
print("Built formal context")
l = fc.lattice
end_time = time.time()
# l = fc.lattice.graphviz(view=True)
print("Number of objects: " + str(len(fc.objects)))
print("Number of attributes:" + str(len(fc.properties)))
# print(fc.properties)
print("Number of concepts: " + str(len(l)))
print("Execution time:" + str(end_time - start_time))
# for extent, intent in l:
#     print(extent)
#     print(intent)
#     print(len(intent))
#     print("=====================================================")
# for c in l:
#    print(c)
