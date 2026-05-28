import sys
default_limit = 1000
sys.setrecursionlimit(default_limit*10)
import App.logic as logic  
from tabulate import tabulate
from DataStructures.List import array_list as al

def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función de la lógica donde se crean las estructuras de datos
    control = logic.new_logic()
    return control

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    filename = "ais_maritime_traffic_100pct.csv"
    (control, total_records, total_vessels, total_vertices, total_edges, delta_time, primeros, ultimos) = logic.load_data(control, filename)

    summary = [
        ["Archivo cargado",            filename],
        ["Total de registros cargados", total_records],
        ["Total de embarcaciones",      total_vessels],
        ["Total de vértices (zonas)",   total_vertices],
        ["Total de arcos",              total_edges],
        ["Tiempo de carga (ms)",        f"{delta_time:.2f}"],
    ]

    print("\n" + "=" * 70)
    print("              RESUMEN DE CARGA DE DATOS")
    print("=" * 70)
    print(tabulate(summary, headers=["Métrica", "Valor"], tablefmt="rounded_outline", colalign=("left", "right")))

    print("\n" + "=" * 70)
    print("         PRIMEROS 5 VÉRTICES CREADOS")
    print("=" * 70)
    print(tabulate(vertices_to_rows(primeros), headers=vertices_headers(), tablefmt="rounded_outline"))

    print("\n" + "=" * 70)
    print("         ÚLTIMOS 5 VÉRTICES CREADOS")
    print("=" * 70)
    print(tabulate(vertices_to_rows(ultimos), headers=vertices_headers(), tablefmt="rounded_outline"))

    return control


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control, zona_origen, zona_destino):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    resultado = logic.req_1(control, zona_origen, zona_destino)
 
    print("\n" + "=" * 70)
    print("          REQUERIMIENTO 1 — TRAYECTORIA ENTRE ZONAS")
    print("=" * 70)
 
    # Validar existencia de zonas
    if not resultado["origen_ok"]:
        print(f"\n La zona de origen '{zona_origen}' no existe en el grafo.")
        return
    if not resultado["destino_ok"]:
        print(f"\n La zona de destino '{zona_destino}' no existe en el grafo.")
        return
 
    if not resultado["existe"]:
        print(f"\n No existe trayectoria entre '{zona_origen}' y '{zona_destino}'.")
        return
 
    total = resultado["total_zonas"]
    print(f"\n  Trayectoria encontrada de '{zona_origen}' a '{zona_destino}'")
    print(f"  Total de zonas en la trayectoria: {total}")
 
    if total > 10:
        print("\n" + "=" * 70)
        print("Se muestran los 5 primeros y 5 últimos vértices")
        print("=" * 70)
 
    print()
    vertices_list = resultado["vertices"]
    rows = []
    for i in range(al.size(vertices_list)):
        v = al.get_element(vertices_list, i)
        nombres_al  = v["nombres"]
        partes = []
        for j in range(al.size(nombres_al)):
            partes.append(al.get_element(nombres_al, j))
        nombres_str = " | ".join(partes)
        rows.append([
            i + 1,
            v["id"],
            v["lat"],
            v["lon"],
            v["n_embarcaciones"],
            nombres_str,
        ])
 
    headers = [
        "#",
        "ID Zona",
        "Latitud",
        "Longitud",
        "Embarcaciones",
        "Nombres (primeros 3 y últimos 3)",
    ]
    print(tabulate(rows, headers=headers, tablefmt="rounded_outline",colalign=("center", "left", "right", "right", "right", "left")))


def print_req_2(control, zona_origen, radio):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    resultado = logic.req_2(control, zona_origen, radio)

    print("\n" + "=" * 70)
    print("      REQUERIMIENTO 2 — MOVIMIENTOS DENTRO DE UN ÁREA")
    print("=" * 70)

    if not resultado["zona_ok"]:
        print(f"\n La zona de navegación '{zona_origen}' no existe en el grafo.")
        return

    print(f"\n  Zona de interés      : {zona_origen}")
    print(f"  Radio consultado     : {radio:.2f} km")
    print(f"  Zonas alcanzables    : {resultado['total_zonas']}")

    zonas_list = resultado["zonas"]

    if al.size(zonas_list) == 0:
        print("\n No se encontraron zonas dentro del área de interés.")
        return

    rows = []
    for i in range(al.size(zonas_list)):
        zona = al.get_element(zonas_list, i)

        rows.append([
            i + 1,
            zona["id"] if zona["id"] is not None else "Unknown",
            zona["lat"] if zona["lat"] is not None else "Unknown",
            zona["lon"] if zona["lon"] is not None else "Unknown",
            zona["records_count"] if zona["records_count"] is not None else "Unknown",
            zona["avg_sog"] if zona["avg_sog"] is not None else "Unknown",
            f"{zona['distancia']:.2f}" if zona["distancia"] is not None else "Unknown",
        ])

    headers = [
        "#",
        "ID Zona",
        "Latitud",
        "Longitud",
        "Total Registros",
        "Vel. Promedio",
        "Distancia (km)",
    ]

    print()
    print(tabulate(
        rows,
        headers=headers,
        tablefmt="rounded_outline",
        colalign=("center", "left", "right", "right", "right", "right", "right")
    ))


def print_req_3(control, n):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    resultado = logic.req_3(control, n)

    print("\n" + "=" * 70)
    print("     REQUERIMIENTO 3 — CONEXIONES MÁS FRECUENTES")
    print("=" * 70)
    print(f"\n  Top {n} conexiones más frecuentes\n")

    rows = []
    for i in range(al.size(resultado)):
        arco = al.get_element(resultado, i)
        rows.append([
            i + 1,
            arco["source"],
            arco["target"],
            arco["trips_count"],
            arco["distance"],
            arco["avg_time"],
        ])

    if rows:
        headers = ["#", "Zona Origen", "Zona Destino", "Total Viajes", "Distancia (km)", "Tiempo Prom (min)"]
        print(tabulate(rows, headers=headers, tablefmt="rounded_outline"))
    else:
        print("\n  No se encontraron conexiones.") 


def print_req_4(control, zona_origen):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    resultado = logic.req_4(control, zona_origen)
 
    print("\n" + "=" * 70)
    print("     REQUERIMIENTO 4 — RED DE CAMINOS MÍNIMOS (DIJKSTRA)")
    print("=" * 70)
 
    if not resultado["origen_ok"]:
        print(f"\n La zona '{zona_origen}' no existe en el grafo.")
        return
 
    print(f"\n  Zona de origen       : {zona_origen}")
    print(f"  Zonas conectadas     : {resultado['total_zonas']}")
    print(f"  Costo total de la red: {resultado['costo_total']:.2f} km")
    print(f"  Total de arcos SPT   : {al.size(resultado['arcos'])}")
 
    total_arcos = al.size(resultado["arcos"])
    if total_arcos > 10:
        print("\n" + "=" * 70)
        print("Se muestran los 5 primeros y 5 últimos arcos")
        print("=" * 70)
 
    rows = []
    for i in range(al.size(resultado["arcos_tabla"])):
        arco = al.get_element(resultado["arcos_tabla"], i)
        rows.append([
            i + 1,
            arco["origen"]  if arco["origen"]  is not None else "Unknown",
            arco["destino"] if arco["destino"] is not None else "Unknown",
            f"{arco['peso']:.2f}",
        ])
 
    headers = ["#", "Zona Origen", "Zona Destino", "Peso (km)"]
    print()
    print(tabulate(rows, headers=headers, tablefmt="rounded_outline",
                   colalign=("center", "left", "left", "right")))


def print_req_5(control, zona_origen, zona_destino):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """

    resultado = logic.req_5(control, zona_origen, zona_destino)

    print("\n" + "=" * 70)
    print("       REQUERIMIENTO 5 — RUTA MÁS EFICIENTE ENTRE ZONAS")
    print("=" * 70)

    if not resultado["origen_ok"]:
        print(f"\n La zona de origen '{zona_origen}' no existe en el grafo.")
        return

    if not resultado["destino_ok"]:
        print(f"\n La zona de destino '{zona_destino}' no existe en el grafo.")
        return

    if not resultado["existe"]:
        print(f"\n No existe ruta entre '{zona_origen}' y '{zona_destino}'.")
        return

    print(f"\n  Ruta encontrada de '{zona_origen}' a '{zona_destino}'")
    print(f"  Costo total de la ruta : {resultado['costo_total']:.2f} km")
    print(f"  Total de zonas         : {resultado['total_zonas']}")
    print(f"  Total de arcos         : {resultado['total_arcos']}")

    if resultado["total_zonas"] > 10:
        print("\n" + "=" * 70)
        print("Se muestran los 5 primeros y 5 últimos vértices de la ruta")
        print("=" * 70)

    rows = []
    vertices_list = resultado["vertices"]

    for i in range(al.size(vertices_list)):
        v = al.get_element(vertices_list, i)

        peso = v["peso_siguiente"]
        if peso != "Unknown":
            peso = f"{peso:.2f}"

        rows.append([
            i + 1,
            v["id"],
            v["lat"],
            v["lon"],
            v["n_embarcaciones"],
            peso
        ])

    headers = [
        "#",
        "ID Zona",
        "Latitud",
        "Longitud",
        "Embarcaciones",
        "Peso al siguiente (km)"
    ]

    print()
    print(tabulate(
        rows,
        headers=headers,
        tablefmt="rounded_outline",
        colalign=("center", "left", "right", "right", "right", "right")
    ))


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    resultado = logic.req_6(control)

    total_subredes = al.size(resultado)

    print("\n" + "=" * 70)
    print("     REQUERIMIENTO 6 — CONECTIVIDAD BIDIRECCIONAL")
    print("=" * 70)
    print(f"\n  Total de subredes encontradas: {total_subredes}\n")

    limite = min(5, total_subredes)

    for i in range(limite):
        subred = al.get_element(resultado, i)
        zonas = subred["zonas"]
        cantidad_zonas = len(zonas)

        print(f"  Subred {subred['id_subred']}")
        print(f"  Zonas en la subred : {subred['total_zonas']}")
        print(f"  Total registros    : {subred['total_registros']}")
        print(f"  Velocidad promedio : {subred['avg_sog']}")

        if cantidad_zonas <= 10:
            zonas_str = " | ".join(zonas)
        else:
            primeras = " | ".join(zonas[:5])
            ultimas = " | ".join(zonas[cantidad_zonas - 5:])
            zonas_str = primeras + "  ...  " + ultimas

        print(f"  Zonas              : {zonas_str}")
        print("-" * 70)


# Funciones auxiliares para formatear la salida
def vertices_headers():
    return [
        "ID Zona",
        "Latitud",
        "Longitud",
        "Total Registros",
        "Vel. Promedio (nudos)",
        "Embarcaciones",
    ]


def vertices_to_rows(vertices_list):
    rows = []
    for i in range(al.size(vertices_list)):
        v = al.get_element(vertices_list, i)
        mmsi_list = v["mmsi_list"]
        n_embarcaciones = al.size(mmsi_list)
        rows.append([
            v["id"],
            v["lat"],
            v["lon"],
            v["records_count"],
            v["avg_sog"],
            n_embarcaciones,
        ])  
    return rows

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            zona_origen = input("Ingrese la zona de origen: ").strip()
            zona_destino = input("Ingrese la zona de destino: ").strip()
            print_req_1(control, zona_origen, zona_destino)

        elif int(inputs) == 2:
            zona_origen = input("Ingrese el identificador de la zona de navegación de interés: ")
            radio = float(input("Ingrese el radio del área de interés en kilómetros: "))
            print_req_2(control, zona_origen, radio)

        elif int(inputs) == 3:
            n = int(input("Ingrese el número de conexiones a consultar: "))
            print_req_3(control, n)

        elif int(inputs) == 4:
            zona_origen = input("Ingrese la zona de origen: ").strip()
            print_req_4(control, zona_origen)

        elif int(inputs) == 5:
            zona_origen = input("Ingrese el identificador de la zona de origen: ")
            zona_destino = input("Ingrese el identificador de la zona de destino: ")
            print_req_5(control, zona_origen, zona_destino) 

        elif int(inputs) == 6:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
