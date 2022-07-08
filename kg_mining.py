from rdflib import URIRef
from description_graph import DescriptionGraph
from description_tree import DescriptionTree
from itertools import chain, combinations
from concepts import Context


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
OWL_THING = URIRef("http://www.w3.org/2002/07/owl#thing")
OWL_NOTHING = URIRef("http://www.w3.org/2002/07/owl#nothing")


class KgMining:
    def __init__(self, URI):
        self.dg = DescriptionGraph(URI)

    def mmsc(self, individuals, depth):
        """ Computes the mmsc of the set of individuals until depth """
        tmp = individuals.copy()
        if len(tmp) == 0:
            # return an empty description tree: bottom
            dt = DescriptionTree(self.dg)
            return dt
        else:
            ind_1 = tmp.pop()
            tree_1 = self.dg.unravel(ind_1, depth)
            trees = set()
            for ind in tmp:
                dt = self.dg.unravel(ind, depth)
                trees.add(dt)
            product_tree = tree_1.product(trees)
            return product_tree

    def compute_attributes(self, individuals, depth):
        """ Returns the set of attributes computed from a set of individuals up to depth."""
        attributes = set()

        # get types of individuals (for N_C)
        tmp = set()
        for x in individuals:
            for cls in self.dg.graph.objects(x, RDF_TYPE):
                tmp.add(cls)
        tmp.add(OWL_THING)
        tmp.add(OWL_NOTHING)

        # add only unique types to attributes
        for cls in tmp:
            dt = DescriptionTree(self.dg)
            dt.labels.add(cls)
            duplicate = False
            # check if attribute a is already added
            for a in attributes:
                if dt.is_equivalent_to(a):
                    duplicate = True
                    break
            if not duplicate:
                attributes.add(dt)

        if depth == 0:
            return attributes

        # get properties (for N_R)
        properties = set()
        for x in individuals:
            for p in self.dg.graph.predicates(x, None):
                properties.add(p)

        # construct attributes with existential and mmsc, add to attributes set
        for xs in list(map(set, powerset(individuals))):
            if len(xs) == 0:
                continue
            for r in properties:
                if r == RDF_TYPE:
                    continue
                # add exists r. mmsc(s) for s subset of X to attributes
                dt = DescriptionTree(self.dg)
                mmsc = self.mmsc(xs, depth - 1)
                dt.edges.setdefault(r, set()).add(mmsc)
                duplicate = False
                for a in attributes:
                    if dt.is_equivalent_to(a):
                        duplicate = True
                        break
                if not duplicate:
                    attributes.add(dt)
        return attributes

    def build_formal_context(self, individuals, depth):
        """ Returns the formal context induced by a set of individuals for a depth."""
        attrs = self.compute_attributes(individuals, depth)
        attributes = ()
        attributes_str = ()
        for m in attrs:
            attributes += (m,)
            attributes_str += (m.to_str(),)
        objects = ()
        incidence = ()
        for g in individuals:
            tg = self.dg.unravel(g, depth)
            gm = ()
            for m in attributes:
                if tg.is_subsumed_by(m):
                    # print(tg.to_str(self.graph) + " ⊑ " + m.to_str(self.graph))
                    gm = gm + (True,)
                else:
                    gm = gm + (False,)
            objects += (g,)
            incidence += (gm,)

        c = Context(objects, attributes_str, incidence)

        return c
