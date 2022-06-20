from rdflib import URIRef
import copy

RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
OWL_THING = URIRef("http://www.w3.org/2002/07/owl#thing")
OWL_NOTHING = URIRef("http://www.w3.org/2002/07/owl#nothing")


class DescriptionTree:
    def __init__(self, graph):
        """ Creates an empty description tree from an RDF-Graph. """
        self.graph = graph
        self.labels = set()
        self.edges = {}

    def copy(self):
        c = DescriptionTree(self.graph)
        c.labels = copy.deepcopy(self.labels)
        c.edges = copy.deepcopy(self.edges)
        return c

    def unravel(self, node, depth):
        """ Unravels the RDF-Graph at the given node until the given depth. """
        if depth == 0:
            for label in self.graph.objects(node, RDF_TYPE):
                self.labels.add(label)
            self.labels.add(OWL_THING)
            return self
        else:
            for predicate, object in self.graph.predicate_objects(node):
                if predicate == RDF_TYPE:
                    self.labels.add(object)
                else:
                    child = DescriptionTree(self.graph)
                    self.edges.setdefault(predicate, set()).add(child.unravel(object, depth - 1))
            self.labels.add(OWL_THING)
            return self

    def binary_product(self, t):
        # product tree
        p = DescriptionTree(self.graph)
        p.labels = copy.deepcopy(self.labels)
        p.labels.intersection_update(t.labels)
        for e in self.edges.keys():
            if e in t.edges:
                for c1 in self.edges.get(e):
                    for c2 in t.edges.get(e):
                        p.edges.setdefault(e, set()).add(c1.binary_product(c2))
        return p

    def product(self, trees):
        p = self.copy()
        for t in trees:
            p = p.binary_product(t)
        return p

    def print(self, n, g):
        """ Prints the description graph. """
        for i in range(n):
            print("\t", end="")
        for l in self.labels:
            print(l.n3(g.namespace_manager), end=" ")
        print()
        for edge in self.edges.keys():
            for i in range(n):
                print("\t", end="")
            print(edge.n3(g.namespace_manager))
            for t in self.edges.get(edge):
                t.print(n + 1, g)

    def to_str(self, g):
        s = ""
        len_labels = len(self.labels)
        i = 0
        for l in self.labels:
            if l == OWL_THING:
                s += "⊤"
            elif l == OWL_NOTHING:
                s += "⊥"
            else:
                s += l.n3(g.namespace_manager)
            if i < (len_labels - 1):
                s += " ⊓ "
            i += 1

        keys = self.edges.keys()
        len_keys = len(keys)
        if len_keys != 0 and len_labels != 0:
            s += " ⊓ "
        i = 0
        for edge in keys:
            s += "∃" + edge.n3(g.namespace_manager) + ".("
            for t in self.edges.get(edge):
                s += t.to_str(g)
            s += ")"
            if i < (len_keys - 1):
                s += " ⊓ "
            i += 1
        return s

    def is_homomorphic_to(self, t):
        if len(self.edges) == 0:
            return self.labels.issubset(t.labels)
        else:
            for e in self.edges.keys():
                if e in t.edges:
                    for c1 in self.edges.get(e):
                        child_homomorphic = False
                        for c2 in t.edges.get(e):
                            if c1.is_homomorphic_to(c2):
                                child_homomorphic = True
                                break
                        if not child_homomorphic:
                            return False
                else:
                    return False
            return True

    def is_subsumed_by(self, t):
        return t.is_homomorphic_to(self)

    def is_equivalent_to(self, t):
        return t.is_homomorphic_to(self) and self.is_homomorphic_to(t)
#
# base_URI = "http://example.org/"
# x1 = URIRef(base_URI + "x1")
# x2 = URIRef(base_URI + "x2")
# x3 = URIRef(base_URI + "x3")
# x4 = URIRef(base_URI + "x4")
#
# g = Graph()
# g.parse("test/example-product-11.ttl")
# g.bind("ex", base_URI)
#
# t1 = DescriptionTree(g)
# t1.unravel(x1, 1)
# print("t1:")
# t1.print(0, g)
#
# t2 = DescriptionTree(g)
# t2.unravel(x2, 1)
# print("t2:")
# t2.print(0, g)
#
# t3 = DescriptionTree(g)
# t3.unravel(x3, 1)
# print("t3:")
# t3.print(0, g)
#
# # t4 = DescriptionTree(g)
# # t4.unravel(x4, 1)
# # print("t4:")
# # t4.print(0, g)
#
# # p = t1.product({t2, t3, t4})
# p = t1.product({t2, t3})
#
# print("Product:")
# p.print(0, g)
