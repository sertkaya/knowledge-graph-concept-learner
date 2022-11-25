from description_tree import DescriptionTree
from rdflib import Graph, URIRef
from kg_mining import KgMining
import time

class TestKgMining:
    base_URI = "http://www.wikidata.org/entity/"
    global germany, poland, france, kingdom_netherlands, czech_republic, estonia, latvia, slovakia, slovenia, belgium, croatia, cyprus, malta, ireland, hungary, spain
    global luxembourg, finland, sweden, denmark, romania, bulgaria

    germany = URIRef(base_URI + "Q183")
    poland = URIRef(base_URI + "Q36")
    france = URIRef(base_URI + "Q142")
    kingdom_netherlands = URIRef(base_URI + "Q29999")
    czech_republic = URIRef(base_URI + "Q213")
    estonia = URIRef(base_URI + "Q191")
    latvia = URIRef(base_URI + "Q211")
    slovakia = URIRef(base_URI + "Q214")
    slovenia = URIRef(base_URI + "Q215")
    belgium = URIRef(base_URI + "Q31")
    croatia = URIRef(base_URI + "Q224")
    cyprus = URIRef(base_URI + "Q229")
    malta = URIRef(base_URI + "Q233")
    ireland = URIRef(base_URI + "Q27")
    hungary = URIRef(base_URI + "Q28")
    spain = URIRef(base_URI + "Q29")
    luxembourg = URIRef(base_URI + "Q32")
    finland = URIRef(base_URI + "Q33")
    sweden = URIRef(base_URI + "Q34")
    denmark = URIRef(base_URI + "Q34")
    romania = URIRef(base_URI + "Q218")
    bulgaria = URIRef(base_URI + "Q219")
#
    def test_kg_mining(self):
        kg = KgMining("test_files/test-eu-members-rdf.ttl")
        print("Parsed input")
        depth = 2
        start_time = time.time()
        print("Started timing")
        # 3
        # fc = kg.build_formal_context({germany, poland, france}, depth)
        # 4
        # fc = kg.build_formal_context({germany, poland, france, kingdom_netherlands}, depth)
        # 5
        # fc = kg.build_formal_context({germany, poland, france, kingdom_netherlands, czech_republic }, depth)
        # 6
        # fc = kg.build_formal_context({germany, poland, france, kingdom_netherlands, czech_republic, estonia}, depth)
        # 7
        # fc = kg.build_formal_context({germany, poland, france, kingdom_netherlands, czech_republic, estonia, latvia}, depth)
        # 10
        # fc = kg.build_formal_context({germany, poland, france, kingdom_netherlands, czech_republic, estonia, latvia, slovakia, slovenia, belgium}, depth)
        # 15
        # fc = kg.build_formal_context({germany, poland, france, kingdom_netherlands, czech_republic, estonia, latvia, slovakia, slovenia, belgium, croatia,
        #                              ireland, sweden, finland, denmark, luxembourg}, depth)
        # 20
        fc = kg.build_formal_context({germany, poland, france, kingdom_netherlands, czech_republic, estonia, latvia, slovakia, slovenia, belgium, croatia,
                                      cyprus, malta, ireland, sweden, finland, denmark, luxembourg, spain, romania, hungary}, depth)
        # print("Built formal context")
        l = fc.lattice
        end_time = time.time()
        # l = fc.lattice.graphviz(view=True)
        print("Number of objects: " + str(len(fc.objects)))
        print("Number of attributes:" + str(len(fc.properties)))
        # print(fc.properties)
        print("Number of concepts: " + str(len(l)))
        print("Execution time:" + str(end_time - start_time))
        # for extent, intent in l:
        #     print(extent)
        #     print(intent)
        #     print(len(intent))
        #     print("=====================================================")
        for c in l:
            print(c)
            print("=====================================================")


    def test_kg_mining_example_paper(self):
        base_URI = "http://example.org/"
        a = URIRef(base_URI + "a")
        b = URIRef(base_URI + "b")
        c = URIRef(base_URI + "c")
        d = URIRef(base_URI + "d")
        e = URIRef(base_URI + "e")

        kg = KgMining("test_files/example-paper.ttl")
        print("Parsed input")
        depth = 1
        # start_time = time.time()
        # print("Started timing")
        # 3
        fc = kg.build_formal_context({a, b, c, d, e}, depth)
        l = fc.lattice
        # end_time = time.time()
        # l = fc.lattice.graphviz(view=True)
        print("Number of objects: " + str(len(fc.objects)))
        print("Number of attributes:" + str(len(fc.properties)))
        print("Attributes:" + str(fc.properties))
        # print("Attributes")
        # for p in fc.properties:
        #     print("p:" + p)
        print("Number of concepts: " + str(len(l)))
        # print("Execution time:" + str(end_time - start_time))
        # for extent, intent in l:
        #     print(extent)
        #     print(intent)
        #     print(len(intent))
        #     print("=====================================================")
        for c in l:
            print(c)
            print("=====================================================")


    def test_kg_mining_unravel_test_3(self):
        base_URI = "http://example.org/"
        a = URIRef(base_URI + "a")
        b = URIRef(base_URI + "b")

        kg = KgMining("test_files/unravel-test-3.ttl")
        print("Parsed input")
        depth = 0
        # start_time = time.time()
        # print("Started timing")
        # 3
        fc = kg.build_formal_context({a, b}, depth)
        l = fc.lattice
        # end_time = time.time()
        # l = fc.lattice.graphviz(view=True)
        print("Number of objects: " + str(len(fc.objects)))
        print("Number of attributes:" + str(len(fc.properties)))
        print("Attributes:" + str(fc.properties))
        # print("Attributes")
        # for p in fc.properties:
        #     print("p:" + p)
        print("Number of concepts: " + str(len(l)))
        # print("Execution time:" + str(end_time - start_time))
        # for extent, intent in l:
        #     print(extent)
        #     print(intent)
        #     print(len(intent))
        #     print("=====================================================")
        for c in l:
            print(c)
            print("=====================================================")