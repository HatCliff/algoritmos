import sys
import random
import os
import pandas as pd

sep = os.path.sep 

if len(sys.argv) == 6:
    semilla = int(sys.argv[1])
    tau = float(sys.argv[2])
    ite = int(sys.argv[3])
    entrada = "data" + sep + sys.argv[4]
    salida = "data" + sep + sys.argv[5]
    print(semilla, tau, ite, entrada, salida)

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

else:
    print("Error en la entrada de datos. Deben ser: Semilla(int), Tau(float), Iteración(int), Entrada_archivo(string), Salida_archivo(string)")

# Generamos una solución aleatoria
solucion = [random.randint(0, 1) for _ in range(n)]
print("Solución inicial:", solucion)

# Generamos el array de probabilidades
probabilidades = [i**-tau for i in range(1, n + 1)]
print("Probabilidades:", probabilidades)

# Iteraciones de optimización
for iter_num in range(ite):
    # Evaluamos el fitness en base al peso total de los ítems
    peso_total = 0
    valor_total = 0
    
    # Ciclo para calcular peso y valor total
    for idx in range(n):
        if solucion[idx] == 1:
            peso_total += int(data.iloc[idx, 1])  # Accede a la columna de pesos
            valor_total += int(data.iloc[idx, 2])  # Accede a la columna de valores

    # Penalización si el peso total excede la capacidad
    if peso_total > c:
        valor_total = -1
    
    # Mostrar resultados en cada iteración
    print(f"Iteración {iter_num + 1}: Peso total = {peso_total}, Valor total = {valor_total}")
    
    solucion = [random.randint(0, 1) for _ in range(n)]
