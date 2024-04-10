import matplotlib.pyplot as plt
import random
import sys
from statistics import *
from math import *
from itertools import *

# Crear una lista vacía para almacenar los resultados de las tiradas
corridas_promedios = []
media_esperada = 18
frecuencia_esperada = 1 / 37
varianza_esperada = 114
desvio_esperado = 10.677

def promedio_por_tirada(cantidad_tiradas):
    tiradas_promedios = []
    resultados = []
    for i in range(cantidad_tiradas): # for para las tiradas
      # Generamos un número aleatorio entre 0 y 36
      resultado_tirada = random.randint(0, 36)
      resultados.append(resultado_tirada)
      tiradas_promedios.append(mean(resultados)) # Se guarda el promedio luego de cada tirada
    corridas_promedios.append(mean(resultados))
    return tiradas_promedios


def grafica_promedio(tiradas_promedios, cantidad_tiradas):
  plt.plot(range(0,cantidad_tiradas),tiradas_promedios, color='red')
  plt.axhline(y=media_esperada, color='b', label='Media Esperada')
  plt.xlabel("Numero de tirada")
  plt.ylabel("Promedio")
  plt.title("Evaluacion del promedio sobre el conjunto de valores aleatorios")

def grafica_promedios(corridas_promedios, cantidad_corridas):
  plt.plot(range(0,cantidad_corridas),corridas_promedios, marker = 'o',color = 'r')
  plt.axhline(y=media_esperada, color='b', label='Media Esperada')
  plt.xlabel("Numero de corrida")
  plt.ylabel("Promedio")
  plt.title("Evaluacion de la media aritmetica de cada corrida")
  plt.grid()

def frecuencia_relativa_por_tirada(cantidad_tiradas):
  tiradas_frecuencia = []
  resultados = []
  for i in range(cantidad_tiradas): # for para las tiradas
      # Generamos un número aleatorio entre 0 y 36
      resultado_tirada = random.randint(0, 36)
      resultados.append(resultado_tirada)
      frecuencia_numero_elegido = resultados.count(numero_elegido) / len(resultados)
      tiradas_frecuencia.append(frecuencia_numero_elegido)
  return tiradas_frecuencia

def grafica_frecuencia_relativa(tiradas_frecuencia, cantidad_tiradas):
  plt.plot(range(0,cantidad_tiradas),tiradas_frecuencia)
  plt.axhline(y=frecuencia_esperada, color='b', label='Frecuencia relativa esperada')
  plt.xlabel("Numero de tirada")
  plt.ylabel("Frecuencia relativa")
  plt.title("Evaluacion de la frecuencia relativa sobre el conjunto de valores aleatorios")

def frecuencia_absoluta_por_corrida(cantidad_tiradas):
  corridas_frecuencias = []
  resultados = []
  for i in range(cantidad_tiradas): # for para las tiradas
      # Generamos un número aleatorio entre 0 y 36
      resultado_tirada = random.randint(0, 36)
      resultados.append(resultado_tirada)
  for i in range(0,36):
    corridas_frecuencias.append(resultados.count(i) / cantidad_tiradas)
  return corridas_frecuencias

def grafica_frecuencias_absolutas(corridas_frecuencias, cantidad_tiradas):
  plt.plot(range(0,36),corridas_frecuencias)
  plt.axhline(y=1/37, color = "gray")
  plt.xlabel("Numeros obtenidos")
  plt.ylabel("Frecuencia absoluta")
  plt.title("Evaluacion de la frecuencia absoluta sobre el conjunto de valores aleatorios")


def desvio_estandar_por_tiradas(cantidad_tiradas):
  tiradas_desvio = []
  resultados = []
  for i in range(cantidad_tiradas): # for para las tiradas
      # Generamos un número aleatorio entre 0 y 36
      resultado_tirada = random.randint(0, 36)
      resultados.append(resultado_tirada)
      tiradas_desvio.append(pstdev(resultados))  #stdev calcula el desvio poblacional
  return tiradas_desvio

def grafica_desvio_estandar(tiradas_desvio, cantidad_tiradas):
  plt.plot(range(0,cantidad_tiradas),tiradas_desvio)
  plt.axhline(y=desvio_esperado, color='b', label='Desvío estandar esperado')
  plt.xlabel("Numero de tirada")
  plt.ylabel("Desvío estandar")
  plt.title("Evaluacion del desvío estandar sobre el conjunto de valores aleatorios")

def varianza_por_tirada(cantidad_tiradas):
  tiradas_varianza = []
  resultados = []
  for i in range(cantidad_tiradas): # for para las tiradas
      # Generamos un número aleatorio entre 0 y 36
      resultado_tirada = random.randint(0, 36)
      resultados.append(resultado_tirada)
      tiradas_varianza.append(pvariance(resultados))
  return tiradas_varianza

def grafica_varianza(tiradas_varianza, cantidad_tiradas):
  plt.plot(range(0,cantidad_tiradas),tiradas_varianza)
  plt.axhline(y=varianza_esperada, color='b', label='Varianza esperada')
  plt.xlabel("Numero de tirada")
  plt.ylabel("Varianza")
  plt.title("Evaluacion de la varianza sobre el conjunto de valores aleatorios")


if len(sys.argv) != 7 or sys.argv[1] != "-n" or sys.argv[3] != "-c" or sys.argv[5] != "-e":
    print("Uso: python script.py -n <cantidad_tiradas> -c <corridas> -e <número_elegido>")
    sys.exit(1)
cantidad_corridas = int(sys.argv[4])
cantidad_tiradas = int(sys.argv[2])
numero_elegido = int(sys.argv[6])
for j in range(cantidad_corridas):
  grafica_promedio(promedio_por_tirada(cantidad_tiradas), cantidad_tiradas)
plt.show()
grafica_promedios(corridas_promedios,cantidad_corridas)
plt.show()
for j in range(cantidad_corridas):
  grafica_frecuencia_relativa(frecuencia_relativa_por_tirada(cantidad_tiradas), cantidad_tiradas)
plt.show()
for j in range(cantidad_corridas):
  grafica_frecuencias_absolutas(frecuencia_absoluta_por_corrida(cantidad_tiradas), cantidad_tiradas)
plt.show()
for j in range(cantidad_corridas):
  grafica_desvio_estandar(desvio_estandar_por_tiradas(cantidad_tiradas), cantidad_tiradas)
plt.show()
for j in range(cantidad_corridas):
  grafica_varianza(varianza_por_tirada(cantidad_tiradas), cantidad_tiradas)
plt.show()