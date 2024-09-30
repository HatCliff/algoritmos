import sys
import numpy as np
from functions.genetica import *
from functions.visual import *
#Esto hace que pasemos los valores de la terminal por el jupyter notebook
#          Seed    N    P   Iter     ProbCruza   ProbMut
if len(sys.argv) == 7:
    semilla = int(sys.argv[1] or '1')
    n = int(sys.argv[2] or '6')
    p = int(sys.argv[3] or '10')
    ite = int(sys.argv[4] or '10')
    pc = float(sys.argv[5] or '50') / 100
    pm = float(sys.argv[6] or '80') / 100
else:
    print("Error en la entrada de los parámetros \n Los parámetros a ingresar son: semilla tamañoTablero TamañoPoblacion NroIteraciones ProbCruza ProbMutacion")
    sys.exit(0)

np.random.seed(semilla)

print("Población inicial:\n")

poblacion = generar_poblacion(n,p)
eval_fitness(n,p,poblacion)

#dibujar_tablero(n ,poblacion, 0) #Cambiar por cualquier numero para ver otro tablero

ruleta = crea_ruleta(p, eval_fitness(n,p,poblacion))
resultados = np.zeros(ite, int)
for i in range(ite):
    padres = seleccionar_padres(poblacion, ruleta)
    hijos = cruzar(padres, pc)
    mutar(hijos, pm)
    eval_fitness(n,p,hijos)

#Imprime la cantidad de soluciones que se encontraron
print("Soluciones encontradas:\n", hijos, "\n")
#dibujar_tablero(n ,hijos,0) #Cambiar por cualquier numero para ver otro tablero

mejor_solucion = np.argmin(eval_fitness(n,p,hijos))
print("Mejor solución encontrada:\033[32m", mejor_solucion, "\n\033[0m El individuo es:\033[32m", hijos[mejor_solucion],"\033[0m \n")

