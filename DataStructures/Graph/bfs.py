from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import digraph as dg
from DataStructures.Queue import queue as q
from DataStructures.Stack import stack as st
from DataStructures.Graph import edge as edg
from DataStructures.Graph import dijsktra_structure as ds
from DataStructures.Priority_queue import priority_queue as pq

# BFS

def bfs(my_graph, source):
    order = dg.order(my_graph)
    visited_map = mp.new_map(order)

    if not dg.contains_vertex(my_graph, source):
        return visited_map

    mp.put(visited_map, source, {
        "edge_from": None,
        "dist_to": 0
    })

    bfs_vertex(my_graph, source, visited_map)

    return visited_map


def bfs_vertex(my_graph, source, visited_map):
    queue = q.new_queue()
    q.enqueue(queue, source)

    while not q.is_empty(queue):
        current = q.dequeue(queue)

        current_info = mp.get(visited_map, current)
        current_dist = current_info["dist_to"]

        adjacent_keys = dg.adjacents(my_graph, current)

        for key_v in adjacent_keys:
            if mp.get(visited_map, key_v) is None:
                mp.put(visited_map, key_v, {
                    "edge_from": current,
                    "dist_to": current_dist + 1
                })

                q.enqueue(queue, key_v)

    return visited_map


def has_path_to(key_v, visited_map):
    if mp.get(visited_map, key_v) is not None:
        return True
    return False


def path_to(key_v, visited_map):
    if not has_path_to(key_v, visited_map):
        return None

    path = st.new_stack()
    current = key_v

    while current is not None:
        st.push(path, current)
        info = mp.get(visited_map, current)
        current = info["edge_from"]

    return path

# DIJKSTRA

def dijkstra(my_graph, source):
    order = dg.order(my_graph)
    aux_structure = ds.new_dijsktra_structure(source, order)

    visited_map = aux_structure["visited"]
    priority_queue = aux_structure["pq"]

    vertices = dg.vertices(my_graph)

    for key_v in vertices["elements"]:
        mp.put(visited_map, key_v, {
            "marked": False,
            "edge_from": None,
            "dist_to": float("inf")
        })

    if not dg.contains_vertex(my_graph, source):
        return aux_structure

    mp.put(visited_map, source, {
        "marked": True,
        "edge_from": None,
        "dist_to": 0
    })

    pq.insert(priority_queue, 0, source)

    while not pq.is_empty(priority_queue):
        current = pq.remove(priority_queue)

        current_info = mp.get(visited_map, current)
        current_dist = current_info["dist_to"]

        edges = dg.edge_vertex(my_graph, current)

        for edge in edges:
            key_v = edg.to(edge)
            weight = edg.weight(edge)

            vertex_info = mp.get(visited_map, key_v)
            new_dist = current_dist + weight

            if new_dist < vertex_info["dist_to"]:
                mp.put(visited_map, key_v, {
                    "marked": True,
                    "edge_from": current,
                    "dist_to": new_dist
                })

                if pq.contains(priority_queue, key_v):
                    pq.improve_priority(priority_queue, new_dist, key_v)
                else:
                    pq.insert(priority_queue, new_dist, key_v)

    return aux_structure


def dist_to(key_v, aux_structure):
    visited_map = aux_structure["visited"]
    info = mp.get(visited_map, key_v)

    if info is None:
        return float("inf")

    return info["dist_to"]


def has_path_to_dijkstra(key_v, aux_structure):
    visited_map = aux_structure["visited"]
    info = mp.get(visited_map, key_v)

    if info is not None and info["marked"] == True:
        return True

    return False


def path_to_dijkstra(key_v, aux_structure):
    if not has_path_to_dijkstra(key_v, aux_structure):
        return None

    visited_map = aux_structure["visited"]
    path = st.new_stack()
    current = key_v

    while current is not None:
        st.push(path, current)
        info = mp.get(visited_map, current)
        current = info["edge_from"]

    return path