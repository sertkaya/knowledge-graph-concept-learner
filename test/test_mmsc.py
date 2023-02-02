from kg_mining import KgMining
from rdflib import URIRef
from utils import powerset
import time

class TestMMSC:
    def test_mmsc(self):
        start_time = time.time()
        # print("Started timing")
        kg = KgMining("test_files/mmsc-example-ricardo-2.ttl")
        # print("Parsed input")

        base_URI = "http://example.org/"
        x0 = URIRef(base_URI + "x0")
        x1 = URIRef(base_URI + "x1")
        x2 = URIRef(base_URI + "x2")
        x3 = URIRef(base_URI + "x3")

        individuals = {x0, x1, x2 }
        depth = 3
        for x in list(map(set, powerset(individuals))):
            print(str(x))
            mmsc = kg.mmsc(x, depth)
            print("mmsc:" + mmsc.to_str())

        end_time = time.time()
        print("Execution time:" + str(end_time - start_time))