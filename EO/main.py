import sys
import os
#from functions.procesamiento_datos import * 
import pandas as pd
sep = os.path.sep 

if len(sys.argv) == 6:
    semilla = int(sys.argv[1])
    tau = float(sys.argv[2])
    ite = int(sys.argv[3])
    entrada = "data"+ sep + sys.argv[4]
    salida = "data" + sep + sys.argv[5]
    print(semilla, tau, ite, entrada, salida)

    data = pd.read_table(entrada,  header=None)
    print(data)

    nombre_problema=data[0][0]
    n=int(data[0][1].split()[1])
    c=int(data[0][2].split()[1])
    z=int(data[0][3].split()[1])
    print("nombre del problema: ", nombre_problema, type(nombre_problema))
    print("n: ",n,type(n))
    print("c: ",c,type(c))
    print("z: ",z,type(z))

    # Eliminar filas y procesar datos
    data.drop(data.index[0:5], axis=0, inplace=True)  # Eliminar encabezados
    data.drop(data.tail(1).index, axis=0, inplace=True)  # Eliminar última fila
    print(data)
    # Dividir columna en varias columnas
    data = data[0].str.split(",", expand=True)
    print(data)

else:
    print("Error en la entrada de data, deben ser asi: Semilla(int), Tau(float),Iteración(int),Entrada_archivo(string),Salida_archivo(string)")





