from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import vertex as v
def new_graph(order):
    new_graph = {"vertices": mp.new_map(order),
                 "num_edges": 0}
    return new_graph

def insert_vertex(my_graph, key_u, info_u):
    new_vertex = v.new_vertex(key_u, info_u)
    new_vertex["adjacents"] = mp.new_map(1)
    mp.put(my_graph["vertices"], key_u, new_vertex)
    return my_graph


def add_edge(my_graph, key_u, key_v, weight=1):
    vertex_u = mp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise Exception("El vertice u no existe")
    vertex_v = mp.get(my_graph["vertices"], key_v)
    if vertex_v is None:
        raise Exception("El vertice v no existe")
    existing_edge = mp.get(vertex_u["adjacents"], key_v)
    if existing_edge is not None:
        return my_graph
    my_graph["num_edges"] += 1
    v.add_adjacent(vertex_u, key_v, weight)
    return my_graph

def contains_vertex(my_graph, key_u):
    vertex_u = mp.get(my_graph["vertices"], key_u)
    if vertex_u is not None:
        return True
    return False

def order(my_graph):
    size = mp.size(my_graph["vertices"])
    return size

def size(my_graph):
    size = my_graph["num_edges"]
    return size

def degree(my_graph, key_u):
    vertex_u = mp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise Exception("El vertice u no existe")
    degree =  v.degree(vertex_u)
    return degree

def adjacents(my_graph, key_u):
    vertex_u = mp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise Exception("El vertice u no existe")
    adjacents_map =  v.get_adjacents(vertex_u)
    adjacents_list = mp.key_set(adjacents_map)
    return adjacents_list["elements"]

def vertices(my_graph):
    vertices_map = my_graph["vertices"]
    vertices_list = mp.key_set(vertices_map)
    return vertices_list

def edge_vertex(my_graph, key_u):
    vertex_u = mp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise Exception("El vertice u no existe")
    edge_vertex_map = v.get_adjacents(vertex_u)
    edge_vertex_list = mp.value_set(edge_vertex_map)
    return edge_vertex_list["elements"]

def get_vertex(my_graph, key_u):
    vertex_u = mp.get(my_graph["vertices"], key_u)
    if vertex_u is not None:
        return vertex_u
    return None

def update_vertex_info(my_graph, key_u, new_info):
    vertex_u = mp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        return my_graph
    v.set_value(vertex_u, new_info)
    return my_graph

def get_vertex_info(my_graph, key_u):
    vertex_u = mp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise Exception("El vertice u no existe")
    info = v.get_value(vertex_u)
    return info

