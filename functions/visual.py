import numpy as np
#Ejemplo gráfico de la primera fila de la población, incluí función para comprobar otras filas
def dibujar_tablero(n,poblacion, pos_poblacion):
    tablero = np.zeros((n,n),int)
    for i in range(n):
        tablero[poblacion[pos_poblacion][i]][i] = '1'
    print(tablero)    
#dibujar_tablero(poblacion, 1)


