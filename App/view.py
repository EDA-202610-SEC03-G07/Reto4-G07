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

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


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
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
