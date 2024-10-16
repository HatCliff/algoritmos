import numpy as np

# Genera una población inicial de tamaño p, donde cada individuo es una permutación aleatoria de n posiciones (reinas).
def generar_poblacion(n, p):
    poblacion = np.zeros((p, n), int)  # Inicializa la matriz de población
    for i in range(p):
        fila = np.arange(n)  # Crea un arreglo de 0 a n-1
        np.random.shuffle(fila)  # Baraja el arreglo para generar una permutación
        poblacion[i] = fila  # Asigna la fila barajada a la matriz
    print(poblacion, "\n")
    return poblacion

# Crea una ruleta de selección que utiliza las aptitudes de los individuos para elegir padres de manera proporcional.
def crea_ruleta(p, fit):
    rule = fit / fit.sum()  # Normaliza las aptitudes para que sumen 1
    rule = np.cumsum(rule)  # Calcula las probabilidades acumuladas
    return rule

# Evalúa la aptitud de cada individuo en la población contando las colisiones de reinas.
def eval_fitness(n, p, poblacion):
    fitness = np.zeros(p, int) 
    for i in range(p):
        colisiones = 0
        for j in range(n):
            for k in range(j + 1, n):
                # Incrementa el contador de colisiones si hay conflicto en las diagonales
                if abs(poblacion[i][j] - poblacion[i][k]) == abs(j - k):
                    colisiones += 1
        fitness[i] = colisiones  # Menos colisiones significa mejor fitness
    return fitness

# Selecciona padres para la nueva generación usando el método de ruleta.
def seleccionar_padres(poblacion, ruleta):
    padres = np.zeros((poblacion.shape[0], poblacion.shape[1]), int)  # Inicializa la matriz de padres
    for i in range(poblacion.shape[0]):
        r = np.random.rand()  # Genera un número aleatorio entre 0 y 1
        for j in range(poblacion.shape[0]):
            if r < ruleta[j]:  # Selecciona un padre según la ruleta
                padres[i] = poblacion[j]
                break
    return padres

# Realiza el cruce entre los padres para generar hijos, asegurando la unicidad de los valores.
def cruzar(padres, pc):
    hijos = np.zeros((padres.shape[0], padres.shape[1]), int)  # Inicializa la matriz de hijos
    for i in range(0, padres.shape[0], 2):  # Itera de dos en dos
        r = np.random.rand()  # Genera un número aleatorio entre 0 y 1
        if r < pc:  # Realiza el cruce si r es menor que la probabilidad de cruce
            punto_cruza = np.random.randint(1, padres.shape[1] - 1)  # Selecciona un punto de cruce
            # Copia la parte inicial de los padres al nuevo hijo
            hijos[i][:punto_cruza] = padres[i][:punto_cruza]
            hijos[i + 1][:punto_cruza] = padres[i + 1][:punto_cruza]
            
            # Completa los hijos asegurando que no haya duplicados
            for j in range(punto_cruza, padres.shape[1]):
                # Rellenar con valores únicos del padre 2
                for val in padres[i + 1]:
                    if val not in hijos[i]:
                        hijos[i][j] = val
                        break

            for j in range(punto_cruza, padres.shape[1]):
                # Rellenar con valores únicos del padre 1
                for val in padres[i]:
                    if val not in hijos[i + 1]:
                        hijos[i + 1][j] = val
                        break
        else:
            # Si no se realiza el cruce, los hijos son copias de los padres
            hijos[i] = padres[i]
            hijos[i + 1] = padres[i + 1]
    return hijos

# Introduce mutaciones en los hijos con una probabilidad pm, cambiando un gen en un individuo.
def mutar(hijos, pm):
    for i in range(hijos.shape[0]):
        r = np.random.rand()
        if r < pm:  # Realiza la mutación si r es menor que pm
            punto_mutacion = np.random.randint(hijos.shape[1])  # Selecciona un gen a mutar
            fila_actual = hijos[i][punto_mutacion]  # Guarda el valor actual
            
            # Genera un nuevo valor aleatorio para la mutación
            nuevo_valor = np.random.randint(hijos.shape[1])
            intentos = 0
            max_intentos = 10  # Limita el número de intentos para encontrar un nuevo valor
            
            # Busca un nuevo valor que no esté en la fila actual
            while nuevo_valor in hijos[i] or nuevo_valor == fila_actual:
                if intentos >= max_intentos:  # Si se alcanzan los intentos máximos, sale
                    break
                nuevo_valor = np.random.randint(hijos.shape[1])
                intentos += 1
            
            # Asigna el nuevo valor si es válido
            if nuevo_valor not in hijos[i] and nuevo_valor != fila_actual:
                hijos[i][punto_mutacion] = nuevo_valor  # Aplica la mutación
                
    return hijos
