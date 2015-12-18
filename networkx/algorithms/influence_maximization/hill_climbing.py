"""
========================================
Hill Climbing for Influence Maximization
========================================

A basic greedy algorithm for influence maximization
"""


from collections import deque
from murmur3 import *

import networkx as nx
import copy
import random


__author__ = """\n""".join(['Toni Andreev <rincerwind@gmail.com>'])
__all__ = ['hill_climbing']

"""
	Generates a seed set of nodes that gives the highest
	approximate maximum influence in the network.

    Parameters
    ----------
    G : NetworkX graph

    seed_size : integer
       The number of nodes to be included into the seed set

    model : string, optional
       The type of model to be used during the influence maximization
       The types are:
       		- Independent Cascade (IC)
       		- Linear Threshold (LT)
       		- Online Independent Cascade (OIC) (Default)

    inf_sets: list of lists of integers, optional
        When given an IC or LT model, the user should also provide the influence sets of each vertex

    num_sim: integer, optional
    	The number of Monte Carlo simulations

    randomSeed: unsigned 32bit integer, optional
        Used with a uniform hash function to yield a probability of an edge existing in a propagation instance

    resolution: unsigned 32bit integer, optional
        Brings the result of the hash function to a range of values

    Returns
    -------
    nodes: set of integers
       The seed set as a set of integers

    Examples
    --------
    >>> G = nx.DiGraph()
    >>> G.add_edges_from([(1,2),(3,2),(3,1),(4,2),(3,5),(6,5),(5,6),(7,6),(6,8),(8,6),(7,8),(8,7),(9,6),(10,9),(11,10),(11,12),(13,11)], act_prob=1.0)

    Notes
    -----
    Based on 'Maximizing the spread of influence through a social network'
    by David Kempe, Jon Kleinberg, and Eva Tardos.
"""

# returns a seed set of size 'seed_size' that maximizes the influence in the network
def hill_climbing(G, seed_size, model="OIC", inf_sets = None, num_sim = 1000, randomSeed=31101982, resolution=3000000):
    if num_sim is None:
        return None

    if num_sim < 1:
        return None

    nNodes = G.number_of_nodes()
    seed_set = set()
    max_inf_set = set()

    if nNodes < 1:
        return None

    for i in range(1, seed_size + 1):
        best_w = None
        best_inf = 0
        nodes = G.nodes()
        for w in nodes:
            if w in seed_set:
                continue

            if model == "OIC":
                w_inf = find_OIC_inf(G, nNodes, seed_set, w, num_sim, randomSeed, resolution)

            elif model == "IC":
                # TO DO
                # w_inf = func
                return
            else:
                # LT model
                # TO DO
                # w_inf = func
                return

            if best_inf < w_inf:
                best_inf = w_inf
                best_w = w

        seed_set.add(best_w)

    return seed_set

# computes the influence of the seed set when w is added to it
def find_OIC_inf(G, nNodes, seed_set, w, l, randomSeed, resolution):
    seedSet = copy.deepcopy(seed_set)
    seedSet.add(w)

    covered = [set()] * (l+1)   # covered per propagation instance
    visited = set()             # visited in current propagation instance
    to_visit = deque()

    inf = 0
    for s in seedSet:
        size = 0

        for i in range(1,l+1):  # iterate over propagation instances
            if s in covered[i]:
                continue

            visited.clear()
            visited.add(s)
            to_visit.clear()
            to_visit.append(s)
            # BFS from s
            while len(to_visit) > 0:
                u = to_visit.popleft()
                covered[i].add(u)
                size += 1

                u_neighbours = G[u]
                for v, meta in u_neighbours.items():
                    if ContainsEdge(G, u, v, i, l, randomSeed, resolution) and (v not in covered[i]) and (v not in visited):
                        visited.add(v)
                        to_visit.append(v)
        inf += float(size)/l
    return inf

# checks whether 'src->dest' exists in instance 'inst' when there are 'nInst' instances
def ContainsEdge(G, src, dest, inst, nInst, randomSeed, resolution):
    hash_prob = murmurHash3(src, dest, inst, nInst, randomSeed) % resolution
    return hash_prob < resolution * G[src][dest]['act_prob']