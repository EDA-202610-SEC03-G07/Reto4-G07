from DataStructures.List import array_list as al
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
def new_map(num_elements, load_factor=0.5, prime=109345121):
   c = num_elements/load_factor
   capacity = mf.next_prime(c)
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


def table(num_elements):
   table = al.new_list()
   for i in range(num_elements):
      element=me.new_map_entry(None, None)
      al.add_last(table, element)
   return table

def put(my_map, key, value):
   hash_value = mf.hash_value(my_map, key)
   pos = find_slot(my_map, key, hash_value)
   if pos[0]:
      me.set_value(al.get_element(my_map["table"], pos[1]),value)
   else:
      al.change_info(my_map["table"], pos[1], me.new_map_entry(key, value))
      my_map["size"] += 1
   my_map["current_factor"] = size(my_map)/my_map["capacity"]
   if my_map["current_factor"] > my_map["limit_factor"]:
      rehash(my_map)
   return my_map

def  find_slot(my_map, key, hash_value):
   first_avail = None
   found = False
   ocupied = False
   while not found:
      if is_available(my_map["table"], hash_value):
            if first_avail is None:
               first_avail = hash_value
            entry = al.get_element(my_map["table"], hash_value)
            if me.get_key(entry) is None:
               found = True
      elif default_compare(key, al.get_element(my_map["table"], hash_value)) == 0:
            first_avail = hash_value
            found = True
            ocupied = True
      hash_value = (hash_value + 1) % my_map["capacity"]
   return ocupied, first_avail
    
def is_available(table, pos):

   entry = al.get_element(table, pos)
   if me.get_key(entry) is None or me.get_key(entry) == "__EMPTY__":
      return True
   return False

def default_compare(key, entry):

   if key == me.get_key(entry):
      return 0
   elif key > me.get_key(entry):
      return 1
   return -1

def contains(my_map, key):
    hash_value = mf.hash_value(my_map, key)
    pos = find_slot(my_map, key, hash_value)
    if pos[0]:
        return True
    return False
 
def get(my_map, key):
   pos = find_slot(my_map, key, mf.hash_value(my_map, key))
   if pos[0]:
      return me.get_value(al.get_element(my_map["table"], pos[1]))
   return None

def remove(my_map, key):
   pos = find_slot(my_map, key, mf.hash_value(my_map, key))
   if pos[0]:
      al.change_info(my_map["table"], pos[1], me.new_map_entry("__EMPTY__", "__EMPTY__"))
      my_map["size"] -= 1
      return True
   return False

def size(my_map):
   return my_map["size"]

def is_empty(my_map):
   return size(my_map) == 0

def key_set(my_map):
   keys = al.new_list()
   for i in range(my_map["capacity"]):
      entry = al.get_element(my_map["table"], i)
      if me.get_key(entry) is not None and me.get_key(entry) != "__EMPTY__":
         al.add_last(keys, me.get_key(entry))
   return keys

def value_set(my_map):
   values = al.new_list()
   for i in range(my_map["capacity"]):
      entry = al.get_element(my_map["table"], i)
      if me.get_key(entry) is not None and me.get_key(entry) != "__EMPTY__":
         al.add_last(values, me.get_value(entry))
   return values

def rehash(my_map):
   old_table = my_map["table"]
   my_map["capacity"] = mf.next_prime(2*my_map["capacity"])
   my_map["table"] = table(my_map["capacity"])
   my_map["size"] = 0
   for i in range(al.size(old_table)):
      entry = al.get_element(old_table, i)
      if me.get_key(entry) is not None and me.get_key(entry) != "__EMPTY__":
         put(my_map, me.get_key(entry), me.get_value(entry))
   return my_map