from rdflib import Graph, URIRef
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
    def __init__(self, file):
        self.graph = Graph()
        self.graph.parse(file)

    def mmsc(self, X, d):
        tmp = X.copy()
        if len(tmp) == 0:
            # return an empty description tree: bottom
            t = DescriptionTree(self.graph)
            return t
        else:
            t1 = DescriptionTree(self.graph)
            x1 = tmp.pop()
            t1.unravel(x1, d)
            s = set()
            for x in tmp:
                t = DescriptionTree(self.graph)
                t.unravel(x, d)
                s.add(t)
            p = t1.product(s)
            return p

    def compute_attributes(self, X, d):
        attributes = set()
        # for x in X:
        #     t = DescriptionTree(self.graph)
        #     # unravel to depth 0, i.e., get only the labels
        #     # the set of labels of x in X is the N_C
        #     t.unravel(x, 0)
        #     attributes.add(t)

        # get types (for N_C)
        tmp = set()
        for x in X:
            for c in self.graph.objects(x, RDF_TYPE):
                tmp.add(c)
        tmp.add(OWL_THING)
        tmp.add(OWL_NOTHING)

        for c in tmp:
            t = DescriptionTree(self.graph)
            t.labels.add(c)
            duplicate = False
            for a in attributes:
                if t.is_equivalent_to(a):
                    duplicate = True
                    break
            if not duplicate:
                attributes.add(t)

        if d == 0:
            return attributes

        # get properties (for N_R)
        properties = set()
        for x in X:
            for p in self.graph.predicates(x, None):
                properties.add(p)

        for xs in list(map(set, powerset(X))):
            if len(xs) == 0:
                continue
            for r in properties:
                if r == RDF_TYPE:
                    continue
                # add exists r. mmsc(s) for s subset of X to attributes
                t = DescriptionTree(self.graph)
                mmsc = self.mmsc(xs, d - 1)
                # print(str(xs) + ":" + r + ":" + mmsc.to_str(self.graph))
                # t.edges[r] = {mmsc}
                t.edges.setdefault(r, set()).add(mmsc)
                duplicate = False
                for a in attributes:
                    if t.is_equivalent_to(a):
                        duplicate = True
                        break
                if not duplicate:
                    attributes.add(t)
        return attributes

    def build_formal_context(self, X, d):
        M = self.compute_attributes(X, d)
        I = []
        # for g in X:
        #     t = DescriptionTree(g)
        #     t.unravel(g, d)
        #     for m in M:

        c = Context(X, M, I)
        return c

# fc = kg.build_formal_context({a, b, c}, 1)
# print("Objects:")
# print(fc.objects)
# print("Attributes:")
# print(fc.properties)

# c = kg.mmsc({a,b}, d)
# print("mmsc:")
# c.print(d, kg.graph)
