#!/usr/bin/env python
from nose.tools import *
import networkx as nx


class TestHC:

    def setUp(self):
        # simple graph
        G = nx.DiGraph()
        G.add_edges_from([(1,2),(3,2),(3,1),(4,2),(3,5),(6,5),(5,6),(7,6),(6,8),(8,6),(7,8),(8,7),(9,6),(10,9),(11,10),(11,12),(13,11)], num_sim = 1, act_prob=1.0)
        self.G = G

    def test_hc(self):
        assert_equal(nx.hill_climbing(self.G, 2), set([13,3]))

    def test_hc(self):
        G = nx.DiGraph()
        G.add_edges_from([(1,2),(3,2),(3,1),(4,2),(3,5),(6,5),(5,6),(7,6),(6,8),(8,6),(7,8),(8,7),(9,6),(10,9),(11,10),(11,12),(13,11)], num_sim = 100, act_prob=0.1)
        assert_equal(nx.hill_climbing(G, 2), set([13,3]))