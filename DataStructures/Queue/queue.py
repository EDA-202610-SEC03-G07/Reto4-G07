#from DataStructures.List import single_linked_list as lt
from DataStructures.List import array_list as lt

def new_queue():
    return lt.new_list()

def enqueue(my_list,element):
    return lt.add_last(my_list, element)

def dequeue(my_list):
    return lt.remove_first(my_list)

def is_empty(my_list):
    return lt.is_empty(my_list)

def peek(my_list):
    return lt.first_element(my_list)

def size(my_list):
    return lt.size(my_list)