
# Descripción del Código

Este script es una implementación de un algoritmo de optimización inspirado en algoritmos de colonias de hormigas para un problema de mochila. El objetivo del código es encontrar la mejor solución para maximizar el valor de los elementos seleccionados, sin exceder la capacidad de la mochila. A continuación se explica cada parte del código:

## Parámetros de Entrada

```python
if len(sys.argv) == 6:
    # Parámetros de entrada
    semilla = int(sys.argv[1])
    coeficiente_tau = float(sys.argv[2])
    max_iteraciones = int(sys.argv[3])
    ruta_entrada = "data" + sep + sys.argv[4]
    ruta_salida = "data" + sep + sys.argv[5]
    print(semilla, coeficiente_tau, max_iteraciones, ruta_entrada, ruta_salida)
```

En esta sección, el script recibe 5 parámetros desde la línea de comandos:

- `semilla`: Un valor entero utilizado para inicializar la semilla de los generadores de números aleatorios.
- `coeficiente_tau`: Un valor flotante que se utilizará para controlar la influencia de las probabilidades de selección.
- `max_iteraciones`: El número máximo de iteraciones que se ejecutará el algoritmo.
- `ruta_entrada`: El archivo de datos de entrada que contiene la información del problema (nombre, capacidad, valores y pesos).
- `ruta_salida`: El archivo donde se guardará la solución encontrada.

## Carga de Datos

```python
# Cargar datos
datos = pd.read_table(ruta_entrada, header=None)
print(datos)
```

En esta sección, se carga el archivo de entrada como un DataFrame de `pandas`. El archivo debe estar formateado de tal manera que la primera fila contiene el nombre del problema, la segunda fila contiene la cantidad de elementos, la tercera la capacidad y la cuarta el valor objetivo. Luego, se cargan los valores y pesos de los elementos a partir de la fila 5 en adelante.

## Generación de la Solución Aleatoria

```python
# Generamos una solución aleatoria
random.seed(semilla)
solucion_actual = np.array([random.randint(0, 1) for _ in range(cantidad_elementos)])
mejor_solucion = np.zeros(cantidad_elementos, dtype=int)
print("Solución inicial:", solucion_actual)
```

En este bloque, se genera una solución inicial aleatoria. Cada elemento tiene una probabilidad de ser seleccionado (1) o no (0). Esta solución es evaluada en cada iteración.

## Evaluación de la Factibilidad

```python
# Evaluar si la solución inicial es factible
es_factible = factible(cantidad_elementos, datos, solucion_actual)
if es_factible:
    mejor_solucion = solucion_actual.copy()
    print("La solución es factible")
else:
    print("La solución no es factible")
```

Aquí se evalúa si la solución generada es factible, es decir, si el peso total de los elementos seleccionados no excede la capacidad de la mochila. Esto se hace utilizando la función `factible`.

## Iteraciones para Mejorar la Solución

```python
# Iterar hasta alcanzar el máximo de iteraciones o el valor objetivo
iteracion_actual = 0
while iteracion_actual < max_iteraciones and valor_solucion < valor_objetivo:
    # Crear arreglo de fitness
    fitness = np.column_stack((datos.iloc[:, 0] / datos.iloc[:, 1], np.arange(cantidad_elementos)))
    print("Fitness inicial:", fitness)
```

Este bloque realiza el ciclo de optimización. El algoritmo realiza iteraciones para mejorar la solución actual, buscando siempre maximizar el valor de los elementos seleccionados, mientras respeta la capacidad de la mochila. 

## Funciones Auxiliares

### Función `factible`

```python
def factible(n, datos, solucion):
    print(datos.head())  # Mostrar las primeras filas para verificar estructura
    peso = 0
    for i in range(n):
        peso += datos.iloc[i, 1] * solucion[i]  # Acceso con iloc
    if peso > datos.iloc[0, 2]:  # Asegurar acceso correcto a capacidad
        return False
    return True
```

La función `factible` evalúa si una solución es válida, comprobando si el peso total de los elementos seleccionados no supera la capacidad de la mochila.

### Función `calc_valor`

```python
def calc_valor(n, datos, solucion):
    valor = 0
    for i in range(n):
        valor += datos.iloc[i, 0] * solucion[i]  # Acceso con iloc
    return valor
```

La función `calc_valor` calcula el valor total de la solución, sumando los valores de los elementos seleccionados en la solución.

### Función `ruleta`

```python
def ruleta(n, tau):
    # Calcular las probabilidades basadas en la fórmula
    probabilidades = np.power(np.arange(1, n + 1), -tau)
    # Normalizar para que sumen 1
    probabilidades /= probabilidades.sum()
    # Calcular la suma acumulada
    return np.cumsum(probabilidades)
```

La función `ruleta` calcula la probabilidad de seleccionar cada elemento en función de su fitness, y devuelve una lista de probabilidades acumuladas que se utilizan para la selección en el proceso de optimización.

## Escritura de la Solución en el Archivo de Salida

```python
# Escribir la solución en el archivo de salida
pd.DataFrame(mejor_solucion).to_csv(ruta_salida, header=None, index=None)
```

Finalmente, la mejor solución encontrada se guarda en un archivo CSV en la ruta especificada.

## Requisitos

- Python 3.x
- pandas
- numpy

### Instalación de Dependencias

```bash
pip install pandas numpy
```

## Ejecución del Script

El script se debe ejecutar desde la línea de comandos, pasando los parámetros necesarios:

```bash
python script.py <semilla> <coeficiente_tau> <max_iteraciones> <archivo_entrada> <archivo_salida>
```

## Ejemplo

```bash
python script.py 1234 1.5 100 data/entrada.txt data/salida.csv
```
