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
from DataStructures.Graph import bfs as bfs_module


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
        "vertex_order": al.new_list(),
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
            al.add_last(catalog["records"], registro)
            catalog["total_records"] += 1

            zona = registro["zona"]
            mmsi = registro["mmsi"] 

            # Vértice por zona, info acumulada y lista de registros
            if not digraph.contains_vertex(catalog["graph"], zona):
                records_list = al.new_list()
                al.add_last(records_list, registro)

                map_mmsi= mp.new_map(10)
                map_nombres = mp.new_map(10)
                map_tipos = mp.new_map(10)
                map_cargas  = mp.new_map(10)
                map_categorias = mp.new_map(10)
                mp.put(map_mmsi,registro["mmsi"], registro["mmsi"])
                mp.put(map_nombres,registro["nombre"],registro["nombre"])
                mp.put(map_tipos,registro["tipo"],registro["tipo"])
                mp.put(map_cargas,registro["carga"],registro["carga"])
                mp.put(map_categorias, registro["categoria_velocidad"], registro["categoria_velocidad"])

                info = {
                    "id":zona,
                    "suma_lat":registro["lat"],
                    "suma_lon":registro["lon"],
                    "suma_velocidad": registro["velocidad"],
                    "suma_longitud": registro["longitud"],
                    "suma_ancho": registro["ancho"],
                    "suma_calado":registro["calado"],
                    "records_count":1,
                    "map_mmsi":map_mmsi,
                    "map_nombres":map_nombres,
                    "map_tipos": map_tipos,
                    "map_cargas":map_cargas,
                    "map_categorias": map_categorias,
                    "records":records_list,
                }
                digraph.insert_vertex(catalog["graph"], zona, info)
                al.add_last(catalog["vertex_order"], zona)

            else:
                # Zona ya existe: obtener info y acumular
                info = digraph.get_vertex_info(catalog["graph"], zona)
                info["suma_lat"] += registro["lat"]
                info["suma_lon"] += registro["lon"]
                info["suma_velocidad"] += registro["velocidad"]
                info["suma_longitud"]  += registro["longitud"]
                info["suma_ancho"]  += registro["ancho"]
                info["suma_calado"] += registro["calado"]
                info["records_count"]+= 1
                mp.put(info["map_mmsi"],registro["mmsi"],registro["mmsi"])
                mp.put(info["map_nombres"],registro["nombre"], registro["nombre"])
                mp.put(info["map_tipos"],registro["tipo"], registro["tipo"])
                mp.put(info["map_cargas"],registro["carga"],registro["carga"])
                mp.put(info["map_categorias"],registro["categoria_velocidad"], registro["categoria_velocidad"])
                al.add_last(info["records"], registro)
                digraph.update_vertex_info(catalog["graph"], zona, info)

            # Priority queue por embarcación, prioridad = BASEDATETIME
            cola = mp.get(catalog["mmsi_records_map"], mmsi)
            if cola is None:
                cola = pq.new_heap(is_min_heap=True)
                mp.put(catalog["mmsi_records_map"], mmsi, cola)
                catalog["total_vessels"] += 1
            pq.insert(cola, registro["fecha"], registro)

    #finalizar vértices (calcular promedios y listas)
    llaves_zonas = digraph.vertices(catalog["graph"])
    for i in range(al.size(llaves_zonas)):
        zona = al.get_element(llaves_zonas, i)
        info = digraph.get_vertex_info(catalog["graph"], zona)
        n = info["records_count"]

        info["lat"] = round(info["suma_lat"] / n, 2)
        info["lon"] = round(info["suma_lon"] / n, 2)
        info["avg_sog"] = round(info["suma_velocidad"] / n, 2)
        info["avg_length"] = round(info["suma_longitud"] / n, 2)
        info["avg_width"] = round(info["suma_ancho"] / n, 2)
        info["avg_draft"] = round(info["suma_calado"]/ n, 2)
        info["mmsi_list"] = mp.key_set(info["map_mmsi"])
        info["vessel_names"] = mp.key_set(info["map_nombres"])
        info["vessel_types"] = mp.key_set(info["map_tipos"])
        info["cargo_types"] = mp.key_set(info["map_cargas"])
        info["speed_categories"] = mp.key_set(info["map_categorias"])
        # Liberar acumuladores internos
        info["suma_lat"] = None
        info["suma_lon"] = None
        info["suma_velocidad"]  = None
        info["suma_longitud"] = None
        info["suma_ancho"] = None
        info["suma_calado"] = None
        info["map_mmsi"] = None
        info["map_nombres"] = None
        info["map_tipos"] = None
        info["map_cargas"] = None
        info["map_categorias"]  = None

        digraph.update_vertex_info(catalog["graph"], zona, info)

    #recorrer trayectorias y construir edge_info_map
    llaves_mmsi = mp.key_set(catalog["mmsi_records_map"])
    for i in range(al.size(llaves_mmsi)):
        mmsi = al.get_element(llaves_mmsi, i)
        cola = mp.get(catalog["mmsi_records_map"], mmsi)

        registros_ordenados = al.new_list()
        while not pq.is_empty(cola):
            registro = pq.remove(cola)
            al.add_last(registros_ordenados, registro)

        n = al.size(registros_ordenados)
        for j in range(n - 1):
            reg_a = al.get_element(registros_ordenados, j)
            reg_b = al.get_element(registros_ordenados, j + 1)

            zona_a = reg_a["zona"]
            zona_b = reg_b["zona"]

            if zona_a == zona_b:
                continue

            llave_arco = zona_a + "_" + zona_b

            t1 = datetime.strptime(reg_a["fecha"], "%Y-%m-%d %H:%M:%S")
            t2 = datetime.strptime(reg_b["fecha"], "%Y-%m-%d %H:%M:%S")
            tiempo_min = abs((t2 - t1).total_seconds() / 60)

            arco = mp.get(catalog["edge_info_map"], llave_arco)
            if arco is None:
                info_a = digraph.get_vertex_info(catalog["graph"], zona_a)
                info_b = digraph.get_vertex_info(catalog["graph"], zona_b)
                dist = distancia_haversine(info_a["lat"], info_a["lon"],
                                           info_b["lat"], info_b["lon"])
                times_list = al.new_list()
                mmsi_list = al.new_list()
                categorias_list = al.new_list()
                al.add_last(times_list,tiempo_min)
                al.add_last(mmsi_list, mmsi)
                al.add_last(categorias_list, reg_a["categoria_velocidad"])
                arco = {
                    "source":zona_a,
                    "target":zona_b,
                    "trips_count":1,
                    "distance":dist,
                    "times":times_list,
                    "trip_mmsi_list":mmsi_list,
                    "trip_speed_categories": categorias_list,
                    "avg_time":None,
                }
                mp.put(catalog["edge_info_map"], llave_arco, arco)
            else:
                arco["trips_count"] += 1
                al.add_last(arco["times"], tiempo_min)
                al.add_last(arco["trip_mmsi_list"],mmsi)
                al.add_last(arco["trip_speed_categories"], reg_a["categoria_velocidad"])

    # calcular avg_time y agregar arcos al grafo
    llaves_arcos = mp.key_set(catalog["edge_info_map"])
    for i in range(al.size(llaves_arcos)):
        llave_arco = al.get_element(llaves_arcos, i)
        arco = mp.get(catalog["edge_info_map"], llave_arco)

        n_tiempos = al.size(arco["times"])
        if n_tiempos > 0:
            suma = 0.0
            for j in range(al.size(arco["times"])):
                suma += al.get_element(arco["times"], j)
            arco["avg_time"] = round(suma / n_tiempos, 2)
        else:
            arco["avg_time"] = 0.0

        digraph.add_edge(catalog["graph"], arco["source"], arco["target"], arco["distance"])

    tiempo_fin = get_time()
    delta = delta_time(tiempo_inicio, tiempo_fin)

    primeros, ultimos = primeros_ultimos_vertices(catalog)
    return (catalog,
            catalog["total_records"],
            catalog["total_vessels"],
            digraph.order(catalog["graph"]),
            digraph.size(catalog["graph"]),
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
def primeros_ultimos_vertices(catalog):
    #llaves = digraph.vertices(catalog["graph"])
    llaves = catalog["vertex_order"]
    n = al.size(llaves)
    primeros = al.new_list()
    ultimos  = al.new_list()
    for i in range(min(5, n)):
        info = digraph.get_vertex_info(catalog["graph"], al.get_element(llaves, i))
        al.add_last(primeros, info)
    for i in range(max(0, n - 5), n):
        info = digraph.get_vertex_info(catalog["graph"], al.get_element(llaves, i))
        al.add_last(ultimos, info)
    return primeros, ultimos

def distancia_haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia en kilómetros entre dos puntos geográficos
    usando la fórmula de Haversine.
    """
    R = 6371.0
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi / 2)**2 + cos(phi1) * cos(phi2) * sin(dlambda / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return round(R * c, 2)



# Funciones de consulta sobre el catálogo
def req_1(catalog, zona_origen, zona_destino):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    resultado = {
        "existe":       False,
        "total_zonas":  0,
        "vertices":     al.new_list(),
        "origen_ok":    digraph.contains_vertex(catalog["graph"], zona_origen),
        "destino_ok":   digraph.contains_vertex(catalog["graph"], zona_destino),
    }

    if not resultado["origen_ok"] or not resultado["destino_ok"]:
        return resultado

    if zona_origen == zona_destino:
        resultado["existe"]      = True
        resultado["total_zonas"] = 1
        info = digraph.get_vertex_info(catalog["graph"], zona_origen)
        al.add_last(resultado["vertices"], vertex_summary(info))
        return resultado

    # BFS desde el origen
    visited_map = bfs_module.bfs(catalog["graph"], zona_origen)

    if not bfs_module.has_path_to(zona_destino, visited_map):
        return resultado

    # Reconstruir camino con path_to
    path_stack = bfs_module.path_to(zona_destino, visited_map)
    path = al.new_list()
    from DataStructures.Stack import stack as st
    while not st.is_empty(path_stack):
        al.add_last(path, st.pop(path_stack))

    total = al.size(path)
    resultado["existe"] = True
    resultado["total_zonas"] = total

    # Índices a mostrar primeros 5 y últimos 5
    if total <= 10:
        for i in range(total):
            zona_key = al.get_element(path, i)
            info_v   = digraph.get_vertex_info(catalog["graph"], zona_key)
            al.add_last(resultado["vertices"], vertex_summary(info_v))
    else:
        for i in range(5):
            zona_key = al.get_element(path, i)
            info_v   = digraph.get_vertex_info(catalog["graph"], zona_key)
            al.add_last(resultado["vertices"], vertex_summary(info_v))
        for i in range(total - 5, total):
            zona_key = al.get_element(path, i)
            info_v   = digraph.get_vertex_info(catalog["graph"], zona_key)
            al.add_last(resultado["vertices"], vertex_summary(info_v))

    return resultado


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


def req_4(catalog, zona_origen):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    resultado = {
        "origen_ok":   digraph.contains_vertex(catalog["graph"], zona_origen),
        "total_zonas": 0,
        "costo_total": 0.0,
        "arcos":       al.new_list(),
        "arcos_tabla": al.new_list(),
    }
 
    if not resultado["origen_ok"]:
        return resultado
 
    # Dijkstra
    aux = bfs_module.dijkstra(catalog["graph"], zona_origen)
    visited_map = aux["visited"]
 
    # Recorrer visited_map para extraer arcos del SPT
    llaves = mp.key_set(visited_map)
    for i in range(al.size(llaves)):
        key_v = al.get_element(llaves, i)
        info  = mp.get(visited_map, key_v)
        if info["marked"] and info["edge_from"] is not None:
            origen_arco  = info["edge_from"]
            dist_destino = info["dist_to"]
            dist_origen  = mp.get(visited_map, origen_arco)["dist_to"]
            peso = round(dist_destino - dist_origen, 2)
            arco = {
                "origen":  origen_arco if origen_arco  is not None else "Unknown",
                "destino": key_v       if key_v        is not None else "Unknown",
                "peso":    peso,
            }
            al.add_last(resultado["arcos"], arco)
        if info["marked"]:
            resultado["total_zonas"] += 1
 
    # Ordenar arcos por origen asc, en empate por destino asc
    sort_arcos(resultado["arcos"])
 
    # Costo total
    costo = 0.0
    for i in range(al.size(resultado["arcos"])):
        costo += al.get_element(resultado["arcos"], i)["peso"]
    resultado["costo_total"] = round(costo, 2)
 
    # Primeros 5 y últimos 5 arcos
    total_arcos = al.size(resultado["arcos"])
    if total_arcos <= 10:
        for i in range(total_arcos):
            al.add_last(resultado["arcos_tabla"], al.get_element(resultado["arcos"], i))
    else:
        for i in range(5):
            al.add_last(resultado["arcos_tabla"], al.get_element(resultado["arcos"], i))
        for i in range(total_arcos - 5, total_arcos):
            al.add_last(resultado["arcos_tabla"], al.get_element(resultado["arcos"], i))
 
    return resultado
    


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

#Otros helpers
def vertex_summary(info):
    """Extrae la información resumida de un vértice para el Req 1."""
    mmsi_list    = info["mmsi_list"]    if info["mmsi_list"]    is not None else al.new_list()
    vessel_names = info["vessel_names"] if info["vessel_names"] is not None else al.new_list()
    return {
        "id": info["id"]  if info["id"]  is not None else "Unknown",
        "lat":info["lat"] if info["lat"] is not None else "Unknown",
        "lon":info["lon"] if info["lon"] is not None else "Unknown",
        "n_embarcaciones": al.size(mmsi_list),
        "nombres":primeros_ultimos_nombres(vessel_names, 3),
    }


def primeros_ultimos_nombres(nombres_al, n):
    """Retorna lista Python con los primeros n y últimos n nombres (o todos si ≤ 2n)."""
    total = al.size(nombres_al)
    result = al.new_list()
    if total == 0:
        al.add_last(result, "Unknown")
        return result
    if total <= 2 * n:
        for i in range(total):
            nombre = al.get_element(nombres_al, i)
            al.add_last(result, nombre if nombre and str(nombre) not in ("None", "") else "Unknown")
    else:
        for i in range(n):
            nombre = al.get_element(nombres_al, i)
            al.add_last(result, nombre if nombre and str(nombre) not in ("None", "") else "Unknown")
        for i in range(total - n, total):
            nombre = al.get_element(nombres_al, i)
            al.add_last(result, nombre if nombre and str(nombre) not in ("None", "") else "Unknown")
    return result

def sort_arcos(arcos_al):
    al.merge_sort(arcos_al, cmp_arcos)
    return arcos_al

def cmp_arcos(a, b):
    if a["origen"] < b["origen"]:
        return True
    if a["origen"] == b["origen"] and a["destino"] < b["destino"]:
        return True
    return False