from DataStructures.Tree import bst_node as bst
from DataStructures.List import single_linked_list as sl
import datetime


def normalize_to_date(key):
    """
    Normaliza 'key' a datetime.date:
    - si key es str con formato 'YYYY-MM-DD' -> parsea y retorna date
    - si key es datetime.datetime -> retorna key.date()
    - si key es datetime.date -> retorna key
    - si key es None -> retorna None
    """
    if key is None:
        return None
    t = type(key)
    if t is str:
        return datetime.datetime.strptime(key, "%Y-%m-%d").date()
    if t is datetime.datetime:
        return key.date()
    if t is datetime.date:
        return key
    return key


def new_map():

    map = {"root":None}

    return map


def put(my_bst, key, value):
    
    if my_bst is None:
        my_bst = new_map()
    my_bst["root"] = insert_node(my_bst.get("root"), key, value)
    return my_bst

def insert_node(root, key, value):
    if root is None:
        root= bst.new_node(key, value)
    else:
        if key < bst.get_key(root): #caso 1 - el key es menor que la llave del root , por lo tanto para la izquierda
            root["left"] = insert_node(root["left"], key, value)
        elif key > bst.get_key(root): #caso 2 - el key es mayor que la llave del root, por lo tanto para la derecha
            root["right"] = insert_node(root["right"], key, value)
        else:
            root["value"] = value
        root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root

def get(my_bst, key):
    """
    Máscara: normaliza la clave a datetime.date si viene como str
    y luego invoca la recursiva get_node.
    """
    if my_bst is None:
        return None

    # Normalizar la llave que viene de la vista (acepta str "YYYY-MM-DD")
    norm_key = normalize_to_date(key)

    node = get_node(my_bst["root"], norm_key)
    if node is None:
        return None
    return bst.get_value(node)


def get_node(root, key):
    if root is None:
        return None
    
    node_key = bst.get_key(root)
    if key < node_key:
        return get_node(root["left"], key)
    elif key > node_key:
        return get_node(root["right"], key)
    else:
        return root

def size(my_bst):
    if my_bst is None:
        return 0    
    return size_tree(my_bst["root"])

def size_tree(my_node):
    if my_node is None:
        return 0
    else:
        return 1+size_tree(my_node["left"])+size_tree(my_node["right"])
    
def contains(my_bst,key):
    """
    Máscara: True si el árbol contiene la key.
    """
    return get(my_bst,key) is not None

def is_empty(my_bst):
    """
    Máscara: True si la tabla está vacía.
    """
    return size(my_bst) == 0
    
def key_set(my_bst):
    """
    Máscara: retorna una single_linked_list con todas las keys en orden.
    """
    lst = sl.new_list()
    if my_bst is None:
        return lst
    root = my_bst["root"]
    keys = key_set_tree(root)

    i = 0
    while i < len(keys):
        sl.add_last(lst, keys[i])
        i += 1
    return lst


def key_set_tree(root):
    """
    Recursiva: retorna lista Python con keys en orden.
    """
    result = []
    if root is None:
        return result
    left = key_set_tree(root["left"])
    i = 0
    while i < len(left):
        result.append(left[i])
        i += 1
    result.append(bst.get_key(root))
    right = key_set_tree(root["right"])
    j = 0
    while j < len(right):
        result.append(right[j])
        j += 1
    return result

def value_set(my_bst):
    """
    Máscara: retorna una single_linked_list con todos los values en orden.
    """
    lst = sl.new_list()
    if my_bst is None:
        return lst
    root = my_bst["root"]
    vals = value_set_tree(root)
    i = 0
    while i < len(vals):
        sl.add_last(lst, vals[i])
        i += 1
    return lst

def value_set_tree(root):
    """
    Recursiva: retorna lista Python con values en orden.
    """
    result = []
    if root is None:
        return result
    left = value_set_tree(root["left"])
    i = 0
    while i < len(left):
        result.append(left[i])
        i += 1
    result.append(bst.get_value(root))
    right = value_set_tree(root["right"])
    j = 0
    while j < len(right):
        result.append(right[j])
        j += 1
    return result

def get_min(my_bst):
    """
    Máscara: retorna la key mínima o None si vacía.
    """
    if my_bst is None:
        return None
    node = get_min_node(my_bst["root"])
    if node is None:
        return None
    return bst.get_key(node)


def get_max(my_bst):
    """
    Máscara: retorna la key máxima o None si vacía.
    """
    if my_bst is None:
        return None
    node = get_max_node(my_bst["root"])
    if node is None:
        return None
    return bst.get_key(node)


def get_min_node(root):
    """
    Recursiva/iterativa: retorna el nodo con la mínima key en subárbol root.
    """
    if root is None:
        return None
    current = root
    while current["left"] is not None:
        current = current["left"]
    return current


def get_max_node(root):
    """
    Recursiva/iterativa: retorna el nodo con la máxima key en subárbol root.
    """
    if root is None:
        return None
    current = root
    while current["right"] is not None:
        current = current["right"]
    return current

def delete_min(my_bst):
    """
    Máscara: elimina la mínima y retorna el BST actualizado.
    """
    if my_bst is None:
        return None
    my_bst["root"] = delete_min_tree(my_bst["root"])
    return my_bst

def delete_max(my_bst):
    """
    Máscara: elimina la máxima y retorna el BST actualizado.
    """
    if my_bst is None:
        return None
    my_bst["root"] = delete_max_tree(my_bst["root"])
    return my_bst

def delete_min_tree(root):
    """
    Recursiva: elimina el mínimo en subárbol root y retorna la nueva raíz.
    """
    if root is None:
        return None
    if root["left"] is None:
        return root["right"]
    root["left"] = delete_min_tree(root["left"])
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root


def delete_max_tree(root):
    """
    Recursiva: elimina el máximo en subárbol root y retorna la nueva raíz.
    """
    if root is None:
        return None
    if root["right"] is None:
        return root["left"]
    root["right"] = delete_max_tree(root["right"])
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root
 
def height(my_bst):
    """
    Máscara: retorna la altura del árbol (nodos en el camino más largo).
    Si el árbol está vacío retorna 0.
    """
    if my_bst is None:
        return 0
    return height_tree(my_bst["root"])

def height_tree(root):
    """
    Recursiva: retorna la altura del subárbol (número de nodos en el camino más largo).
    Si root es None retorna 0.
    """
    if root is None:
        return 0
    left_h = height_tree(root["left"])
    right_h = height_tree(root["right"])
    if left_h > right_h:
        return 1 + left_h
    return 1 + right_h

def keys(my_bst, key_initial, key_final):
    """
    Máscara: retorna keys en [key_initial, key_final] como single_linked_list.
    Normaliza inputs (acepta str "YYYY-MM-DD", datetime.date, datetime.datetime).
    """
    # convertir parámetros a datetime.date si vienen como str
    key_lo = normalize_to_date(key_initial)
    key_hi = normalize_to_date(key_final)

    lst = sl.new_list()
    if my_bst is None:
        return lst
    root = my_bst["root"]
    collector = []
    keys_range(root, key_lo, key_hi, collector)
    i = 0
    while i < len(collector):
        sl.add_last(lst, collector[i])
        i += 1
    return lst

def keys_range(root, key_lo, key_hi, collector):
    """
    Recursiva: añade a collector las keys en [key_lo, key_hi] en orden.
    collector es una lista Python mutable pasada por referencia.
    """
    if root is None:
        return
    root_key = bst.get_key(root)
    if root_key is None:
        return
    if root_key > key_lo:
        keys_range(root["left"], key_lo, key_hi, collector)
    if key_lo <= root_key <= key_hi:
        collector.append(root_key)
    if root_key < key_hi:
        keys_range(root["right"], key_lo, key_hi, collector)

def values(my_bst, key_initial, key_final):
    """
    Máscara: retorna values correspondientes a keys en [key_initial, key_final] como single_linked_list.
    Normaliza inputs (acepta str "YYYY-MM-DD", datetime.date, datetime.datetime).
    """
    key_lo = normalize_to_date(key_initial)
    key_hi = normalize_to_date(key_final)

    lst = sl.new_list()
    if my_bst is None:
        return lst
    root = my_bst["root"]
    collector = []
    values_range(root, key_lo, key_hi, collector)
    i = 0
    while i < len(collector):
        sl.add_last(lst, collector[i])
        i += 1
    return lst

def values_range(root, key_lo, key_hi, collector):
    """
    Recursiva: añade a collector los values cuyas keys están en [key_lo, key_hi].
    """
    if root is None:
        return
    root_key = bst.get_key(root)
    if root_key is None:
        return
    if root_key > key_lo:
        values_range(root["left"], key_lo, key_hi, collector)
    if key_lo <= root_key <= key_hi:
        collector.append(bst.get_value(root))
    if root_key < key_hi:
        values_range(root["right"], key_lo, key_hi, collector)

def remove(my_bst,key):

    if my_bst is None:
        return None
    my_bst["root"] = remove_node(my_bst["root"], key)
    return my_bst

def remove_node(root,key):

    if root is None:
        return None
    
    if key < bst.get_key(root):
        root["left"] = remove_node(root["left"], key)
    elif key > bst.get_key(root):
        root["right"] = remove_node(root["right"], key)
    else:
        # Nodo encontrado
        if root["right"] is None:
            return root["left"]
        if root["left"] is None:
            return root["right"]
        
         # Nodo con dos hijos
        temp = root
        root = min_node(temp["right"])
        root["right"] = delete_min_tree(temp["right"])
        root["left"] = temp["left"]

    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root

def min_node(root):
    while root["left"] is not None:
        root = root["left"]
    return root

def floor(my_bst, key):
    """
    Máscara: retorna la llave que es piso de 'key' (mayor o igual más cercana por debajo).
    """
    if my_bst is None:
        return None
    return floor_key(my_bst["root"], key)


def ceiling(my_bst, key):
    """
    Máscara: retorna la llave techo de 'key' (menor o igual más cercana por encima).
    """
    if my_bst is None:
        return None
    return ceiling_key(my_bst["root"], key)


def select(my_bst, pos):
    """
    Máscara: retorna la llave en la posición pos (0-indexed) o None.
    """
    if my_bst is None:
        return None
    root = my_bst["root"]
    return select_key(root, pos)


def rank(my_bst, key):
    """
    Máscara: retorna el número de keys estrictamente menores que key.
    """
    if my_bst is None:
        return 0
    return rank_keys(my_bst["root"], key)

def floor_key(root, key):
    """
    Recursiva: retorna la mayor key <= key, o None si no existe.
    """
    if root is None:
        return None
    root_key = bst.get_key(root)
    if root_key is None:
        return None
    if root_key == key:
        return root_key
    if root_key > key:
        return floor_key(root["left"], key)
    # root_key < key
    right_floor = floor_key(root["right"], key)
    if right_floor is not None:
        return right_floor
    return root_key


def ceiling_key(root, key):
    """
    Recursiva: retorna la menor key >= key, o None si no existe.
    """
    if root is None:
        return None
    root_key = bst.get_key(root)
    if root_key is None:
        return None
    if root_key == key:
        return root_key
    if root_key < key:
        return ceiling_key(root["right"], key)
    # root_key > key
    left_ceil = ceiling_key(root["left"], key)
    if left_ceil is not None:
        return left_ceil
    return root_key


def select_key(root, pos):
    """
    Recursiva: retorna la key en la posición pos (0-indexed) usando tamaños almacenados.
    """
    if root is None:
        return None
    left_size = size_tree(root["left"])
    if pos < left_size:
        return select_key(root["left"], pos)
    if pos == left_size:
        return bst.get_key(root)
    return select_key(root["right"], pos - left_size - 1)


def rank_keys(root, key):
    """
    Recursiva: retorna el número de keys estrictamente menores que key.
    """
    if root is None:
        return 0
    root_key = bst.get_key(root)
    if root_key is None:
        return 0
    if key < root_key:
        return rank_keys(root["left"], key)
    elif key == root_key:
        return size_tree(root["left"])
    else:
        # key > root_key
        return 1 + size_tree(root["left"]) + rank_keys(root["right"], key)

# -------------------- Comparador --------------------

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
    node_key = bst.get_key(element)
    if node_key is None:
        return -1
    if key == node_key:
        return 0
    if key > node_key:
        return 1
    return -1