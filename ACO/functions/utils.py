import numpy as np
#Codigo de la tarea de genetica
def generar_poblacion(n, p):
    poblacion = np.zeros((p, n), int)  # Inicializa la matriz de población
    for i in range(p):
        fila = np.arange(n)  # Crea un arreglo de 0 a n-1
        np.random.shuffle(fila)  # Baraja el arreglo para generar una permutación
        poblacion[i] = fila  # Asigna la fila barajada a la matriz
    return poblacion
#Fin codigo de la tarea de genetica

def calc_costo(matriz_distancias):
    cost_matrix = np.zeros(matriz_distancias.shape[0])
    for i in range(matriz_distancias.shape[0]):
        cost_matrix[i] = np.sum(matriz_distancias[i])  # Suma las distancias de cada fila
    return cost_matrix


def matriz_distancias(data):
    n = len(data) # Tomamos el num de ciudades
    distancias = np.zeros((n, n), float) # Inicializamos la matriz de distancias
    for i in range(n):
        for j in range(n):
            if i != j:
                distancias[i][j] = np.sqrt((data[i][0] - data[j][0]) ** 2 + (data[i][1] - data[j][1]) ** 2)
    return distancias

def leer_data(filename):
    data = np.loadtxt(filename, skiprows=6, max_rows=52,usecols=(1, 2))
    return data
