from DataStructures.Priority_queue import pq_entry as pqe


def new_heap(is_min_heap=True):
    if is_min_heap:
        cmp_function = default_compare_lower_value
    else:
        cmp_function = default_compare_higher_value
    return {
        'elements':{
            'elements': [None],
            'size': 1
        },
        'size': 0,
        'cmp_function': cmp_function
    }

def insert(my_heap, priority, value):

    new_entry = pqe.new_pq_entry(priority, value)
    my_heap['elements']['elements'].append(new_entry)
    my_heap['elements']['size'] += 1
    my_heap['size'] += 1
    swin(my_heap, my_heap['size'])
    return my_heap

def remove(my_heap):
    if is_empty(my_heap):
        return None
    top_entry = my_heap['elements']['elements'][1]
    exchange(my_heap, 1, my_heap['size'])
    my_heap['elements']['elements'].pop()
    my_heap['elements']['size'] -= 1
    my_heap['size'] -= 1
    sink(my_heap, 1)
    return pqe.get_value(top_entry)



def swin(my_heap, pos):
    cmp_function = my_heap['cmp_function']
    while pos > 1:
        father_pos = pos // 2
        father = my_heap['elements']['elements'][father_pos]
        child = my_heap['elements']['elements'][pos]
        if priority(my_heap, father, child):
            break
        exchange(my_heap, pos, father_pos)
        pos = father_pos
    
def sink(my_heap, pos):
    cmp_function = my_heap['cmp_function']
    size = my_heap['size']
    while 2 * pos <= size:
        child_pos = 2 * pos
        if child_pos < size:
            left = my_heap['elements']['elements'][child_pos]
            right = my_heap['elements']['elements'][child_pos + 1]
            if not priority(my_heap, left, right):
                child_pos += 1
        parent = my_heap['elements']['elements'][pos]
        child = my_heap['elements']['elements'][child_pos]
        if priority(my_heap, parent, child):
            break
        exchange(my_heap, pos, child_pos)
        pos = child_pos


def priority(my_heap, parent, child):
    return my_heap["cmp_function"](parent, child)

def exchange(my_heap, pos1, pos2):
    elements = my_heap["elements"]["elements"]
    aux = elements[pos1]
    elements[pos1] = elements[pos2]
    elements[pos2] = aux
    return my_heap

def is_empty(my_heap):
    return size(my_heap) == 0

def size(my_heap):
    return my_heap['size']

def get_first_priority(my_heap):
    if is_empty(my_heap):
        return None
    elemet = pqe.get_priority(my_heap['elements']['elements'][1])
    return elemet

def is_present_value(my_heap, value):
    elemets = my_heap['elements']['elements']
    size = my_heap['elements']['size']
    for i in range(1, size):
        if pqe.get_value(elemets[i]) == value:
            return i
    return -1

def contains(my_heap, value):
    return is_present_value(my_heap, value) != -1

def improve_priority(my_heap, priority, value):
    pos = is_present_value(my_heap, value)
    if pos is -1:
        return None
    entry = my_heap['elements']['elements'][pos]
    pqe.set_priority(entry, priority)
    swin(my_heap, pos)
    return my_heap
    
#fUNCIONES DE COMPARACION
def default_compare_higher_value(father_node, child_node):
    if pqe.get_priority(father_node) >= pqe.get_priority(child_node):
        return True
    return False

def default_compare_lower_value(father_node, child_node):
    if pqe.get_priority(father_node) <= pqe.get_priority(child_node):
        return True
    return False
