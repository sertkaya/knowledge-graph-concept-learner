from rdflib import URIRef
import copy
from line_profiler_pycharm import profile
import math
from functools import total_ordering

RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
OWL_THING = URIRef("http://www.w3.org/2002/07/owl#thing")
OWL_NOTHING = URIRef("http://www.w3.org/2002/07/owl#nothing")


@total_ordering
class DescriptionTree:
    # dictionary of description trees
    # keys are sorted labels, values are description trees
    dts = {}

    def __new__(cls, dg, labels, edges):
        key = DescriptionTree.compute_key(cls, labels, edges)
        if key in DescriptionTree.dts:
            dt = DescriptionTree.dts.get(key)
            return dt
        else:
            self = object.__new__(cls)
            DescriptionTree.dts[key] = self
            return self

    def __init__(self, dg, labels, edges):
        """ Creates or gets a description tree with the given labels. """
        self.dg = dg
        self.labels = labels
        self.edges = edges

    def __lt__(self, other):
        return id(self) < id(other)

    def compute_key(self, labels, edges):
        key = ""
        for l in sorted(labels):
            key += hex(id(l)) + "_"
        for edge in sorted(edges.keys()):
            key += hex(id(edge)) + "("
            for c in sorted(edges.get(edge)):
                key += self.compute_key(self, c.labels, c.edges)
            key += ")"
        return key

    def copy(self):
        """ Creates a copy of this description tree """
        labels = copy.copy(self.labels)
        edges = copy.copy(self.edges)
        c = DescriptionTree(self.dg, labels, edges)
        return c

    def binary_product(self, t):
        """ Returns the product of this tree with tree t"""
        labels = copy.copy(self.labels)
        labels.intersection_update(t.labels)
        edges = {}
        for e in self.edges.keys():
            if e in t.edges:
                for c1 in self.edges.get(e):
                    for c2 in t.edges.get(e):
                        edges.setdefault(e, set()).add(c1.binary_product(c2))
        return DescriptionTree(self.dg, labels, edges)

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
            print(label.n3(self.dg.graph.namespace_manager), end=", ")
        for edge in self.edges.keys():
            for i in range(n):
                print("\t", end="")
            for t in self.edges.get(edge):
                print(edge.n3(self.dg.graph.namespace_manager) + ".(", end="")
                t.print(n)
                print(")", end=", ")

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

        edges = self.edges.keys()
        len_edges = len(edges)
        if len_edges != 0 and len_labels != 0:
            string += " ⊓ "
        i = 0
        for edge in edges:
            # print("edge:" + str(edge))
            children = self.edges.get(edge)
            len_children = len(children)
            j = 0
            for c in children:
                string += "∃" + edge.n3(self.dg.graph.namespace_manager) + ".("
                # print("c:" + str(c))
                string += c.to_str()
                string += ")"
                # just to avoid trailing ⊓
                if j < (len_children - 1):
                    string += " ⊓ "
                j += 1
            # just to avoid trailing ⊓
            if i < (len_edges - 1):
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
