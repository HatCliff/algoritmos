import sys
import random
import os
import pandas as pd
import numpy as np
from functions.utilidades import *
sep = os.path.sep

if len(sys.argv) == 6:
    # Parámetros de entrada
    semilla = int(sys.argv[1])
    coeficiente_tau = float(sys.argv[2])
    max_iteraciones = int(sys.argv[3])
    ruta_entrada = "data" + sep + sys.argv[4]
    ruta_salida = "data" + sep + sys.argv[5]
    print(semilla, coeficiente_tau, max_iteraciones, ruta_entrada, ruta_salida)

    # Cargar datos
    datos = pd.read_table(ruta_entrada, header=None)
    print(datos)

    # Leer parámetros del archivo
    nombre_problema = datos.iloc[0, 0]
    cantidad_elementos = int(datos.iloc[1, 0].split()[1])
    capacidad = int(datos.iloc[2, 0].split()[1])
    valor_objetivo = int(datos.iloc[3, 0].split()[1])
    print("Nombre del problema:", nombre_problema)
    print("Cantidad de elementos:", cantidad_elementos)
    print("Capacidad:", capacidad)
    print("Valor objetivo:", valor_objetivo)

    # Procesar datos eliminando encabezados y última fila
    datos = datos.iloc[5:-1, 0].str.split(",", expand=True).astype(float)
    print(datos)

else:
    print("Error en la entrada de datos. Deben ser: Semilla(int), Tau(float), Iteraciones(int), Archivo_entrada(string), Archivo_salida(string)")
    sys.exit(1)

# Generamos una solución aleatoria
random.seed(semilla)
solucion_actual = np.array([random.randint(0, 1) for _ in range(cantidad_elementos)])
mejor_solucion = np.zeros(cantidad_elementos, dtype=int)
print("Solución inicial:", solucion_actual)

# Generar el array de probabilidades
probabilidades = [i**-coeficiente_tau for i in range(1, cantidad_elementos + 1)]
print("Probabilidades:", probabilidades)

# Evaluar si la solución inicial es factible
es_factible = factible(cantidad_elementos, datos, solucion_actual)
if es_factible:
    mejor_solucion = solucion_actual.copy()
    print("La solución es factible")
else:
    print("La solución no es factible")

# Calcular el valor de la solución
valor_solucion = calc_valor(cantidad_elementos, datos, solucion_actual)
print("Valor de la solución:", valor_solucion)

# Iterar hasta alcanzar el máximo de iteraciones o el valor objetivo
iteracion_actual = 0
while iteracion_actual < max_iteraciones and valor_solucion < valor_objetivo:
    # Crear arreglo de fitness
    fitness = np.column_stack((datos.iloc[:, 0] / datos.iloc[:, 1], np.arange(cantidad_elementos)))
    print("Fitness inicial:", fitness)

    # Ordenar por fitness si es factible
    if es_factible:
        fitness_ordenado = fitness[solucion_actual == 0]
        if fitness_ordenado.shape[0] > 0:
            fitness_ordenado = fitness_ordenado[np.argsort(-fitness_ordenado[:, 0])]
        else:
            print("No hay elementos válidos en fitness_ordenado para la solución factible.")
            break
    else:
        fitness_ordenado = fitness[solucion_actual == 1]
        if fitness_ordenado.shape[0] > 0:
            fitness_ordenado = fitness_ordenado[np.argsort(fitness_ordenado[:, 0])]
        else:
            print("No hay elementos válidos en fitness_ordenado para la solución no factible.")
            break

    # Verificar si fitness_ordenado tiene elementos
    if fitness_ordenado.shape[0] == 0:
        print("No hay elementos válidos en fitness_ordenado, terminando...")
        break

    # Crear ruleta
    ruleta_probabilidades = ruleta(len(fitness_ordenado), coeficiente_tau)
    print("Ruleta:", ruleta_probabilidades)

    # Seleccionar elemento mediante la ruleta
    valor_aleatorio = np.random.rand()
    indice_seleccionado = np.searchsorted(ruleta_probabilidades, valor_aleatorio)
    indice_seleccionado = min(max(0, indice_seleccionado), len(fitness_ordenado) - 1)

    # Asegurarse de que el índice seleccionado sea válido
    if indice_seleccionado < 0 or indice_seleccionado >= len(fitness_ordenado):
        print("Índice de selección inválido, terminando...")
        break

    # Actualizar la solución
    indice_elemento = int(fitness_ordenado[indice_seleccionado, 1])
    solucion_actual[indice_elemento] = 1 - solucion_actual[indice_elemento]  # Alternar entre 0 y 1
    print("Solución actualizada:", solucion_actual)

    # Calcular el valor de la nueva solución
    valor_solucion = calc_valor(cantidad_elementos, datos, solucion_actual)

    # Evaluar si la solución es factible
    es_factible = factible(cantidad_elementos, datos, solucion_actual)
    if es_factible:
        mejor_solucion = solucion_actual.copy()

    iteracion_actual += 1

print("Mejor solución:", mejor_solucion)

# Escribir la solución en el archivo de salida
pd.DataFrame(mejor_solucion).to_csv(ruta_salida, header=None, index=None)
