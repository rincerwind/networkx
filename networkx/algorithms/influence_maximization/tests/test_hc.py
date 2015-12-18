#!/usr/bin/env python
from nose.tools import *
import networkx as nx


class TestHC:

    def setUp(self):
        # simple graph
        G = nx.DiGraph()
        G.add_edges_from([(1,2),(3,2),(3,1),(4,2),(3,5),(6,5),(5,6),(7,6),(6,8),(8,6),(7,8),(8,7),(9,6),(10,9),(11,10),(11,12),(13,11)], act_prob=1.0)
        self.G = G

    def test_hc(self):
        print help(nx)
        print nx.hill_climbing(self.G, 2)
        assert_equal(True, True)