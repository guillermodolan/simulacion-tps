import matplotlib.pyplot as plt
import random
import sys
from statistics import *
from math import *
from itertools import *

# Datos
CANT_NUMEROS = 37
promedios_corridas = []
f_absolutas_corridas = [0 for _ in range(CANT_NUMEROS)]
resultados_totales = []
MEDIA_ESPERADA = sum([x for x in range(CANT_NUMEROS)]) / CANT_NUMEROS
FRECUENCIA_ESPERADA = 1 / CANT_NUMEROS
VARIANZA_ESPERADA = sum([(x - MEDIA_ESPERADA)**2 for x in range(CANT_NUMEROS)]) / CANT_NUMEROS
DESVIO_ESPERADO = sqrt(VARIANZA_ESPERADA)

# Funciones
def promedio_por_tirada(resultados_tiradas):
    promedios_tiradas = []

    for i in range(1, cantidad_tiradas + 1):
       # Se guarda el promedio luego de cada tirada
       promedios_tiradas.append(mean(resultados_tiradas[:i]))

    return promedios_tiradas

def frecuencia_relativa_por_tirada(resultados_tiradas):
  f_relativas_tiradas = []

  for i in range(1, cantidad_tiradas + 1): 
      fr_num_elegido = resultados_tiradas[:i].count(numero_elegido) / len(resultados_tiradas[:i])
      # Se guarda la frecuencia relativa luego de cada tirada
      f_relativas_tiradas.append(fr_num_elegido)

  return f_relativas_tiradas

def frecuencia_absoluta_por_corrida(resultados_tiradas):
  f_absolutas_tiradas = []

  for num in range(CANT_NUMEROS):
    # Se cuenta cuantas veces salio cada numero en las n tiradas de una corrida
    f_absolutas_tiradas.append(resultados_tiradas.count(num))

  return f_absolutas_tiradas

def varianza_por_tirada(resultados_tiradas):
  varianzas_tiradas = []

  for i in range(1, cantidad_tiradas + 1): 
    # Se guarda la varianza luego de cada tirada
    varianzas_tiradas.append(pvariance(resultados_tiradas[:i]))

  return varianzas_tiradas

def desvio_stndr_por_tirada(varianzas_tiradas):
  return [sqrt(var) for var in varianzas_tiradas]

#Graficas
def creacion_ventanas():
  plt.figure('promedios_tiradas')
  plt.figure('promedios_corridas')
  plt.figure('f_relativas_tiradas')
  plt.figure('f_absolutas_tiradas')
  plt.figure('varianzas_tiradas')
  plt.figure('desvios_standar_tiradas')

def grafica_promedios_tiradas(promedios_tiradas, cantidad_tiradas):
  plt.figure('promedios_tiradas')
  plt.plot(range(cantidad_tiradas),promedios_tiradas,linewidth=0.2)
  plt.axhline(y=MEDIA_ESPERADA,color='b',label='Media Esperada')
  plt.xlabel("Numero de tirada")
  plt.ylabel("Promedio")
  plt.title("Evaluacion del promedio sobre el conjunto de valores aleatorios")

def grafica_promedios_corridas(promedios_corridas, cantidad_corridas):
  plt.figure('promedios_corridas')
  plt.plot(range(0,cantidad_corridas),promedios_corridas, marker = 'o',linewidth=0.7, markersize=3)
  plt.axhline(y=MEDIA_ESPERADA, color='b', label='Media Esperada')
  plt.xlabel("Numero de corrida")
  plt.ylabel("Promedio")
  plt.title("Evaluacion del promedio de cada corrida")
  plt.grid()

def grafica_frecuencia_relativa(f_relativas_tiradas, cantidad_tiradas):
  plt.figure('f_relativas_tiradas')
  plt.plot(range(cantidad_tiradas),f_relativas_tiradas,color="red",linewidth=0.2)
  plt.axhline(y=FRECUENCIA_ESPERADA,color='b',label='Frecuencia relativa esperada')
  plt.xlabel("Numero de tirada")
  plt.ylabel("Frecuencia relativa")
  plt.title("Evaluacion de la frecuencia relativa sobre el conjunto de valores aleatorios")

def grafica_frecuencias_absolutas(resultados_totales, cantidad_tiradas, cantidad_corridas):
  plt.figure('f_absolutas_tiradas')
  plt.hist(resultados_totales, CANT_NUMEROS, rwidth=0.75)
  plt.axhline(y=cantidad_tiradas*cantidad_corridas/CANT_NUMEROS, color = "gray")
  plt.xlabel("Numeros obtenidos")
  plt.ylabel("Frecuencia absoluta")
  plt.title("Evaluacion de la frecuencia absoluta sobre el conjunto de valores aleatorios")

def grafica_desvio_estandar(desvios_standar_tiradas, cantidad_tiradas):
  plt.figure('desvios_standar_tiradas')
  plt.plot(range(cantidad_tiradas),desvios_standar_tiradas,linewidth=0.2)
  plt.axhline(y=DESVIO_ESPERADO, color='b', label='Desvío estandar esperado')
  plt.xlabel("Numero de tirada")
  plt.ylabel("Desvío estandar")
  plt.title("Evaluacion del desvío estandar sobre el conjunto de valores aleatorios")

def grafica_varianza(varianzas_tiradas, cantidad_tiradas):
  plt.figure('varianzas_tiradas')
  plt.plot(range(0,cantidad_tiradas),varianzas_tiradas,linewidth=0.2)
  plt.axhline(y=VARIANZA_ESPERADA, color='b', label='Varianza esperada')
  plt.xlabel("Numero de tirada")
  plt.ylabel("Varianza")
  plt.title("Evaluacion de la varianza sobre el conjunto de valores aleatorios")

# Captura argumentos desde consola
if len(sys.argv) != 7 or sys.argv[1] != "-n" or sys.argv[3] != "-c" or sys.argv[5] != "-e":
    print("Uso: python script.py -n <cantidad_tiradas> -c <corridas> -e <número_elegido>")
    sys.exit(1)
cantidad_corridas = int(sys.argv[4])
cantidad_tiradas = int(sys.argv[2])
numero_elegido = int(sys.argv[6])

# Creacion ventanas
creacion_ventanas()

# Ejecucion
for _ in range(cantidad_corridas):
  resultados_tiradas = [random.randint(0, CANT_NUMEROS - 1) for _ in range(cantidad_tiradas)]
  resultados_totales.extend(resultados_tiradas) # Utilizado para la grafica de frecuencia absoluta
  promedios_tiradas = promedio_por_tirada(resultados_tiradas)
  promedios_corridas.append(mean(resultados_tiradas))
  f_relativas_tiradas = frecuencia_relativa_por_tirada(resultados_tiradas)
  f_absolutas_tiradas = frecuencia_absoluta_por_corrida(resultados_tiradas)
  f_absolutas_corridas = [(n + f_absolutas_tiradas[i]) for (i, n) in enumerate(f_absolutas_corridas)]
  varianzas_tiradas = varianza_por_tirada(resultados_tiradas)
  desvios_standar_tiradas = desvio_stndr_por_tirada(varianzas_tiradas)

  grafica_promedios_tiradas(promedios_tiradas, cantidad_tiradas)
  grafica_frecuencia_relativa(f_relativas_tiradas, cantidad_tiradas)
  grafica_varianza(varianzas_tiradas, cantidad_tiradas)
  grafica_desvio_estandar(desvios_standar_tiradas, cantidad_tiradas)

grafica_frecuencias_absolutas(resultados_totales, cantidad_tiradas, cantidad_corridas)
grafica_promedios_corridas(promedios_corridas, cantidad_corridas)

plt.show()
