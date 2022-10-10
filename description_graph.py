from rdflib import Graph, URIRef
from description_tree import DescriptionTree

RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
OWL_THING = URIRef("http://www.w3.org/2002/07/owl#thing")


class DescriptionGraph:
    def __init__(self, URI):
        """ creates a graph from a given URI """
        self.graph = Graph()
        self.graph.parse(URI)
        # default description tree for owl:thing
        # default_labels = {OWL_THING}
        # self.dt_owl_thing = DescriptionTree(default_labels, {})
        # self.dt_owl_thing = DescriptionTree(self)
        # self.dt_owl_thing.labels.add(OWL_THING)

    def unravel(self, node, depth):
        """ Unravels the RDF-Graph at the given node until the given depth. """
        # dt = DescriptionTree(self)
        if depth == 0:
            labels = set()
            edges = {}
            for object in self.graph.objects(node, RDF_TYPE, unique=True):
                # dt.labels.add(label)
                labels.add(object)
            # dt.labels.add(OWL_THING)
            # return dt
            labels.add(OWL_THING)
            # print("node:" + node)
            # print("labels:" + str(labels))
            return DescriptionTree(self, labels,edges)
            # if dt.is_equivalent_to(self.dt_owl_thing):
            #     return self.dt_owl_thing
            # else:
            #     return dt
            # if (len(dt.labels) == 1):
            #     return self.dt_owl_thing
            # else:
            #     return dt
        else:
            labels = set()
            labels.add(OWL_THING)
            edges = {}
            for predicate, object in self.graph.predicate_objects(node, unique=True):
                if predicate == RDF_TYPE:
                    # dt.labels.add(object)
                    labels.add(object)
                else:
                    # dt.edges.setdefault(predicate, set()).add(self.unravel(object, depth - 1))
                    edges.setdefault(predicate, set()).add(self.unravel(object, depth - 1))
                    # print("predicate:" + predicate)
                    # print("edges:" + str(edges))
                    # c = self.unravel(object, depth - 1)
                    # if c.is_equivalent_to(self.dt_owl_thing):
                    #     dt.edges.setdefault(predicate, set()).add(self.dt_owl_thing)
                    # else:
                    #     dt.edges.setdefault(predicate, set()).add(c)
            # dt.labels.add(OWL_THING)
            # return dt
            return DescriptionTree(self, labels,edges)
