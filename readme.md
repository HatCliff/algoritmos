# Readme Algoritmos genéticos
## Integrantes
- Lucas Ayala Casanova
- Pablo González Keller
- Patricio Pizarro Tapia
## Estructura del Proyecto

El proyecto consta de los siguientes archivos:

- `main.py`: Archivo principal que gestiona la ejecución del algoritmo genético.
- `functions/genetica.py`: Contiene las funciones relacionadas con la generación de la población, evaluación de la aptitud, selección de padres, cruce y mutación.
- `functions/visual.py`: Incluye funciones para visualizar el estado de la población y los tableros generados (para esta tarea fue solo 1 función pero en pos del orden pusimos otro archivo).

## Uso
Escribir en la terminal el siguiente comando:
```bash
python3 main.py <semilla> <tamañoTablero> <tamañoPoblacion> <nroIteraciones> <probCruza> <probMutacion>
```
Donde:
- `semilla`: Semilla para la generación de números aleatorios.
- `tamañoTablero`: Tamaño del tablero cuadrado.
- `tamañoPoblacion`: Cantidad de individuos en la población.
- `nroIteraciones`: Cantidad de iteraciones a realizar.
- `probCruza`: Probabilidad de cruce.
- `probMutacion`: Probabilidad de mutación.

Ejemplo:
```bash
python main.py 42 8 20 100 70 80
```
Esto ejecuta el programa con una semilla de 42, un tablero de 8x8, 20 individuos en la población, 100 iteraciones, una probabilidad de cruce del 70% y una probabilidad de mutación del 80%.

# Breve explicación del codigo
Generación de Población: Se inicializa una población de individuos donde cada uno representa una posible solución al problema (una permutación de las posiciones de las reinas, segun lo visto en clases).
```python
def generar_poblacion(n, p):
    poblacion = np.zeros((p, n), int)
    for i in range(p):
        fila = np.arange(n)
        np.random.shuffle(fila)
        poblacion[i] = fila
    return poblacion
```
Evaluación de Aptitud: Se calcula el número de colisiones (conflictos entre reinas) para determinar la "aptitud" de cada individuo; menos colisiones implican una mejor solución.
```python
def eval_fitness(n, p, poblacion):
    fitness = np.zeros(p, int) 
    for i in range(p):
        colisiones = 0
        for j in range(n):
            for k in range(j + 1, n):
                if abs(poblacion[i][j] - poblacion[i][k]) == abs(j - k):
                    colisiones += 1
        fitness[i] = colisiones
    return fitness
```

Selección de Padres: Utilizando un método de ruleta, se seleccionan padres basados en su aptitud para generar una nueva generación.
```python
def seleccionar_padres(poblacion, ruleta):
    padres = np.zeros((poblacion.shape[0], poblacion.shape[1]), int)
    for i in range(poblacion.shape[0]):
        r = np.random.rand()
        for j in range(poblacion.shape[0]):
            if r < ruleta[j]:
                padres[i] = poblacion[j]
                break
    return padres
```
Cruce: Se realiza el cruce entre padres para producir nuevos hijos, asegurando que cada individuo mantenga posiciones únicas.
```python
def cruzar(padres, pc):
    hijos = np.zeros((padres.shape[0], padres.shape[1]), int)
    for i in range(0, padres.shape[0], 2):
        r = np.random.rand()
        if r < pc:
            punto_cruza = np.random.randint(1, padres.shape[1] - 1)
            hijos[i][:punto_cruza] = padres[i][:punto_cruza]
            hijos[i + 1][:punto_cruza] = padres[i + 1][:punto_cruza]
            for j in range(punto_cruza, padres.shape[1]):
                for val in padres[i + 1]:
                    if val not in hijos[i]:
                        hijos[i][j] = val
                        break
            for j in range(punto_cruza, padres.shape[1]):
                for val in padres[i]:
                    if val not in hijos[i + 1]:
                        hijos[i + 1][j] = val
                        break
        else:
            hijos[i] = padres[i]
            hijos[i + 1] = padres[i + 1]
    return hijos
```
Mutación: Se introducen cambios aleatorios en algunos individuos para aumentar la variabilidad genética de la población.
```python
def mutar(hijos, pm):
    for i in range(hijos.shape[0]):
        r = np.random.rand()
        if r < pm:
            punto_mutacion = np.random.randint(hijos.shape[1])
            fila_actual = hijos[i][punto_mutacion]
            nuevo_valor = np.random.randint(hijos.shape[1])
            intentos = 0
            max_intentos = 10
            while nuevo_valor in hijos[i] or nuevo_valor == fila_actual:
                if intentos >= max_intentos:
                    break
                nuevo_valor = np.random.randint(hijos.shape[1])
                intentos += 1
            if nuevo_valor not in hijos[i] and nuevo_valor != fila_actual:
                hijos[i][punto_mutacion] = nuevo_valor
    return hijos
```

Visualizacion: Se incluye una función para visualizar el estado de la población y los tableros generados.
```python
def dibujar_tablero(n,poblacion, pos_poblacion):
    tablero = np.zeros((n,n),int)
    for i in range(n):
        tablero[poblacion[pos_poblacion][i]][i] = '1'
    print(tablero)    
```
