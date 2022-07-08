from rdflib import Graph, URIRef
from description_tree import DescriptionTree

RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
OWL_THING = URIRef("http://www.w3.org/2002/07/owl#thing")


class DescriptionGraph:
    def __init__(self, URI):
        """ creates a graph from a given URI """
        self.graph = Graph()
        self.graph.parse(URI)

    def unravel(self, node, depth):
        """ Unravels the RDF-Graph at the given node until the given depth. """
        dt = DescriptionTree(self)
        if depth == 0:
            for label in self.graph.objects(node, RDF_TYPE):
                dt.labels.add(label)
            dt.labels.add(OWL_THING)
            return dt
        else:
            for predicate, object in self.graph.predicate_objects(node):
                if predicate == RDF_TYPE:
                    dt.labels.add(object)
                else:
                    dt.edges.setdefault(predicate, set()).add(self.unravel(object, depth - 1))
            dt.labels.add(OWL_THING)
            return dt
