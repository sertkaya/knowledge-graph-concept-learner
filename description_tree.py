from rdflib import URIRef
import copy

RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
OWL_THING = URIRef("http://www.w3.org/2002/07/owl#thing")
OWL_NOTHING = URIRef("http://www.w3.org/2002/07/owl#nothing")


class DescriptionTree:
    def __init__(self, dg):
        """ Creates an empty description tree from an RDF-Graph. """
        self.dg = dg
        self.labels = set()
        self.edges = {}

    def copy(self):
        """ Creates a copy of this description tree """
        c = DescriptionTree(self.dg)
        c.labels = copy.copy(self.labels)
        c.edges = copy.copy(self.edges)
        return c

#    def unravel(self, node, depth):
#        """ Unravels the RDF-Graph at the given node until the given depth. """
#        if depth == 0:
#            for label in self.graph.objects(node, RDF_TYPE):
#                self.labels.add(label)
#            self.labels.add(OWL_THING)
#            return self
#        else:
#            for predicate, object in self.graph.predicate_objects(node):
#                if predicate == RDF_TYPE:
#                    self.labels.add(object)
#                else:
#                    child = DescriptionTree(self.graph)
#                    self.edges.setdefault(predicate, set()).add(child.unravel(object, depth - 1))
#            self.labels.add(OWL_THING)
#            return self

    def binary_product(self, t):
        """ Returns the product of this tree with tree t"""
        p = DescriptionTree(self.dg)
        p.labels = copy.copy(self.labels)
        p.labels.intersection_update(t.labels)
        for e in self.edges.keys():
            if e in t.edges:
                for c1 in self.edges.get(e):
                    for c2 in t.edges.get(e):
                        p.edges.setdefault(e, set()).add(c1.binary_product(c2))
        return p

    def product(self, trees):
        """ Returns the product of this tree with the trees in the set trees"""
        p = self.copy()
        for t in trees:
            p = p.binary_product(t)
        return p

    def print(self, n):
        """ Pretty prints the description graph. """
        for i in range(n):
            print("\t", end="")
        for label in self.labels:
            print(label.n3(self.dg.graph.namespace_manager), end=" ")
        print()
        for edge in self.edges.keys():
            for i in range(n):
                print("\t", end="")
            print(edge.n3(self.dg.graph.namespace_manager))
            for t in self.edges.get(edge):
                t.print(n + 1)

    def to_str(self):
        """ Returns a string representation in the Description Logics notation"""
        string = ""
        len_labels = len(self.labels)
        i = 0
        for label in self.labels:
            if label == OWL_THING:
                string += "⊤"
            elif label == OWL_NOTHING:
                string += "⊥"
            else:
                string += label.n3(self.dg.graph.namespace_manager)
            # just to avoid trailing ⊓
            if i < (len_labels - 1):
                string += " ⊓ "
            i += 1

        keys = self.edges.keys()
        len_keys = len(keys)
        if len_keys != 0 and len_labels != 0:
            string += " ⊓ "
        i = 0
        for edge in keys:
            string += "∃" + edge.n3(self.dg.graph.namespace_manager) + ".("
            for t in self.edges.get(edge):
                string += t.to_str()
            string += ")"
            if i < (len_keys - 1):
                string += " ⊓ "
            i += 1
        return string

    def is_homomorphic_to(self, t):
        """ Checks if this tree is homomorphic to tree t"""
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
        """ Checks if the concept description represented by this tree
        is subsumed by the concept description represented by tree t"""
        return t.is_homomorphic_to(self)

    def is_equivalent_to(self, t):
        """ Checks if the concept description represented by this tree
        is equivalent to the concept description represented by tree t"""
        return t.is_homomorphic_to(self) and self.is_homomorphic_to(t)
