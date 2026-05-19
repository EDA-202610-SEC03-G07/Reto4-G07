from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import digraph as dg
from DataStructures.Queue import queue as q
from DataStructures.Stack import stack as st

def bfs(my_graph, source):
    order = dg.order(my_graph)
    visited_map = mp.new_map(order)
    mp.put(visited_map, source, {"marked": True, "edge_from": None, "dist_to": 0})
    bfs_vertex(my_graph, source, visited_map)
    return visited_map

def bfs_vertex(my_graph, source, visited_map):
    pass

