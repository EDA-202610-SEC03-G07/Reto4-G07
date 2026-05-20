import time
import csv
import time
import os
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime
 
from DataStructures.Graph import digraph
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.List import array_list as al
 


def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    catalog = {
        "records":          al.new_list(),
        "total_records":    0,
        "total_vessels":    0,
        "vertices":         mp.new_map(3000),
        "mmsi_records_map": mp.new_map(15000),
        "edge_info_map":    mp.new_map(50000),
        "graph":            digraph.new_graph(3000),
    }
    return catalog


# Funciones para la carga de datos
data_dir = data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'Data')
def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    tiempo_inicio = get_time()
    ruta = os.path.join(data_dir, filename)
    archivo = csv.DictReader(open(ruta, encoding='utf-8'))
 
    for fila in archivo:
        registro = limpiar_registro(fila)
        al.add_last(catalog["registros"], registro)
        catalog["total_registros"] += 1
 
        zona = registro["zona"]
        mmsi = registro["mmsi"]
 
        vertice = mp.get(catalog["vertices"], zona)
        if vertice is None:
            vertice = nuevo_vertice(registro)
            mp.put(catalog["vertices"], zona, vertice)
        else:
            actualizar_vertice(vertice, registro)
 
        cola = mp.get(catalog["mapa_mmsi"], mmsi)
        if cola is None:
            cola = pq.new_heap(is_min_pq=True)
            mp.put(catalog["mapa_mmsi"], mmsi, cola)
            catalog["total_embarcaciones"] += 1
        pq.insert(cola, registro, registro["fecha"])
 
    llaves_zonas = mp.key_set(catalog["vertices"])
    for zona in llaves_zonas["elements"]:
        vertice = mp.get(catalog["vertices"], zona)
        finalizar_vertice(vertice)
        digraph.insert_vertex(catalog["grafo"], zona, vertice)
 
    llaves_mmsi = mp.key_set(catalog["mapa_mmsi"])
    for mmsi in llaves_mmsi["elements"]:
        cola = mp.get(catalog["mapa_mmsi"], mmsi)
 
        registros_ordenados = al.new_list()
        while not pq.is_empty(cola):
            registro = pq.del_min(cola)
            al.add_last(registros_ordenados, registro)
 
        n = al.size(registros_ordenados)
        for i in range(n - 1):
            reg_a = al.get_element(registros_ordenados, i)
            reg_b = al.get_element(registros_ordenados, i + 1)
 
            zona_a = reg_a["zona"]
            zona_b = reg_b["zona"]
 
            if zona_a == zona_b:
                continue
 
            llave_arco = zona_a + "_" + zona_b
 
            t1 = datetime.strptime(reg_a["fecha"], "%Y-%m-%d %H:%M:%S")
            t2 = datetime.strptime(reg_b["fecha"], "%Y-%m-%d %H:%M:%S")
            tiempo_min = abs((t2 - t1).total_seconds() / 60)
 
            arco = mp.get(catalog["mapa_arcos"], llave_arco)
            if arco is None:
                va   = mp.get(catalog["vertices"], zona_a)
                vb   = mp.get(catalog["vertices"], zona_b)
                dist = distancia_haversine(va["lat"], va["lon"], vb["lat"], vb["lon"])
                arco = nuevo_arco(zona_a, zona_b, dist, tiempo_min, mmsi, reg_a["categoria_velocidad"])
                mp.put(catalog["mapa_arcos"], llave_arco, arco)
            else:
                actualizar_arco(arco, tiempo_min, mmsi, reg_a["categoria_velocidad"])
 
    llaves_arcos = mp.key_set(catalog["mapa_arcos"])
    for llave_arco in llaves_arcos["elements"]:
        arco = mp.get(catalog["mapa_arcos"], llave_arco)
        arco["tiempo_promedio"] = round(arco["suma_tiempos"] / arco["total_viajes"], 2)
        del arco["suma_tiempos"]
        digraph.add_edge(catalog["grafo"], arco["origen"], arco["destino"], arco["distancia"])
 
    tiempo_fin = get_time()
    delta = delta_time(tiempo_inicio, tiempo_fin)
 
    primeros, ultimos = primeros_ultimos_vertices(catalog)
    return (catalog,
            catalog["total_registros"],
            catalog["total_embarcaciones"],
            digraph.order(catalog["grafo"]),
            digraph.size(catalog["grafo"]),
            delta,
            primeros,
            ultimos)
 
 
def limpiar_registro(fila):
    return {
        "mmsi":               str(fila["MMSI"]),
        "fecha":              str(fila["BASEDATETIME"]),
        "lat":                float(fila["LAT"])     if fila["LAT"]     else 0.0,
        "lon":                float(fila["LON"])     if fila["LON"]     else 0.0,
        "velocidad":          float(fila["SOG"])     if fila["SOG"]     else 0.0,
        "longitud":           float(fila["LENGTH"])  if fila["LENGTH"]  else 0.0,
        "ancho":              float(fila["WIDTH"])   if fila["WIDTH"]   else 0.0,
        "calado":             float(fila["DRAFT"])   if fila["DRAFT"]   else 0.0,
        "zona":               str(fila["DEST_CLUSTER"]),
        "nombre":             str(fila["VESSELNAME"])      if fila["VESSELNAME"]      else "Unknown",
        "tipo":               str(fila["VESSELTYPE"])      if fila["VESSELTYPE"]      else "Unknown",
        "carga":              str(fila["CARGO"])           if fila["CARGO"]           else "Unknown",
        "categoria_velocidad":str(fila["SPEED_CATEGORY"])  if fila["SPEED_CATEGORY"]  else "Unknown",
    }
 
 
def nuevo_vertice(registro):
    return {
        "id":               registro["zona"],
        "suma_lat":         registro["lat"],
        "suma_lon":         registro["lon"],
        "suma_velocidad":   registro["velocidad"],
        "suma_longitud":    registro["longitud"],
        "suma_ancho":       registro["ancho"],
        "suma_calado":      registro["calado"],
        "total_registros":  1,
        "set_mmsi":         {registro["mmsi"]},
        "set_nombres":      {registro["nombre"]},
        "set_tipos":        {registro["tipo"]},
        "set_cargas":       {registro["carga"]},
        "set_categorias":   {registro["categoria_velocidad"]},
    }
 
 
def actualizar_vertice(vertice, registro):
    vertice["suma_lat"]       += registro["lat"]
    vertice["suma_lon"]       += registro["lon"]
    vertice["suma_velocidad"] += registro["velocidad"]
    vertice["suma_longitud"]  += registro["longitud"]
    vertice["suma_ancho"]     += registro["ancho"]
    vertice["suma_calado"]    += registro["calado"]
    vertice["total_registros"] += 1
    vertice["set_mmsi"].add(registro["mmsi"])
    vertice["set_nombres"].add(registro["nombre"])
    vertice["set_tipos"].add(registro["tipo"])
    vertice["set_cargas"].add(registro["carga"])
    vertice["set_categorias"].add(registro["categoria_velocidad"])
 
 
def finalizar_vertice(vertice):
    n = vertice["total_registros"]
    vertice["lat"]               = round(vertice["suma_lat"]      / n, 2)
    vertice["lon"]               = round(vertice["suma_lon"]      / n, 2)
    vertice["avg_sog"]           = round(vertice["suma_velocidad"] / n, 2)
    vertice["avg_length"]        = round(vertice["suma_longitud"]  / n, 2)
    vertice["avg_width"]         = round(vertice["suma_ancho"]     / n, 2)
    vertice["avg_draft"]         = round(vertice["suma_calado"]    / n, 2)
    vertice["lista_mmsi"]        = list(vertice["set_mmsi"])
    vertice["nombres"]           = list(vertice["set_nombres"])
    vertice["tipos"]             = list(vertice["set_tipos"])
    vertice["cargas"]            = list(vertice["set_cargas"])
    vertice["categorias"]        = list(vertice["set_categorias"])
    del vertice["suma_lat"], vertice["suma_lon"], vertice["suma_velocidad"]
    del vertice["suma_longitud"], vertice["suma_ancho"], vertice["suma_calado"]
    del vertice["set_mmsi"], vertice["set_nombres"]
    del vertice["set_tipos"], vertice["set_cargas"], vertice["set_categorias"]
 
 
def nuevo_arco(zona_a, zona_b, dist, tiempo_min, mmsi, categoria):
    lista_mmsi       = al.new_list()
    lista_categorias = al.new_list()
    al.add_last(lista_mmsi,       mmsi)
    al.add_last(lista_categorias, categoria)
    return {
        "origen":            zona_a,
        "destino":           zona_b,
        "total_viajes":      1,
        "distancia":         dist,
        "suma_tiempos":      tiempo_min,
        "tiempo_promedio":   None,
        "lista_mmsi":        lista_mmsi,
        "lista_categorias":  lista_categorias,
    }
 
 
def actualizar_arco(arco, tiempo_min, mmsi, categoria):
    arco["total_viajes"]  += 1
    arco["suma_tiempos"]  += tiempo_min
    al.add_last(arco["lista_mmsi"],       mmsi)
    al.add_last(arco["lista_categorias"], categoria)
 
 
def primeros_ultimos_vertices(catalog):
    llaves = mp.key_set(catalog["vertices"])
    n      = len(llaves["elements"])
    primeros = al.new_list()
    ultimos  = al.new_list()
    for i in range(min(5, n)):
        vertice = mp.get(catalog["vertices"], llaves["elements"][i])
        al.add_last(primeros, vertice)
    for i in range(-1, -min(6, n + 1), -1):
        vertice = mp.get(catalog["vertices"], llaves["elements"][i])
        al.add_last(ultimos, vertice)
    return primeros, ultimos
# Funciones de consulta sobre el catálogo


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
