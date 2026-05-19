from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import digraph as dg
from DataStructures.Graph import vertex as v
from DataStructures.Stack import stack as st
from DataStructures.Graph import digraph as dg
def dfs(my_graph, source):
    order = dg.order(my_graph)
    visited_map = mp.new_map(order)
    mp.put(visited_map, source, {"marked": True, "edge_from": None})
    dfs_vertex(my_graph, source, visited_map)  
    return visited_map

def dfs_vertex(my_graph, vertex, visited_map):
    adjacent_keys = dg.adjacents(my_graph, vertex)  
    for key_v in adjacent_keys:
        if mp.get(visited_map, key_v) is None:
            mp.put(visited_map, key_v, {"marked": True, "edge_from": vertex})
            dfs_vertex(my_graph, key_v, visited_map)
    
    return visited_map

def has_path_to(key_v, visited_map):
    if mp.get(visited_map, key_v) is not None:
        return True
    return False


def path_to(key_v, visited_map):
    if not has_path_to(key_v, visited_map):
        return None

    stack = st.new_stack()
    current = key_v
    while current is not None:
        st.push(stack, current)
        info = mp.get(visited_map, current)
        current = info["edge_from"]
    return stack
