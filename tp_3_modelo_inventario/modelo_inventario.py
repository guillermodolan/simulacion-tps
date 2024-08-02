from enum import Enum
from dataclasses import dataclass
from numpy.random import default_rng
from typing import List, Tuple
import matplotlib.pyplot as plt


class EventType(Enum):
    ARRIBO_PEDIDO = 0
    DEMANDA = 1
    EVALUACION = 2
    FIN_SIMULACION = 3


rng = default_rng()


@dataclass(init=False)
class Sistema:
    # Variables del sistema
    tiempo: float  # Reloj de la simulación
    nivel_inventario: int  # Nivel actual del inventario
    historial_nivel_inventario: List[Tuple[float, int]]  # Historial del nivel de inventario a través del tiempo
    tiempo_proximo_evento: List[float]  # Lista de tiempo de ocurrencia del siguiente evento
    tiempo_ultimo_evento: float  # Tiempo de ocurrencia del último evento
    tipo_proximo_evento: EventType  # Tipo de evento del siguiente evento
    cantidad_ordenada: float

    # Contadores estadísticos
    costo_total_ordenar: float  # Costo total por ordenar nuevas unidades
    area_costo_mantenimiento: float  # Área debajo de la curva de costo por mantenimiento
    area_costo_faltante: float  # Área debajo de la curva de costo por faltante

    @property
    def nivel_inventario(self) -> int:
        return self.historial_nivel_inventario[-1][1]

    @nivel_inventario.setter
    def nivel_inventario(self, value):
        self.historial_nivel_inventario.append((self.tiempo, value))


@dataclass(frozen=True)
class Parametros:
    nivel_inicial_inventario: int  # Nivel inicial de inventario
    tiempo_simulacion: float  # Duración total de la simulación
    limite_inferior_inventario: int  # Límite inferior del inventario
    limite_superior_inventario: int  # Límite superior del inventario
    media_interdemanda: float  # Media de tiempo de llegada de nuevas demandas
    distribucion_prob_demanda: List[float]  # Distribución empírica de la demanda
    tiempo_evaluacion: float  # Intervalo de tiempo entre evaluaciones de inventario
    costo_orden: float  # Costo de realizar un pedido
    costo_orden_por_unidad: float  # Costo incremental de realizar un pedido por cada unidad pedida
    costo_mantenimiento: float  # Costo de mantenimiento
    costo_faltante: float  # Costo de faltante
    demora_min_orden: float  # Tiempo mínimo de demora del pedido
    demora_max_orden: float  # Tiempo máximo de demora del pedido


# def formato_impresion(sistema: Sistema, cadena: str):
#    print("%12f %4du: %s" % (sistema.tiempo, sistema.nivel_inventario, cadena))


def inicializar(params: Parametros) -> Sistema:
    """Inicializa los atributos del sistema."""
    sistema = Sistema()

    sistema.tiempo = 0
    sistema.historial_nivel_inventario = []
    sistema.nivel_inventario = params.nivel_inicial_inventario
    sistema.tiempo_ultimo_evento = 0
    sistema.costo_total_ordenar = 0
    sistema.area_costo_mantenimiento = 0
    sistema.area_costo_faltante = 0

    sistema.tiempo_proximo_evento = [
        float('inf'),
        rng.exponential(params.media_interdemanda),
        params.tiempo_evaluacion,
        params.tiempo_simulacion
    ]

    print(f'{sistema.tiempo, sistema.nivel_inventario} Inicio simulación')

    return sistema


def temporizacion(sistema: Sistema):
    """Determina el próximo tipo de evento y avanza el reloj de la simulación."""
    tiempo_proximo_evento_min, tipo_proximo_evento_min = \
        min((tiempo_evento, tipo_evento) for (tipo_evento, tiempo_evento) in enumerate(sistema.tiempo_proximo_evento))
    sistema.tipo_proximo_evento = EventType(tipo_proximo_evento_min)
    sistema.tiempo = tiempo_proximo_evento_min


def actualizar_estadisticas(sistema: Sistema):
    tiempo_desde_ultimo_evento = sistema.tiempo - sistema.tiempo_ultimo_evento
    sistema.tiempo_ultimo_evento = sistema.tiempo

    if sistema.nivel_inventario < 0:
        sistema.area_costo_faltante -= sistema.nivel_inventario * tiempo_desde_ultimo_evento
    elif sistema.nivel_inventario > 0:
        sistema.area_costo_mantenimiento += sistema.nivel_inventario * tiempo_desde_ultimo_evento


def numero_aleatorio_entre(prob_demanda: List[float]):
    r = rng.random()
    for (idx, prob) in enumerate(prob_demanda):
        if r < prob:
            res = idx
            break
    else:
        res = len(prob_demanda)
    return res + 1


def arribo_pedido(sistema: Sistema):
    """Evento de llegada de un pedido de unidades."""
    # Incrementar el nivel de inventario por la cantidad ordenada.
    sistema.nivel_inventario += sistema.cantidad_ordenada
    # Como no hay pedidos pendientes, eliminar evento de arribo de pedidos.
    sistema.tiempo_proximo_evento[EventType.ARRIBO_PEDIDO.value] = float('inf')
    print(f'{sistema.tiempo, sistema.nivel_inventario} Llegada {sistema.cantidad_ordenada} unidades')


def demanda(sistema: Sistema, params: Parametros):
    """Evento de demanda de productos por parte de un cliente."""
    # Generar el tamaño de la demanda.
    tamaño_demanda = numero_aleatorio_entre(params.distribucion_prob_demanda)
    # Disminuir el nivel de inventario por la cantidad demandada.
    sistema.nivel_inventario -= tamaño_demanda
    # Programar el evento de la próxima demanda.
    sistema.tiempo_proximo_evento[EventType.DEMANDA.value] = sistema.tiempo + rng.exponential(params.media_interdemanda)
    print(f'{sistema.tiempo, sistema.nivel_inventario} Demanda {tamaño_demanda} unidades')



def evaluacion(sistema: Sistema, params: Parametros):
    """Evento de evaluación y reabastecimiento de inventario."""
    # Verificar si el nivel de inventario está por debajo del límite inferior.
    if sistema.nivel_inventario < params.limite_inferior_inventario:
        # El nivel de inventario está por debajo del límite. Realizar un pedido con la cantidad apropiada.
        sistema.cantidad_ordenada = params.limite_superior_inventario - sistema.nivel_inventario
        sistema.costo_total_ordenar += params.costo_orden + params.costo_orden_por_unidad * sistema.cantidad_ordenada
        # Programar el evento de arribo del pedido.
        sistema.tiempo_proximo_evento[EventType.ARRIBO_PEDIDO.value] = sistema.tiempo + rng.uniform(
            params.demora_min_orden, params.demora_max_orden)
    # Programar el evento de la próxima evaluación de inventario.
    sistema.tiempo_proximo_evento[EventType.EVALUACION.value] = sistema.tiempo + params.tiempo_evaluacion
#    formato_impresion(sistema, "Pedido %d unidades" % sistema.cantidad_ordenada)
    print(f'{sistema.tiempo, sistema.nivel_inventario}, Pedido: {sistema.cantidad_ordenada} unidades')


def reporte(sistema: Sistema, params: Parametros):
    costo_promedio_ordenar = sistema.costo_total_ordenar / params.tiempo_simulacion
    costo_promedio_mantenimiento = params.costo_mantenimiento * sistema.area_costo_mantenimiento / params.tiempo_simulacion
    costo_promedio_faltante = params.costo_faltante * sistema.area_costo_faltante / params.tiempo_simulacion
    costo_promedio_total = sum((costo_promedio_ordenar, costo_promedio_mantenimiento, costo_promedio_faltante))
    print("Costo promedio de ordenar: %f" % costo_promedio_ordenar)
    print("Costo promedio de mantenimiento: %f" % costo_promedio_mantenimiento)
    print("Costo promedio de faltante: %f" % costo_promedio_faltante)
    print("Costo promedio total: %f" % costo_promedio_total)


def grafico(sistema: Sistema, params: Parametros):
    plt.axhline(y=params.limite_inferior_inventario, color='royalblue', linestyle='dotted')
    plt.axhline(y=params.limite_superior_inventario, color='royalblue', linestyle='dotted')
    plt.axhline(y=0, color='black')
    x, y = zip(*sistema.historial_nivel_inventario)
    plt.step(x, y, where='post', color='red')
    plt.fill_between(x, y, color='mistyrose', step='post')
    plt.xlabel("Tiempo")
    plt.ylabel("Unidades")
    plt.show()


def main():
    params = Parametros(
        nivel_inicial_inventario=20,
        tiempo_simulacion=90,
        limite_inferior_inventario=15,
        limite_superior_inventario=30,
        media_interdemanda=13.5,
        distribucion_prob_demanda=[1 / 6, 1 / 2, 5 / 6],
        tiempo_evaluacion=30,
        costo_orden=32,
        costo_orden_por_unidad=3,
        costo_mantenimiento=2,
        costo_faltante=20,
        demora_min_orden=15,
        demora_max_orden=30
    )

    sistema = inicializar(params)

    while True:
        temporizacion(sistema)
        actualizar_estadisticas(sistema)

        if sistema.tipo_proximo_evento == EventType.ARRIBO_PEDIDO:
            arribo_pedido(sistema)
        elif sistema.tipo_proximo_evento == EventType.DEMANDA:
            demanda(sistema, params)
        elif sistema.tipo_proximo_evento == EventType.EVALUACION:
            evaluacion(sistema, params)
        elif sistema.tipo_proximo_evento == EventType.FIN_SIMULACION:
            break

    reporte(sistema, params)
    grafico(sistema, params)


if __name__ == "__main__":
    main()
