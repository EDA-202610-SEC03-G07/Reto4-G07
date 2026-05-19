
def new_list():
    newlist ={
        "elements": [],
        "size": 0,
    }
    return newlist

def get_element(my_list, index):
    return my_list["elements"][index]

def is_present(my_list, element, comparation_function):
    
    size = my_list["size"]
    if size> 0:
        keyexist= False 
        for keypos in range (0, size):
            info= my_list["elements"][keypos]
            if comparation_function(element,info)== 0:
                keyexist=True
                break
        if keyexist:
            return keypos
    return -1

def add_first(lista, element):
    elementos = lista["elements"]
    elementos.insert(0, element)
    
    lista["size"] += 1
    
    return lista

def add_last(lista, element):
    
    lista["elements"].append(element)
    lista["size"] += 1
    
    return lista 
       
def size(lista):
    
    return lista["size"]

def first_element(lista):
    
    if lista["size"]>0:
        return lista["elements"][0]
    else:
        return None
    
def is_empty(lista):
    
    if lista["size"]==0:
        return True
    else:
        return False
    
def remove_first(lista):
    if lista["size"]>0:
        remove=lista["elements"][0]
        lista["elements"]=lista["elements"][1:]
        lista["size"]-= 1
        return remove

def remove_last(lista):
    if lista["size"]>0:
        remove= lista["elements"][-1]
        lista["elements"]= lista["elements"][:-1]
        lista["size"]-= 1
        return remove
    
def insert_element(lista,pos, element):
    lista["elements"].insert(pos,element)
    lista["size"]+= 1
    return lista

def delete_element(lista,pos):
    
    lista["elements"]=lista["elements"][:pos] + lista["elements"][pos+1:]
    
    lista["size"]-=1
    return lista

def change_info(lista,pos,new_info):
    lista["elements"][pos]= new_info
    return lista["elements"]

def exchange (lista,pos_1,pos_2):
    intercambio= lista["elements"][pos_1],lista["elements"][pos_2]= lista["elements"][pos_2],lista["elements"][pos_1]
    return intercambio

def sub_list(lista, pos_i, num_elements):
    result = {"size": 0, "elements": []}
    for i in range (pos_i, pos_i + num_elements):
        if i < lista["size"]:
            result["elements"].append(lista["elements"][i])
            result["size"] += 1
    return result

#FUNCIONES DE ORDENAMIENTO ARRAY LIST
def default_sort_criteria(element1, element2):
    is_sorted = False
    if element1 < element2:
        is_sorted = True
    return is_sorted

def selection_sort(lista, sort_criteria):
    tamaño = size(lista)
    for i in range(tamaño):
        minimo = i
        for j in range(i + 1, tamaño):
            if sort_criteria(lista["elements"][j], lista["elements"][minimo]) < 0:
                minimo = j
        if minimo != i:
            exchange(lista, i, minimo)
    return lista

def insertion_sort(my_list, sort_crit):
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

def shell_sort(my_list,sort_crit):
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
    if n > 1:
        mid = (n // 2)
        #se divide la lista original en dos partes
        left_list = sub_list(my_list, 0, mid)
        right_list = sub_list(my_list, mid, n - mid)

        #se hace el llamado recursivo con la lista izquierda y derecha 
        merge_sort(left_list, sort_crit)
        merge_sort(right_list, sort_crit)

        #i recorre la lista izquierda, j la derecha y k la lista original
        i = j = k = 0

        left_elements = size(left_list)
        righ_telements = size(right_list)

        while (i < left_elements) and (j < righ_telements):
            elem_i = get_element(left_list, i)
            elem_j = get_element(right_list, j)
            # compara y ordena los elementos
            if sort_crit(elem_j, elem_i):   # caso estricto elem_j < elem_i
                change_info(my_list, k, elem_j)
                j += 1
            else:                            # caso elem_i <= elem_j
                change_info(my_list, k, elem_i)
                i += 1
            k += 1

        # Agrega los elementos que no se comprararon y estan ordenados
        while i < left_elements:
            change_info(my_list, k, get_element(left_list, i))
            i += 1
            k += 1

        while j < righ_telements:
            change_info(my_list, k, get_element(right_list, j))
            j += 1
            k += 1
    return my_list

def quick_sort(my_list, sort_crit):
    
    quick_sort_recursive(my_list, 0, size(my_list)-1, sort_crit)
    return my_list

def quick_sort_recursive(my_list, lo, hi, sort_crit):
    if (lo >= hi):
        return
    pivot = partition(my_list, lo, hi, sort_crit)
    quick_sort_recursive(my_list, lo, pivot-1, sort_crit)
    quick_sort_recursive(my_list, pivot+1, hi, sort_crit)

def partition(my_list, lo, hi, sort_crit):
    follower = leader = lo
    while leader < hi:
        if sort_crit(
           get_element(my_list, leader), get_element(my_list, hi)):
           exchange(my_list, follower, leader)
           follower += 1
        leader += 1
    exchange(my_list, follower, hi)
    return follower