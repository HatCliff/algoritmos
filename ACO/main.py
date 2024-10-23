import sys
import numpy as np
from functions.utils import *

if len(sys.argv) == 6:
    semilla = int(sys.argv[1])
    iteraciones = int(sys.argv[2])  # Número de iteraciones (entre 100 y 500)
    hormigas = int(sys.argv[3])  # Número de hormigas (entre 10 y 100)
    alpha = float(sys.argv[4])  # Factor de evaporación (alpha)
    beta = float(sys.argv[5])  # Coeficiente heurístico (beta entre 2 y 5)
    q_0 = 0.9  # Valor constante
else:
    print("Error en la entrada de los parámetros. Los parámetros a ingresar son: semilla iteraciones hormigas alpha beta")
    sys.exit(0)

filename = "data/berlin52.tsp.txt"
data = leer_data(filename)
np.random.seed(semilla)

n = len(data)
resultados = generar_poblacion(n,n)
matriz_distancia = matriz_distancias(data)
matriz_heuristica = 1 / np.linalg.inv(matriz_distancia)




