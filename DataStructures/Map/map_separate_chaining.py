from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sl
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf

def new_map(num_elements, load_factor=4, prime=109345121):
    capacity = mf.next_prime(num_elements/load_factor)
    new_map = {"prime": prime,
                "capacity": capacity,
                "scale": 1,
                "shift": 0,
                "table": table(capacity),
                "current_factor": 0,
                "limit_factor": load_factor,
                "size": 0
                }
    return new_map
def table(n):
    table = al.new_list()
    for i in range(n):
        sl_list = sl.new_list()
        al.add_last(table, sl_list)
    return table

def default_compare(key, element):

   if (key == me.get_key(element)):
      return 0
   elif (key > me.get_key(element)):
      return 1
   return -1

def put(my_map, key, value):
   hash_value = mf.hash_value(my_map, key)
   sl_list = al.get_element(my_map["table"], hash_value)
   pos = sl.is_present(sl_list, key, default_compare)
   if pos != -1:
      me.set_value(sl.get_element(sl_list, pos), value)
   else:
      sl.add_last(sl_list, me.new_map_entry(key, value))
      my_map["size"] += 1
   my_map["current_factor"] = size(my_map)/my_map["capacity"]
   if my_map["current_factor"] > my_map["limit_factor"]:
      rehash(my_map)

def size(my_map):
   return my_map["size"]

def rehash(my_map):
    old_table = my_map["table"]
    new_capacity = mf.next_prime(2*my_map["capacity"])
    my_map["capacity"] = new_capacity
    my_map["table"] = table(new_capacity)
    my_map["size"] = 0
    for i in range(al.size(old_table)):
        entry = al.get_element(old_table, i)
        sl_list = entry
        act = sl_list["first"]
        while act is not None:
           put(my_map, me.get_key(act["info"]), me.get_value(act["info"]))
           act = act["next"]
    return my_map

def contains(my_map, key):
   hash_value = mf.hash_value(my_map, key)
   sl_list = al.get_element(my_map["table"], hash_value)
   pos = sl.is_present(sl_list, key, default_compare)
   if pos != -1:
        return True
   return False

def remove(my_map, key):
   hash_value = mf.hash_value(my_map, key)
   sl_list = al.get_element(my_map["table"], hash_value)
   pos = sl.is_present(sl_list, key, default_compare)
   if pos != -1:
      sl.delete_element(sl_list, pos)
      my_map["size"] -= 1
      return True
   return False
def get(my_map, key):
   hash_value = mf.hash_value(my_map, key)
   sl_list = al.get_element(my_map["table"], hash_value)
   pos = sl.is_present(sl_list, key, default_compare)
   if pos != -1:
      return me.get_value(sl.get_element(sl_list, pos))
   return None

def is_empty(my_map):
   return size(my_map) == 0

def key_set(my_map):
    keys = al.new_list()
    for i in range(al.size(my_map["table"])):
        sl_list = al.get_element(my_map["table"], i)
        act = sl_list["first"]
        while act is not None:
            al.add_last(keys, me.get_key(act["info"]))
            act = act["next"]
    return keys

def value_set(my_map):
    values = al.new_list()
    for i in range(al.size(my_map["table"])):   
        sl_list = al.get_element(my_map["table"], i)
        act = sl_list["first"]
        while act is not None:
            al.add_last(values, me.get_value(act["info"]))
            act = act["next"]
    return values