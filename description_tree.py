from rdflib import Graph, URIRef
import copy

RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
OWL_THING = URIRef("http://www.w3.org/2002/07/owl#thing")


class DescriptionTree:
    def __init__(self, graph):
        """ Creates an empty description tree from an RDF-Graph. """
        self.graph = graph
        self.labels = set()
        self.edges = set()

    def copy(self):
        c = DescriptionTree(self.graph)
        c.labels = copy.deepcopy(self.labels)
        c.edges = copy.deepcopy(self.edges)
        return(c)

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
                    # tree.edges.setdefault(predicate, set()).add(g.unravel(object, depth - 1))
                    child = DescriptionTree(self.graph)
                    self.edges.add((predicate, child.unravel(object, depth - 1)))
            self.labels.add(OWL_THING)
            return self

    def product(self, trees, depth):
        if depth == 0:
            p = self.copy()
            for tree in trees:
               p.labels.intersection_update(tree.labels)
            return(p)


    def print(self,n):
        """ Prints the description graph. """
        for i in range(n):
            print("\t", end="")
        print(self.labels)
        for edge, t in self.edges:
            for i in range(n):
                print("\t", end="")
            print(edge)
            t.print(n+1)


base_URI = "http://example.org/"
x1 = URIRef(base_URI + "x1")
x2 = URIRef(base_URI + "x2")

g = Graph()
g.parse("test/example-product-0.ttl")

t1 = DescriptionTree(g)
t1.unravel(x1, 0)

t2 = DescriptionTree(g)
t2.unravel(x2, 0)

p = t1.product({t2}, 0)

for t in p.labels:
    print(t)