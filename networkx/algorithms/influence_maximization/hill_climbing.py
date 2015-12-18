"""
========================================
Hill Climbing for Influence Maximization
========================================

A basic greedy algorithm for influence maximization
"""

import networkx as nx
from collections import deque
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

    num_sim: integer, optional
    	The number of Monte Carlo simulations

    Returns
    -------
    nodes: set of integers
       The seed set as a set of integers

    Examples
    --------
    >>> G = nx.DiGraph()
    >>> G.add_edges_from([(1,2),(3,2),(3,1),(4,2),(3,5),(6,5),(5,6),(7,6),(6,8),(8,6),(7,8),(8,7),(9,6),(10,9),(11,10),(11,12),(13,11)], act_prob=0.6)

    Notes
    -----
    Based on 'Maximizing the spread of influence through a social network'
    by David Kempe, Jon Kleinberg, and Eva Tardos.
"""

def hill_climbing(G, seed_size, model="OIC", inf_sets = None, num_sim = 1000, randomSeed=31101982, resolution=3000000):
	if num_sim is None:
		return

	nNodes = G.number_of_nodes()
	nodes = G.nodes()
	seed_set = set()
	max_inf_set = set()

	for i in range(1, seed_size + 1):

		best_w = None
		best_inf = 0
		for w in nodes:
			if w in seed_set:
				continue

			if model == "OIC" and num_sim > 0:
				w_inf = find_OIC_inf(G, nNodes, seed_set, w, num_sim, randomSeed, resolution)

			elif model == "IC" and num_sim > 0:
				# TO DO
				return
			elif model == "LT" and num_sim > 0:
				# TO DO
				return

			if best_inf < w_inf:
				best_inf = w_inf
				best_w = w

		seed_set.add(best_w)

	return seed_set

# computes the influence of the seed set when w is added to it
def find_OIC_inf(G, nNodes, seed_set, w, l, randomSeed, resolution):
    seedSet = set(seed_set)
    seedSet.add(w)
    covered = [set()] * (l+1)
    visited = set()
    to_visit = deque()

    inf = 0
    for s in seedSet:
        size = 0

        for i in range(1,l+1):
            if s in covered[i]:
                continue

            visited.clear()
            visited.add(s)
            to_visit.clear()
            to_visit.append(s)
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

def ContainsEdge(G, src, dest, inst, nInst, randomSeed, resolution):
    hash_prob = murmurHash3(src, dest, inst, nInst, randomSeed) % resolution
    return hash_prob < G[src][dest]['act_prob']

def murmurHash3(u,v,i,l, randomSeed):
    h = (randomSeed<<16)+l
    
    c1 = 0xcc9e2d51
    c2 = 0x1b873593

    # Hash the first vertex
    k = u
    k = (c1 * k) & 0xFFFFFFFF
    k = ( k << 15 | k >> 17 ) & 0xFFFFFFFF
    k = ( c2 * k ) & 0xFFFFFFFF
    h ^= k
    h = ( h << 13 | h >> 19 ) & 0xFFFFFFFF
    h = ( h * 5 + 0xe6546b64 ) & 0xFFFFFFFF

    # Hash the second vertex
    k = v
    k = (c1 * k) & 0xFFFFFFFF
    k = ( k << 15 | k >> 17 ) & 0xFFFFFFFF
    k = ( c2 * k ) & 0xFFFFFFFF
    h ^= k
    h = ( h << 13 | h >> 19 ) & 0xFFFFFFFF
    h = ( h * 5 + 0xe6546b64 ) & 0xFFFFFFFF

    # Hash the instance
    k = i
    k = (c1 * k) & 0xFFFFFFFF
    k = ( k << 15 | k >> 17 ) & 0xFFFFFFFF
    k = ( c2 * k ) & 0xFFFFFFFF
    h ^= k

    # Mix the results
    h ^= 10
    h ^= (h >> 16)
    h = ( h * 0x85ebca6b ) & 0xFFFFFFFF
    h ^= (h >> 13)
    h = ( h * 0xc2b2ae35 ) & 0xFFFFFFFF
    h ^= (h >> 16)
    
    return h

G = nx.DiGraph()
G.add_edges_from([(1,2),(3,2),(3,1),(4,2),(3,5),(6,5),(5,6),(7,6),(6,8),(8,6),(7,8),(8,7),(9,6),(10,9),(11,10),(11,12),(13,11)], act_prob=1.0)
print hill_climbing(G, 2)