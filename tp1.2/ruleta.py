# Hay 3 estrategias de apuestas a elegir (m, d, f)
# Hay capital finito o infinito (f, i)
# con f el programa terminaria cuando se quede en bancarrota
# con i se utilizaria el TCL para ver cuantas repeticiones son suficientes
# Hay que crear una estrategia de apuesta (o)
import argparse
from enum import StrEnum, IntEnum
import random
from statistics import mean
import matplotlib.pyplot as plt

# Codigos colores para la ruleta
class Color(StrEnum):
    VERDE = 'v'
    ROJO = 'r'
    NEGRO = 'n'

COLORES = set(color for color in Color)

# Codigos estrategias de apuesta
class Estrategia(StrEnum):
    MARTINGALA = 'm'
    DALEMBERT = 'd'
    FIBONACCI = 'f'
    OTRA = 'o'

ESTRATEGIAS = set(estrategia for estrategia in Estrategia)

# Codigos jugadas
class Jugada(StrEnum):
    ROJO = 'r'
    NEGRO = 'n'
    PAR = 'e'
    IMPAR = 'o'
    DOCENA1 = 'd1'
    DOCENA2 = 'd2'
    DOCENA3 = 'd3'
    FILA1 = 'f1'
    FILA2 = 'f2'
    FILA3 = 'f3'
    BAJOS = 'b'
    ALTOS = 'a'
    PLENO = 'pl'

JUGADAS = set(jugada for jugada in Jugada)

# Codigos probabilidades
PROBABILIDAD = {
    Jugada.ROJO : 18/37,
    Jugada.NEGRO : 18/37,
    Jugada.PAR : 18/37,
    Jugada.IMPAR : 18/37,
    Jugada.DOCENA1 : 12/37,
    Jugada.DOCENA2 : 12/37,
    Jugada.DOCENA3 : 12/37,
    Jugada.FILA1 : 12/37,
    Jugada.FILA2 : 12/37,
    Jugada.FILA3 : 12/37,
    Jugada.BAJOS : 18/37,
    Jugada.ALTOS : 18/37,
    Jugada.PLENO : 1/37
}

# Codigos capitales
class Capital(StrEnum):
    FINITO = 'f'
    INFINITO = 'i'

CAPITALES = set(capital for capital in Capital)

# Creacion ruleta
RULETA = [
    (0, Color.VERDE),
    (1, Color.ROJO), (2, Color.NEGRO), (3, Color.ROJO), (4, Color.NEGRO), (5, Color.ROJO), 
    (6, Color.NEGRO), (7, Color.ROJO), (8, Color.NEGRO), (9, Color.ROJO), (10, Color.NEGRO), 
    (11, Color.NEGRO), (12, Color.ROJO), (13, Color.NEGRO), (14, Color.ROJO), (15, Color.NEGRO), 
    (16, Color.ROJO), (17, Color.NEGRO), (18, Color.ROJO), (19, Color.ROJO), (20, Color.NEGRO), 
    (21, Color.ROJO), (22, Color.NEGRO), (23, Color.ROJO), (24, Color.NEGRO), (25, Color.ROJO), 
    (26, Color.NEGRO), (27, Color.ROJO), (28, Color.NEGRO), (29, Color.NEGRO), (30, Color.ROJO), 
    (31, Color.NEGRO), (32, Color.ROJO), (33, Color.NEGRO), (34, Color.ROJO), (35, Color.NEGRO), 
    (36, Color.ROJO)
]

# Crea las diferentes ventanas de graficas
def creacion_ventanas():
    plt.figure('flujo_caja')
    plt.figure('f_relativas_apuesta_favorable')
    plt.figure('cantidad_apostada')
    plt.figure('promedio_frecuencia_relativa')

# Crea la grafica que muestra el flujo de caja a lo largo de las tiradas
def grafica_flujo_caja(flujo_caja, cantidad_tiradas, CAPITAL_INICIAL):
    plt.figure('flujo_caja')
    plt.plot(range(cantidad_tiradas+1), flujo_caja, linewidth=0.6)
    plt.axhline(y=CAPITAL_INICIAL,color='b',label='Capital Inicial', linewidth=0.4)
    plt.axhline(y=0,color='r',label='0', linewidth=0.4)
    plt.xlabel("Numero de tirada")
    plt.ylabel("Capital")
    plt.title("Evaluacion del flujo de caja")

# Crea la grafica de la frecuencia relativa de obtener una apuesta favorable por tirada
def grafica_frecuencias_apuestas_favorables(f_relativas_apuesta_favorable, cantidad_tiradas, f_relativa_esperada):
    plt.figure('f_relativas_apuesta_favorable')
    plt.plot(range(cantidad_tiradas),f_relativas_apuesta_favorable, linewidth=0.6)
    plt.axhline(y=f_relativa_esperada,color='b',label='Frec Relativa Esperada', linewidth=0.4)
    plt.xlabel("Numero de tirada")
    plt.ylabel("Frecuencia relativa")
    plt.title("Evaluacion de las frecuencias relativas de apuestas favorables")

# Crea la grafica de la cantidad apostada por tirada
def grafica_apuestas(cantidad_apostada_por_tirada, cantidad_tiradas):
    plt.figure('cantidad_apostada')
    plt.plot(range(cantidad_tiradas+1),cantidad_apostada_por_tirada,ls='', marker = 'o', markersize=1)
    # plt.axhline(y=f_relativa_esperada,color='b',label='Frec Relativa Esperada', linewidth=0.4)
    plt.xlabel("Numero de tirada")
    plt.ylabel("Cantidad apostada")
    plt.title("Evaluacion de la evolucion de las apuestas ")

# Crea la grafica de los promedios de las frecuencias relativas de apuestas favorables sobre las tiradas
def grafica_promedio_frecuencias_relativas(promedio_frecuencia_relativa, cantidad_tiradas):
    plt.figure('promedio_frecuencia_relativa')
    plt.plot(range(cantidad_tiradas),promedio_frecuencia_relativa, linewidth=0.6)
    plt.xlabel("Numero de tirada")
    plt.ylabel("Frecuencia relativa")
    plt.title("Evaluacion del promedio de las frecuencias relativas")

# Detecta el tipo de apuesta elegida por el usuario y verifica si gano o perdio la apuesta
def apostar(tipo_jugada, tirada):
    numero, color = tirada

    # Cuando se apuesta por un numero especifico
    if tipo_jugada not in JUGADAS:
        beneficio = 35
        return numero == tipo_jugada, beneficio

    # Cuando no se apuesta a ningun numero y sale 0 -> las jugadas pierden
    if numero == 0: 
        return False, 0
    
    # Cuando se apuesta a un color
    if tipo_jugada == Jugada.ROJO or tipo_jugada == Jugada.NEGRO:
        beneficio = 1
        return color == tipo_jugada, beneficio
    
    # Cuando se apuesta par o impar
    if tipo_jugada == Jugada.PAR or tipo_jugada ==  Jugada.IMPAR:
        beneficio = 1
        if tipo_jugada == Jugada.PAR: 
            return numero % 2 == 0, beneficio
        else:
            return numero % 2 != 0, beneficio
    
    # Cuando se apuesta de 1 a 18 o de 19 a 36
    if tipo_jugada == Jugada.BAJOS or tipo_jugada ==  Jugada.ALTOS:
        beneficio = 1
        if tipo_jugada == Jugada.BAJOS:
            return numero <= 18, beneficio
        else:
            return numero <= 36 and numero >= 19, beneficio
    
    # Cuando se apuesta una docena
    if tipo_jugada == Jugada.DOCENA1 or tipo_jugada == Jugada.DOCENA2 or tipo_jugada == Jugada.DOCENA3:
        beneficio = 2
        if tipo_jugada == Jugada.DOCENA1:
            return numero <= 12, beneficio
        elif tipo_jugada == Jugada.DOCENA2:
            return numero >= 13 and numero <= 24, beneficio
        else:
            return numero >= 25, beneficio

    # Cuando se apuesta una fila
    if tipo_jugada == Jugada.FILA1 or tipo_jugada == Jugada.FILA2 or tipo_jugada == Jugada.FILA3:
        beneficio = 2
        if tipo_jugada == Jugada.FILA1:
            return numero in [x for x in range(1, 36, 3)], beneficio
        elif tipo_jugada == Jugada.FILA2:
            return numero in [x for x in range(2, 36, 3)], beneficio
        else:
            return numero in [x for x in range(3, 36, 3)], beneficio

# Siempre es mejor elegir apuestas con un ~50% de probabilidades de ganar
# La cantidad de tiradas queda definida si el capital es finito por la bancarrota y
# si es infinito por TCL

# Argumentos (vienen de la consola)
# cantidad_corridas = 30
# cantidad_tiradas = 0
# tipo_jugada = 'r' # Rojo
# estrategia = 'o'
# capital = 'f'

# Ejecucion de la estrategia martingala
def estrategia_martingala(tipo_jugada, tirada, capital, apuesta, APUESTA_INICIAL):
    gano, beneficio = apostar(tipo_jugada, tirada)
    if gano:
        capital += (apuesta * beneficio)
        apuesta = APUESTA_INICIAL
    else:
        capital -= apuesta
        apuesta *= 2
    
    return (gano ,capital, apuesta)

# Ejecucion de la estrategia d'alembert
def estrategia_dalembert(tipo_jugada, tirada, capital, apuesta, APUESTA_INICIAL):
    gano, beneficio = apostar(tipo_jugada, tirada)
    if gano:
        capital += (apuesta * beneficio)
        apuesta -= 0 if apuesta == APUESTA_INICIAL else 1
    else:
        capital -= apuesta
        apuesta += 1

    return (gano, capital, apuesta)

# Ejecucion de la estrategia fibonacci
def estrategia_fibonacci(tipo_jugada, tirada, capital, apuesta, apuesta_anterior, APUESTA_INICIAL):
    gano, beneficio = apostar(tipo_jugada, tirada)
    if gano:
        capital += (apuesta * beneficio)
        nueva_apuesta = APUESTA_INICIAL if apuesta == APUESTA_INICIAL else apuesta - apuesta_anterior
        apuesta_anterior = APUESTA_INICIAL if apuesta == APUESTA_INICIAL else apuesta_anterior - nueva_apuesta
    else:
        capital -= apuesta
        nueva_apuesta = apuesta_anterior + apuesta
        apuesta_anterior = apuesta
    apuesta = nueva_apuesta

    return (gano, capital, apuesta, apuesta_anterior)

# Ejecucion de la estrategia paroli
def estrategia_paroli(tipo_jugada, tirada, capital, apuesta, victorias_consecutivas, APUESTA_INICIAL):
    gano, beneficio = apostar(tipo_jugada, tirada)
    if gano:
        victorias_consecutivas += 1
        capital += (apuesta * beneficio)
        if victorias_consecutivas < 3:
            apuesta *= 2
        else:
            victorias_consecutivas = 0
            apuesta = APUESTA_INICIAL
    else:
        capital -= apuesta
        victorias_consecutivas = 0
        apuesta = APUESTA_INICIAL
    
    return (gano, capital, apuesta, victorias_consecutivas)

def finalizar_capital_infinito(promedio_frecuencia_relativa, probabilidad):
    if len(promedio_frecuencia_relativa) < 1000:
        return False
    elif abs(mean(promedio_frecuencia_relativa[:-100]) - probabilidad) < 0.05:
        return True

def simular_corridas(cantidad_corridas, cantidad_tiradas, tipo_jugada, estrategia, capital):
    CAPITAL_INICIAL = float('inf') if capital == Capital.INFINITO else 200
    APUESTA_INICIAL = 1

    for c in range(cantidad_corridas):
        print('\nCorrida: ', c, '\n')
        promedio_frecuencia_relativa = []
        capital = CAPITAL_INICIAL
        apuesta = APUESTA_INICIAL
        flujo_caja = [CAPITAL_INICIAL]
        f_relativa_apuesta_favorable = []
        cantidad_apostada_por_tirada = [apuesta]
        cantidad_tiradas = 0
        cantidad_ganadas = 0

        if estrategia == Estrategia.MARTINGALA:
            while capital > 0:
                cantidad_tiradas += 1
                tirada = random.choice(RULETA)
                gano, capital, apuesta = estrategia_martingala(tipo_jugada, tirada, capital, apuesta, APUESTA_INICIAL)
                cantidad_ganadas += 1 if gano else 0
                f_relativa_apuesta_favorable.append(cantidad_ganadas / cantidad_tiradas)
                promedio_frecuencia_relativa.append(mean(f_relativa_apuesta_favorable))
                cantidad_apostada_por_tirada.append(apuesta)
                flujo_caja.append(capital)
                print('Tirada: ', cantidad_tiradas, 'Capital: ', capital, 'Apuesta: ', apuesta)
                # Si el capital es infinito, verifica la condicion de finalizacion en cada iteracion
                if capital_elegido == Capital.INFINITO:
                    terminar_ejecucion = finalizar_capital_infinito(promedio_frecuencia_relativa, PROBABILIDAD[tipo_jugada] if tipo_jugada in PROBABILIDAD else PROBABILIDAD[Jugada.PLENO])
                    if terminar_ejecucion: break

        elif estrategia == Estrategia.DALEMBERT:
            while capital > 0:
                cantidad_tiradas += 1
                tirada = random.choice(RULETA)
                gano, capital, apuesta = estrategia_dalembert(tipo_jugada, tirada, capital, apuesta, APUESTA_INICIAL)
                cantidad_ganadas += 1 if gano else 0
                f_relativa_apuesta_favorable.append(cantidad_ganadas / cantidad_tiradas)
                promedio_frecuencia_relativa.append(mean(f_relativa_apuesta_favorable))
                cantidad_apostada_por_tirada.append(apuesta)
                flujo_caja.append(capital)
                print('Tirada: ', cantidad_tiradas, 'Capital: ', capital, 'Apuesta: ', apuesta)
                # Si el capital es infinito, verifica la condicion de finalizacion en cada iteracion
                if capital_elegido == Capital.INFINITO:
                    terminar_ejecucion = finalizar_capital_infinito(promedio_frecuencia_relativa, PROBABILIDAD[tipo_jugada] if tipo_jugada in PROBABILIDAD else PROBABILIDAD[Jugada.PLENO])
                    if terminar_ejecucion: break

        elif estrategia == Estrategia.FIBONACCI:
            apuesta_anterior = APUESTA_INICIAL
            while capital > 0:
                cantidad_tiradas += 1
                tirada = random.choice(RULETA)
                gano, capital, apuesta, apuesta_anterior = estrategia_fibonacci(tipo_jugada, tirada, capital, apuesta,
                                                                                apuesta_anterior, APUESTA_INICIAL)
                cantidad_ganadas += 1 if gano else 0
                f_relativa_apuesta_favorable.append(cantidad_ganadas / cantidad_tiradas)
                promedio_frecuencia_relativa.append(mean(f_relativa_apuesta_favorable))
                cantidad_apostada_por_tirada.append(apuesta)
                flujo_caja.append(capital)
                print('Tirada: ', cantidad_tiradas, 'Capital: ', capital, 'Apuesta: ', apuesta)
                # Si el capital es infinito, verifica la condicion de finalizacion en cada iteracion
                if capital_elegido == Capital.INFINITO:
                    terminar_ejecucion = finalizar_capital_infinito(promedio_frecuencia_relativa, PROBABILIDAD[tipo_jugada] if tipo_jugada in PROBABILIDAD else PROBABILIDAD[Jugada.PLENO])
                    if terminar_ejecucion: break

        elif estrategia == Estrategia.OTRA:
            victorias_consecutivas = 0
            while capital > 0:
                cantidad_tiradas += 1
                tirada = random.choice(RULETA)
                gano, capital, apuesta, victorias_consecutivas = estrategia_paroli(tipo_jugada, tirada, capital,
                                                                                   apuesta, victorias_consecutivas,
                                                                                   APUESTA_INICIAL)
                cantidad_ganadas += 1 if gano else 0
                f_relativa_apuesta_favorable.append(cantidad_ganadas / cantidad_tiradas)
                promedio_frecuencia_relativa.append(mean(f_relativa_apuesta_favorable))
                cantidad_apostada_por_tirada.append(apuesta)
                flujo_caja.append(capital)
                print('Tirada: ', cantidad_tiradas, 'Capital: ', capital, 'Apuesta: ', apuesta)
                # Si el capital es infinito, verifica la condicion de finalizacion en cada iteracion
                if capital_elegido == Capital.INFINITO:
                    terminar_ejecucion = finalizar_capital_infinito(promedio_frecuencia_relativa, PROBABILIDAD[tipo_jugada] if tipo_jugada in PROBABILIDAD else PROBABILIDAD[Jugada.PLENO])
                    if terminar_ejecucion: break

        # Se realizan graficas
        grafica_flujo_caja(flujo_caja, cantidad_tiradas, CAPITAL_INICIAL)
        grafica_frecuencias_apuestas_favorables(f_relativa_apuesta_favorable, cantidad_tiradas, PROBABILIDAD[tipo_jugada] if tipo_jugada in PROBABILIDAD else PROBABILIDAD[Jugada.PLENO])
        grafica_promedio_frecuencias_relativas(promedio_frecuencia_relativa, cantidad_tiradas)
        grafica_apuestas(cantidad_apostada_por_tirada, cantidad_tiradas)

    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simulación de ruleta')
    parser.add_argument('-n', type=int, help='Cantidad de tiradas', required=True)
    parser.add_argument('-c', type=int, help='Cantidad de corridas', required=True)
    parser.add_argument('-e', choices=list(JUGADAS).extend([range(37)]), help="Tipo de jugada: ej: 10 --> Pleno 'r' --> Rojo 'n' --> Negro 'e' --> Par "
                                            "'o' --> Impar 'd1' --> Docena 1 'd2' --> Docena 2 "
                                            "'d3' --> Docena 3 'f1' --> Fila 1 'f2' --> Fila 2 "
                                            "'f3' --> Fila 3 'a' --> Altos 'b' --> Bajos", required=True)
    parser.add_argument('-s', choices=list(ESTRATEGIAS), type=str, help="Estrategia utilizada : 'm' --> Martingala"
                                                            "'d' --> D Alembert 'f' --> Fibonacci 'o' --> Paroli", required=True)
    parser.add_argument('-a', choices=list(CAPITALES), type=str, help="Tipo de capital: 'f' --> finito 'i' --> infinito", required=True)
    args = parser.parse_args()

    cantidad_tiradas = args.n
    cantidad_corridas = args.c
    tipo_jugada = args.e
    estrategia = args.s
    capital_elegido = args.a
    veces_capital_agotado = 0

    # Creacion ventanas
    creacion_ventanas()

    simular_corridas(args.c, args.n, args.e, args.s, args.a)