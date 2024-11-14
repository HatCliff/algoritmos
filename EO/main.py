import sys
import os

sep = os.path.sep 

if len(sys.argv) == 6:
    semilla = int(sys.argv[1])
    tau = float(sys.argv[2])
    ite = int(sys.argv[3])
    entrada = "data"+ sep + sys.argv[4]
    salida = "data" + sep + sys.argv[5]
    print(semilla, tau, ite, entrada, salida)
else:
    print("Error en la entrada de datos, deben ser asi: Semilla(int), Tau(float),Iteración(int),Entrada_archivo(string),Salida_archivo(string)")

