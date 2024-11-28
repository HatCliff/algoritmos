import sys
import random
import os
import pandas as pd

sep = os.path.sep
import random

def generar_solucion_inicial(data, capacidad_max):
    """
    Genera una solución inicial válida en la que el peso total no exceda la capacidad máxima de la mochila.
    """
    solucion = [0] * len(data)
    peso_total = 0

    # Iteramos hasta que no se pueda agregar más ítems sin exceder la capacidad
    while peso_total < capacidad_max:
        idx = random.randint(0, len(data) - 1)  # Seleccionamos un ítem aleatorio
        if solucion[idx] == 0:  # Si no ha sido seleccionado
            peso_item = int(data.iloc[idx, 1])  # Accedemos al peso del ítem
            if peso_total + peso_item <= capacidad_max:
                solucion[idx] = 1  # Marcamos el ítem como seleccionado
                peso_total += peso_item  # Actualizamos el peso total
    return solucion

# Función para evaluar la solución
def evaluar_solucion(solucion, data, capacidad_max):
    peso_total = 0
    valor_total = 0
    for idx in range(len(solucion)):
        if solucion[idx] == 1:
            peso_total += int(data.iloc[idx, 1])  # Accedemos al peso del ítem
            valor_total += int(data.iloc[idx, 2])  # Accedemos al valor del ítem
    
    # Si el peso total excede la capacidad, se penaliza la solución
    if peso_total > capacidad_max:
        return -1, peso_total  # Penalización (-1) si la capacidad es excedida
    
    return valor_total, peso_total

# Función para generar una nueva solución vecina
def generar_vecina(solucion):
    nueva_solucion = solucion[:]
    # Cambiar un ítem aleatorio 
    idx = random.randint(0, len(solucion) - 1)
    nueva_solucion[idx] = 1 - nueva_solucion[idx]  # Cambia de 0 a 1 o de 1 a 0
    return nueva_solucion

# Función para calcular las probabilidades de selección basada en el rango
def calcular_probabilidades(fitness_values):
    # Calcular el rango de los elementos
    ranked_indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i])
    # Generar probabilidades de selección por el rango
    probabilidades = [0] * len(fitness_values)
    total_rank = sum(range(1, len(fitness_values) + 1))  # Suma de rangos
    for i, idx in enumerate(ranked_indices):
        probabilidades[idx] = (i + 1) / total_rank  # Asigna la probabilidad de acuerdo al rango
    return probabilidades

# Función para seleccionar un componente usando Selección por Rango (RWS)
def seleccionar_componente(probabilidades):
    rand = random.random()
    acumulado = 0.0
    for idx, prob in enumerate(probabilidades):
        acumulado += prob
        if acumulado >= rand:
            return idx
    return len(probabilidades) - 1

# Algoritmo principal
def optimizar_mochila(data, capacidad_max, iteraciones, tau_inicial):
    # Generamos una solución inicial aleatoria
    solucion = [random.randint(0, 1) for _ in range(len(data))]
    mejor_solucion = solucion
    mejor_valor, mejor_peso = evaluar_solucion(solucion, data, capacidad_max)

    for iter_num in range(iteraciones):
        # Evaluar fitness de cada componente
        fitness_values = []
        for i in range(len(solucion)):
            vecina = generar_vecina(solucion[:i] + [1 - solucion[i]] + solucion[i + 1:])
            valor_vecina, _ = evaluar_solucion(vecina, data, capacidad_max)
            fitness_values.append(valor_vecina)

        # Calcular las probabilidades según los valores de fitness
        probabilidades = calcular_probabilidades(fitness_values)

        # Selección del componente a modificar (por RWS)
        componente_seleccionado = seleccionar_componente(probabilidades)

        # Generamos una nueva vecina cambiando el componente seleccionado
        nueva_solucion = solucion[:]
        nueva_solucion[componente_seleccionado] = 1 - nueva_solucion[componente_seleccionado]

        # Evaluamos la nueva solución
        valor_nueva, peso_nueva = evaluar_solucion(nueva_solucion, data, capacidad_max)

        # Si la nueva solución es mejor, la actualizamos como la mejor solución
        if valor_nueva > mejor_valor:
            mejor_solucion = nueva_solucion
            mejor_valor = valor_nueva
            mejor_peso = peso_nueva

        # Si la nueva solución es peor pero aceptable, la aceptamos con una probabilidad basada en tau
        elif valor_nueva < mejor_valor:
            prob_aceptacion = random.random()
            if prob_aceptacion < tau_inicial:
                mejor_solucion = nueva_solucion
                mejor_valor = valor_nueva
                mejor_peso = peso_nueva

        # Reducir tau (enfriamiento)
        tau_inicial *= 0.995  # Enfriamiento exponencial

        # Mostrar el progreso
        print(f"Iteración {iter_num + 1}/{iteraciones}: Mejor valor = {mejor_valor}, Mejor peso = {mejor_peso}")

    return mejor_solucion, mejor_valor, mejor_peso

# Main
if len(sys.argv) == 6:
    semilla = int(sys.argv[1])
    tau = float(sys.argv[2])
    ite = int(sys.argv[3])
    entrada = "data" + sep + sys.argv[4]
    salida = "data" + sep + sys.argv[5]
    print(semilla, tau, ite, entrada, salida)

    # Cargar datos desde el archivo
    data = pd.read_table(entrada, header=None)
    print(data)

    # Leer parámetros del archivo
    nombre_problema = data[0][0]
    n = int(data[0][1].split()[1])
    c = int(data[0][2].split()[1])
    z = int(data[0][3].split()[1])
    print("Nombre del problema:", nombre_problema)
    print("n:", n)
    print("c:", c)
    print("z:", z)

    # Eliminar encabezados y procesar datos
    data.drop(data.index[0:5], axis=0, inplace=True)  # Eliminar encabezados
    data.drop(data.tail(1).index, axis=0, inplace=True)  # Eliminar última fila

    # Dividir la columna en varias columnas
    data = data[0].str.split(",", expand=True)
    print(data)

    # Ejecutar el algoritmo de optimización
    mejor_solucion, mejor_valor, mejor_peso = optimizar_mochila(data, c, ite, tau)

    # Mostrar la mejor solución encontrada
    print("\nMejor solución encontrada:")
    print("Ítems seleccionados:", mejor_solucion)
    print("Valor total:", mejor_valor)
    print("Peso total:", mejor_peso)
else:
    print("Error en la entrada de datos. Deben ser: Semilla(int), Tau(float), Iteración(int), Entrada_archivo(string), Salida_archivo(string)")
