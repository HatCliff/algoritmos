import pandas as pd
import numpy as np

def factible(n, datos, solucion):
    print(datos.head())  # Mostrar las primeras filas para verificar estructura
    peso = 0
    for i in range(n):
        peso += datos.iloc[i, 1] * solucion[i]  # Acceso con iloc
    if peso > datos.iloc[0, 2]:  # Asegurar acceso correcto a capacidad
        return False
    return True

def calc_valor(n, datos, solucion):
    valor = 0
    for i in range(n):
        valor += datos.iloc[i, 0] * solucion[i]  # Acceso con iloc
    return valor

def ruleta(n, tau):
    # Calcular las probabilidades basadas en la fórmula
    probabilidades = np.power(np.arange(1, n + 1), -tau)
    # Normalizar para que sumen 1
    probabilidades /= probabilidades.sum()
    # Calcular la suma acumulada
    return np.cumsum(probabilidades)
