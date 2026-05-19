from DataStructures.Tree import rbt_node as rbt
from DataStructures.List import single_linked_list as sl
import datetime

def new_map():
    return {
        "root": None,
        "type": "RBT",
    }
    
def put(my_rbt, key, value):
    
    if my_rbt is None:
        my_rbt = new_map()
    my_rbt["root"] = insert_node(my_rbt["root"], key, value)
    my_rbt["root"]["color"] = rbt.BLACK
    return my_rbt

def insert_node(root, key, value):
    if root is None:
        return rbt.new_node(key, value)  # nuevo nodo siempre en RED
    
    if key < rbt.get_key(root):
        root["left"] = insert_node(root["left"], key, value)
    elif key > rbt.get_key(root):
        root["right"] = insert_node(root["right"], key, value)
    else:
        root["value"] = value

    if rbt.is_red(root["right"]) and not rbt.is_red(root["left"]):
        root = rotate_left(root)

    left_is_red = rbt.is_red(root["left"])
    left_left_is_red = (root["left"] is not None and 
                        root["left"]["left"] is not None and 
                        rbt.is_red(root["left"]["left"]))
    if left_is_red and left_left_is_red:
        root = rotate_right(root)

    if rbt.is_red(root["left"]) and rbt.is_red(root["right"]):
        flip_colors(root)

    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root
def size(my_tree):
    if my_tree is None:
        return 0
    return size_tree(my_tree["root"])

def size_tree(my_node):
    if my_node is None:
        return 0
    return my_node["size"]


def rotate_left(node_rbt):
    if node_rbt is None or node_rbt["right"] is None:
        return node_rbt

    new_root = node_rbt["right"]
    node_rbt["right"] = new_root["left"]
    new_root["left"] = node_rbt

    new_root["color"] = node_rbt["color"]
    node_rbt["color"] = rbt.RED

    new_root["size"] = node_rbt["size"]
    node_rbt["size"] = 1 + size_tree(node_rbt["left"]) + size_tree(node_rbt["right"])

    return new_root


def rotate_right(node_rbt):
    if node_rbt is None or node_rbt["left"] is None:
        return node_rbt

    new_root = node_rbt["left"]
    node_rbt["left"] = new_root["right"]
    new_root["right"] = node_rbt

    new_root["color"] = node_rbt["color"]
    node_rbt["color"] = rbt.RED

    new_root["size"] = node_rbt["size"]
    node_rbt["size"] = 1 + size_tree(node_rbt["left"]) + size_tree(node_rbt["right"])

    return new_root


#Funcion de comparacion de nodos

def default_compare(key, element):
    """
    Compara key con la llave del elemento (element es un nodo dict).
    Retorna:
      0  si key == element.key
      1  si key > element.key
     -1  si key < element.key
    """
    if element is None:
        return -1
    node_key = rbt.get_key(element)
    if node_key is None:
        return -1
    if key == node_key:
        return 0
    if key > node_key:
        return 1
    return -1
def flip_node_color(node_rbt):
    #Cambia el color del nodo a rojo y el color de sus  hijos
    if rbt.is_red(node_rbt):
        node_rbt["color"] = rbt.BLACK
    else:
        node_rbt["color"] = rbt.RED
def flip_colors(node_rbt):
    #Cambia el color del nodo a rojo y el color de sus  hijos
    flip_node_color(node_rbt)
    if node_rbt["left"] is not None:
        flip_node_color(node_rbt["left"])
    if node_rbt["right"] is not None:
        flip_node_color(node_rbt["right"])
        
def get_node(root, key):
    if root is None:
        return None
    if key < rbt.get_key(root):
        return get_node(root["left"], key)
    elif key > rbt.get_key(root):
        return get_node(root["right"], key)
    else:
        return root
def get(my_rbt, key):
    if my_rbt is None:
        return None
    node = get_node(my_rbt["root"], key)
    if node is not None:
        return rbt.get_value(node)
    else:
        return None
    
def contains(my_rbt, key):
    if my_rbt is None:
        return False
    node = get(my_rbt, key)
    if node is None:
        return False
    return True
def is_empty(my_rbt):
    return size(my_rbt) == 0

def key_set_tree(root, key_list):
    if root is not None:
        key_set_tree(root["left"], key_list)
        sl.add_last(key_list, rbt.get_key(root))
        key_set_tree(root["right"], key_list)
    return key_list
def key_set(my_rbt):
    key_list = sl.new_list()
    if my_rbt is None:
        return key_list
    key_set_tree(my_rbt["root"], key_list)
    return key_list
def value_set_tree(root, value_list):
    if root is not None:    
        value_set_tree(root["left"], value_list)
        sl.add_last(value_list, rbt.get_value(root))
        value_set_tree(root["right"], value_list)
    return value_list
def value_set(my_rbt):
    value_list = sl.new_list()
    if my_rbt is None:
        return value_list
    value_set_tree(my_rbt["root"], value_list)
    return value_list
def left_key_tree(root):
    if root["left"] is None:
        return rbt.get_key(root)
    return left_key_tree(root["left"])
def right_key_tree(root):
    if root["right"] is None:
        return rbt.get_key(root)
    return right_key_tree(root["right"])
    
def get_min_node(root):
    if root is None:
        return None
    return left_key_tree(root)
def get_max_node(root):
    if root is None:
        return None
    return right_key_tree(root)
def get_min(my_rbt):
    if my_rbt is None:
        return None
    return get_min_node(my_rbt["root"])
def get_max(my_rbt):
    if my_rbt is None:
        return None
    return get_max_node(my_rbt["root"])

def height_tree(root):
    if root is None:
        return -1
    else:
        left_hight = height_tree(root["left"])
        right_height = height_tree(root["right"])
        if left_hight > right_height:
            return left_hight + 1
        return right_height + 1
def height(my_rbt):
    if my_rbt is None:
        return 0
    return height_tree(my_rbt["root"]) 

def keys_range(root, key_initial, key_final, key_list):
    if root is not None:
        root_key = rbt.get_key(root)
        if key_initial < root_key:
            keys_range(root["left"], key_initial, key_final, key_list)
        if key_initial <= root_key <= key_final:
            sl.add_last(key_list, rbt.get_key(root))
        if root_key < key_final:
            keys_range(root["right"], key_initial, key_final, key_list)     
    return key_list

def keys(my_rbt, key_initial, key_final):
    key_list = sl.new_list()
    if my_rbt is None:
        return key_list
    keys_range(my_rbt["root"], key_initial, key_final, key_list)
    return key_list

def values_range(root, key_initial, key_final, value_list):
    if root is not None:
        root_key = rbt.get_key(root)
        if key_initial < root_key:
            values_range(root["left"], key_initial, key_final, value_list)
        if key_initial <= root_key <= key_final:
            sl.add_last(value_list, rbt.get_value(root))
        if root_key < key_final:
            values_range(root["right"], key_initial, key_final, value_list)     
    return value_list   
def values(my_rbt, key_initial, key_final):
    value_list = sl.new_list()
    if my_rbt is None:
        return value_list
    values_range(my_rbt["root"], key_initial, key_final, value_list)
    return value_list
 

