def new_list():
    newlist = {
        "first": None,
        "last": None,
        "size" : 0,
    }
    
    return newlist

def get_element(my_list,pos):
    searchpos= 0
    node= my_list["first"]
    while searchpos< pos:
        node= node["next"]
        searchpos+= 1
    return node["info"]

def is_present(my_list, element, cmp_function ):
    is_in_array= False
    temp= my_list["first"]
    count= 0 
    while not is_in_array and temp != None:
        if cmp_function(element, temp["info"])== 0:
            is_in_array=True
        else:
            temp = temp["next"]
            count += 1
    if not is_in_array:
        count= -1
    return count 

def size(my_list):
    
     return my_list['size']
 
def add_first(my_list, element):
    new_node = {"info": element, "next": None}

    if my_list["size"] == 0:
        
        my_list["first"] = new_node
        my_list["last"] = new_node
    else:
        
        new_node["next"] = my_list["first"]
        
        my_list["first"] = new_node

    my_list["size"] += 1

    return my_list

def add_last(my_list, element):
    new_node = {"info": element, "next": None}
    
    if my_list['size'] == 0:
        my_list['first'] = new_node
        my_list['last'] = new_node
    else:
        my_list['last']['next'] = new_node
        my_list['last'] = new_node
    
    my_list['size'] += 1
    return my_list

def first_element(my_list):
    if my_list["size"] == 0:
        return None
    return my_list['first']['info']

def size(my_list):
    
     return my_list['size']

def is_empty(my_list):
    if my_list["size"]==0:
        return True
    else:
        return False
    
def last_element(my_list):
    if my_list["size"]==0:
        return None
    else:
        return my_list["last"]

def delete_element(my_list,pos):
    if pos < 0 or pos >= my_list['size']:
        return None
    
    if pos == 0:
        my_list['first'] = my_list['first']['next']
        if my_list['size'] == 1:
            my_list['last'] = None
    else:
        current = my_list['first']
        i = 0
        while i < pos - 1:
            current = current['next']
            i += 1
        current['next'] = current['next']['next']
        if pos == my_list['size'] - 1:
            my_list['last'] = current
    
    my_list['size'] -= 1
    return my_list

def remove_first(my_list):
    info_primero_eliminado=my_list["first"]["info"]
    if my_list["size"]==0:
        return None
    elif my_list["size"]==1:
        my_list["first"]=None
        my_list["last"]=None
        
    else:
        primero=my_list["first"]
        my_list["first"]=primero["next"]
    my_list["size"]-=1
    return info_primero_eliminado

def remove_last(my_list):
    info_ultimo_eliminado=my_list["last"]["info"]
    if my_list["size"]==0:
        return None
    elif my_list["size"]==1:
        my_list["first"]=None
        my_list["last"]=None
    elif my_list["size"]==2:
        my_list["last"]=my_list["first"]
    else:
        current = my_list['first']
        while current['next'] != my_list['last']:
            current = current['next']
        current['next'] = None
        my_list['last'] = current
    
    my_list['size'] -= 1
    return info_ultimo_eliminado

def insert_element(my_list, pos, element):
    if pos < 0:
        return None

    if pos == 0:
        
        return add_first(my_list, element)

    if pos >= my_list['size']:
        return add_last(my_list, element)

    new_node = {"info": element, "next": None}
    current = my_list['first']
    i = 0

    while i < pos - 1:
        current = current['next']
        i += 1

    new_node['next'] = current['next']
    current['next'] = new_node
    my_list['size'] += 1

    return my_list
 
def change_info(my_list, pos, new_info):
    if pos < 0 or pos >= my_list['size']:
        return None
    
    current = my_list['first']
    i = 0
    while i < pos:
        current = current['next']
        i += 1
    
    current['info'] = new_info
    return my_list

    
def exchange(my_list, pos_1, pos_2):
    size = my_list["size"]

    if pos_1 < 0 or pos_2 < 0 or pos_1 >= size or pos_2 >= size:
        return None
    if pos_1 == pos_2:
        return my_list
    
    actual = my_list["first"]
    contador = 0
    nodo_1 = None
    nodo_2 = None

    while actual != None:
        if contador == pos_1:
            nodo_1 = actual
        if contador == pos_2:
            nodo_2 = actual
        actual = actual["next"]
        contador += 1

    aux = nodo_1["info"]
    nodo_1["info"] = nodo_2["info"]
    nodo_2["info"] = aux

    return my_list
    
def sub_list(my_list, pos, num_elements):
    if pos < 0 or pos >= size(my_list):
        return None
    
    sub = new_list()
    current = my_list['first']
    
    for i in range(pos):
        current = current['next']
    
    count = 0
    while current is not None and count < num_elements:
        add_last(sub, current["info"])
        current = current['next']
        count += 1
    
    return sub   

def info(node):
    if node== None:
        return None
    else:
        return node["info"]

def default_function(elemen_1, element_2):

   if elemen_1 > element_2:
      return 1
   elif elemen_1 < element_2:
      return -1
   return 0

#ALGORITMOS DE ORDENAMIENTO
def default_sort_criteria(elemento1,elemento2):
    is_sorted = False
    if elemento1 < elemento2:
        is_sorted = True
    return is_sorted

def selection_sort(my_list, sort_crit):
    if size(my_list) <= 1:
        return my_list
    if size(my_list) > 1:
        n = size(my_list)
        pos1 = 0
        while pos1 < n:
            pos2 = pos1
            while (pos2 > 0) and (sort_crit(get_element(my_list, pos2), get_element(my_list, pos2-1))):
                exchange(my_list, pos2, pos2-1)
                pos2 -= 1
            pos1 += 1
    return my_list

def insertion_sort(my_list, sort_crit):
    if size(my_list) > 1:
        n = size(my_list)
        pos1 = 0
        while pos1 < n:
            pos2 = pos1
            while (pos2 > 0) and (sort_crit(
                get_element(my_list, pos2), get_element(my_list, pos2-1))):
                node_prev = my_list["first"]
                p = 0
                while p < pos2 - 1:
                    node_prev = node_prev["next"]
                    p += 1
                node_act = node_prev["next"]               
                aux = node_prev["info"]
                node_prev["info"] = node_act["info"]
                node_act["info"] = aux
                pos2 -= 1
            pos1 += 1
    return my_list

def shell_sort(my_list, sort_crit):
    if size(my_list) > 1:
        n = size(my_list)
        h = 1
        while h < n//3:   # primer gap. La lista se h-ordena con este tamaño
            h = 3*h + 1
        while (h >= 1):
            for i in range(h, n):
                j = i
                while (j >= h) and sort_crit(
                                    get_element(my_list, j),
                                    get_element(my_list, j-h)):
                    exchange(my_list, j, j-h)
                    j -= h
            h //= 3    # h se decrementa en un tercio
    return my_list

def merge_sort(my_list, sort_crit):
    n = size(my_list)
    if n <= 1:
        return my_list
    else:
        mid = (n // 2)
        left_list = sub_list(my_list, 0, mid)
        right_list = sub_list(my_list, mid, n - mid)

        merge_sort(left_list, sort_crit)
        merge_sort(right_list, sort_crit)

        curr_left = left_list["first"]
        curr_right = right_list["first"]
        
        dest_node = my_list["first"]

        while curr_left is not None and curr_right is not None:
            if sort_crit(curr_right['info'], curr_left['info']):
                dest_node["info"] = curr_right["info"]
                curr_right = curr_right["next"]
            else:
               dest_node["info"] = curr_left["info"]
               curr_left = curr_left["next"]
            dest_node = dest_node["next"]

        while curr_left is not None:
            dest_node["info"] = curr_left["info"]
            curr_left = curr_left["next"]
            dest_node = dest_node["next"]

        while curr_right is not None:
            dest_node["info"] = curr_right["info"]
            curr_right = curr_right["next"]
            dest_node = dest_node["next"]

    return my_list

def quick_sort(my_list, sort_crit):
    if not is_empty(my_list):
        quick_sort_recursive(my_list,0, size(my_list)-1, sort_crit )
    return my_list

def quick_sort_recursive(my_list, low, high, sort_crit):
    if low>=high:
        return 
    pivoit_index = partition(my_list,low,high, sort_crit)
    quick_sort_recursive(my_list, low, pivoit_index-1, sort_crit)
    quick_sort_recursive(my_list, pivoit_index+1, high, sort_crit)
    
def partition(my_list, low, high, sort_crit):
    node_low = my_list["first"]
    pos_actual = 0
    while pos_actual < low:
        node_low = node_low["next"]
        pos_actual += 1
        
    node_high = node_low
    while pos_actual < high:
        node_high = node_high["next"]
        pos_actual += 1

    pivot = node_high["info"]
    follower_node = node_low
    leader_node = node_low
    follower = leader = low
    
    while leader < high:
        if sort_crit(leader_node["info"], pivot):
            aux = follower_node["info"]
            follower_node["info"] = leader_node["info"]
            leader_node["info"] = aux
            
            follower_node = follower_node["next"]
            follower += 1
            
        leader_node = leader_node["next"]
        leader += 1
    
    aux = follower_node["info"]
    follower_node["info"] = node_high["info"]
    node_high["info"] = aux
    
    return follower
    
    