from rdflib import Graph, URIRef

RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
OWL_THING = URIRef("http://www.w3.org/2002/07/owl#thing")


class DescriptionTree:
    def __init__(self, graph):
        """ Creates an empty description tree from an RDF-Graph. """
        self.graph = graph
        self.labels = set()
        self.edges = set()

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

    def product(self, tree1, trees_rest, depth):
        if depth == 0:
            p = DescriptionTree(self.graph)
            p.unravel(tree1, 0)
            for tree in trees_rest:
                tmp = DescriptionTree(self.graph)
                tmp.unravel(tree, 0)
                p.labels.intersection_update(tmp.labels)
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
a = URIRef(base_URI + "a")
b = URIRef(base_URI + "b")

g = Graph()
g.parse("unravel-test-felix.ttl")
tree = DescriptionTree(g)
tree.unravel(a, 5)
tree.print(0)
