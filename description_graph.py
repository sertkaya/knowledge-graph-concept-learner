from rdflib import Graph, URIRef, BNode

rdf_type_URI = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
owl_thing_URI = URIRef("http://www.w3.org/2002/07/owl#thing")


class DescriptionGraph:
    def __init__(self, URI):
        """ creates a graph from a given URI """
        self.g = Graph()
        self.g.parse(URI)

    def node_labels(self, node):
        """ returns the labels of the node """
        return self.g.objects(node, rdf_type_URI)

    def node_mmsc(self, node, depth):
        """ returns the mmsc of a node as a description graph """
        if depth == 0:
            dg = Graph()
            n = node
            for label in self.g.objects(node, rdf_type_URI):
                dg.add((n, rdf_type_URI, label))
            dg.add((n, rdf_type_URI, owl_thing_URI))
            return dg
        # else:
        #     l = set()
        #     for p, o in self.g.predicate_objects(node):
        #         if p != rdf_type_URI:
        #             s = set()
        #             for label in self.node_prime(o, depth - 1):
        #                 s.add(label)
        #             if len(s) != 0:
        #                 fs = frozenset(s)
        #                 l.add((p, fs))
        #     return l


    def unravel_helper(self, node, depth, prefix, tree):
        if depth == 0:
            n_uri = prefix + str(node)
            n = URIRef(n_uri)
            for type in self.g.objects(node, rdf_type_URI):
                tree.add((n, rdf_type_URI, type))
            tree.add((n, rdf_type_URI, owl_thing_URI))
#         else:
#             for p, o in self.g.predicate_objects(node):
#                 if p != rdf_type_URI:
#                     dg = Graph()
#                     for n in self.unravel(o, depth - 1):


    def unravel(self, node, depth):
        """ unravels the graph self.g at node until depth into a tree """
        tree = Graph()
        prefix = ""
        self.unravel_helper(node, depth, prefix, tree)
        return tree

g = DescriptionGraph("example-iccs.ttl")

base_URI = "http://example.org/"
a = URIRef(base_URI + "a")
b = URIRef(base_URI + "b")

for n in g.unravel(a, 0):
    print(n)

# for d in 0,1,2,3:
#     print(d)
#     for a in dg.node_prime(a_URI, d):
#         print(a)
