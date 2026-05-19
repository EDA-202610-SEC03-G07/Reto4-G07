#from DataStructures.List import single_linked_list as lt
from DataStructures.List import array_list as lt
def new_stack():
    stack = {
        'size': 0,
        'elements': lt.new_list(),
    }
    return stack

def push(stack, element):
    lt.add_first(stack["elements"], element)
    stack['size'] += 1
    return stack

def pop(stack): 
    if stack['size'] > 0:
        element = lt.first_element(stack['elements'])  
        lt.remove_first(stack['elements'])
        stack['size'] -= 1
        return element 
    else:
        return None
   
def is_empty(stack):
    empty=None
    if stack["size"]==0:
        empty=True
    else:
        empty=False
    return empty
   
def top(stack):
    top=None
    if stack['size'] > 0:
        top= lt.first_element(stack['elements'])
    else:
        return None
    return top
   
def size(stack):
    return stack['size']