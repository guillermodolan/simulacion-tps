import math
import random as rdm
from matplotlib import pyplot as plt

def readInt(ingresar):
    while True:
        entrada = input(ingresar)
        try:
            entrada = int(entrada)
            return entrada
        except ValueError:
            print("La entrada es incorrecta: escribe un numero entero")

def readFloat(ingresar):
    while True:
        entrada = input(ingresar)
        try:
            entrada = float(entrada)
            return entrada
        except ValueError:
            print("La entrada es incorrecta: escribe un numero real")

def mostrarMenu():
    print("\nMenu")
    print("Seleccione una opción:")
    print("\t1. Modelo MM1")
    print("\t2. Modelo de inventarios")
    print("\n\t0. Salir")

def menu():
    opcion = -1
    while opcion != 0:
        mostrarMenu()
        opcion = int(input("\nIngrese su opción: ") or -1)
        if opcion == 1:
            print("\n1. MM1")
            ejecutar_mm1()
        elif opcion == 2:
            print("\n2. Inventario")
            ejecutar_inventario()

        elif opcion == 0:
            print("\nFin de aplicativo de simulación.")
        else:
            print("\nOpcion incorrecta!")


# -------------------------------------- MM1 --------------------------------------

def ejecutar_mm1():
    class SingleServerQueueing:
        IDLE = 0
        BUSY = 1

        n_queue_overflow = 0
        num_custs_delayed = 0
        total_of_delays_in_system = 0
        total_of_delays_in_q = 0
        area_num_in_system = 0
        area_num_in_q = 0
        area_server_status = 0
        time_n_custs_in_q = list()
        sum_probability_refusal_service = 0
        time = 0

        def __init__(self, mean_interarrival, mean_service, num_delays_required, q_limit, n_run):
            if n_run == 1:
                SingleServerQueueing.time_n_custs_in_q = [0] * (q_limit + 2)

            # Specify parameters
            self.mean_interarrival = mean_interarrival
            self.mean_service = mean_service
            self.num_delays_required = num_delays_required
            self.q_limit = q_limit
            self.n_run = n_run

            # Specify the number of events for the timing function
            self.num_events = 2

        def initializationRoutine(self):
            # Initialize the simulation clock
            self.time = 0

            # Initialize the variables
            self.server_status = SingleServerQueueing.IDLE
            self.num_in_system = 0
            self.num_in_q = 0
            self.time_last_event = 0
            self.num_custs_entered = 0
            self.num_custs_delayed = 0
            self.total_of_delays_in_system = 0
            self.total_of_delays_in_q = 0
            self.area_num_in_system = 0
            self.area_num_in_q = 0
            self.area_server_status = 0
            self.overflowing_queue = False
            self.probability_refusal_service = 0

            # Initialize lists
            self.time_next_event = [0] * (self.num_events + 1)
            self.time_arrival = [0] * (self.q_limit + 2)
            self.time_arrival_q = [0] * (self.q_limit + 1)
            self.time_n_custs_in_q = [0] * (self.q_limit + 1)

            # Initialize graph list
            self.custs_in_system_graph_x = list()
            self.custs_in_system_graph_y = list()
            self.custs_in_q_graph_x = list()
            self.custs_in_q_graph_y = list()
            self.server_utilization_graph_x = list()
            self.server_utilization_graph_y = list()

            self.custs_in_system_graph_x.append(self.time)
            self.custs_in_system_graph_y.append(0)
            self.custs_in_q_graph_x.append(self.time)
            self.custs_in_q_graph_y.append(0)
            self.server_utilization_graph_x.append(self.time)
            self.server_utilization_graph_y.append(0)

            # Initialize event list
            self.time_next_event[1] = math.inf
            self.time_next_event[2] = self.time + SingleServerQueueing.expon(self.mean_interarrival)
            self.empty_event_list = False

        def timingRoutine(self):
            min_time_next_event = math.inf
            self.next_event_type = 0

            # Determine the event type of the next event to occur
            for i in range(self.num_events):
                i += 1
                if self.time_next_event[i] < min_time_next_event:
                    min_time_next_event = self.time_next_event[i]
                    self.next_event_type = i

            # Check to see whether the event list is empty
            if self.next_event_type == 0:
                # The event list is empty, so stop the simulation
                print("Lista de eventos vacía en el tiempo: " + str(self.time))
                self.empty_event_list = True

            # The event list is not empty, so advance the simulation clock
            self.time = min_time_next_event

        def updateTimeAvgStats(self):
            # Compute time since last event, and update last-event-time marker
            time_since_last_event = self.time - self.time_last_event
            self.time_last_event = self.time

            # Update area under number-in-system function
            SingleServerQueueing.area_num_in_system += self.num_in_system * time_since_last_event
            self.area_num_in_system += self.num_in_system * time_since_last_event

            # Update area under number-in-queue function
            SingleServerQueueing.area_num_in_q += self.num_in_q * time_since_last_event
            self.area_num_in_q += self.num_in_q * time_since_last_event

            # Update area under server-busy indicator function
            SingleServerQueueing.area_server_status += self.server_status * time_since_last_event
            self.area_server_status += self.server_status * time_since_last_event

            # Update time number of custs in q
            SingleServerQueueing.time_n_custs_in_q[self.num_in_q] += time_since_last_event
            self.time_n_custs_in_q[self.num_in_q] += time_since_last_event

        def updateGraphs(self):
            # Update custs_in_system_graph
            self.custs_in_system_graph_x.append(self.time)
            self.custs_in_system_graph_y.append(self.num_in_system)

            # Update custs_in_q_graph
            self.custs_in_q_graph_x.append(self.time)
            self.custs_in_q_graph_y.append(self.num_in_q)

            # Update server_utilization_graph
            self.server_utilization_graph_x.append(self.time)
            if self.server_status == SingleServerQueueing.IDLE:
                self.server_utilization_graph_y.append(0)
            elif self.server_status == SingleServerQueueing.BUSY:
                self.server_utilization_graph_y.append(1)

        def arrive(self):
            # Schedule next arrival
            self.time_next_event[2] = self.time + SingleServerQueueing.expon(self.mean_interarrival)

            # Check to see whether server is busy
            if self.server_status == SingleServerQueueing.BUSY:
                # Server is busy, so increment number of customers in queue
                self.num_in_q += 1

                # Check to see whether an overflow condition exists
                if self.num_in_q > self.q_limit:
                    # The queue has overflowed, so stop the simulation
                    print("Desbordamiento de la longitud de la cola en el tiempo: " + str(self.time))
                    self.overflowing_queue = True
                    self.probability_refusal_service = 1 / (self.num_custs_entered + 1)
                    SingleServerQueueing.sum_probability_refusal_service += self.probability_refusal_service
                    return

                # Store the time of arrival of the arriving customer at the (new) end of time_arrival_q
                self.time_arrival_q[self.num_in_q] = self.time
            elif self.server_status == SingleServerQueueing.IDLE:
                # Server is idle, so arriving customer has a delay in q of zero
                delay = 0
                SingleServerQueueing.total_of_delays_in_q += delay
                self.total_of_delays_in_q += delay

                # Increment the number of customers delayed, and make server busy
                SingleServerQueueing.num_custs_delayed += 1
                self.num_custs_delayed += 1
                self.server_status = SingleServerQueueing.BUSY

                # Schedule a departure
                self.time_next_event[1] = self.time + SingleServerQueueing.expon(self.mean_service)

            # Increment number of customers
            self.num_custs_entered += 1
            self.num_in_system += 1

            # Store the time of arrival of the arriving customer at the (new) end of time_arrival
            self.time_arrival[self.num_in_system] = self.time

        def depart(self):
            # Decrement the number of customers in the system
            self.num_in_system -= 1

            # Compute the delay of the customer who departed and update the total delay in system accumulator
            delay = self.time - self.time_arrival[1]
            SingleServerQueueing.total_of_delays_in_system += delay
            self.total_of_delays_in_system += delay

            # Move each customer in system up one place
            for i in range(self.num_in_system):
                i += 1
                self.time_arrival[i] = self.time_arrival[i + 1]

            # Check to see whether the queue is empty
            if self.num_in_q == 0:
                # The queue is empty so make the server idle and eliminate the departure event from consideration
                self.server_status = SingleServerQueueing.IDLE
                self.time_next_event[1] = math.inf
            elif self.num_in_q > 0:
                # The queue is nonempty, so decrement the number of customers in queue
                self.num_in_q -= 1

                # Compute the delay of the customer who is beginning service and update the total delay in q accumulator
                delay = self.time - self.time_arrival_q[1]
                SingleServerQueueing.total_of_delays_in_q += delay
                self.total_of_delays_in_q += delay

                # Increment the number of customers delayed, and schedule departure
                SingleServerQueueing.num_custs_delayed += 1
                self.num_custs_delayed += 1
                self.time_next_event[1] = self.time + SingleServerQueueing.expon(self.mean_service)

                # Move each customer in queue up one place
                for i in range(self.num_in_q):
                    i += 1
                    self.time_arrival_q[i] = self.time_arrival_q[i + 1]

        @staticmethod
        def expon(mean):
            # Generate a U(0,1) random variate
            u = rdm.uniform(0, 1)

            # Return an exponential random variate with mean "mean"
            return -mean * math.log(u)

        @staticmethod
        def makeGraph(x, y, title, y_label, name):
            plt.figure(figsize=(10, 6))
            plt.plot(x, y, "r-")
            plt.title(title)
            plt.xlabel("t (tiempo)")
            plt.ylabel(y_label)
            plt.grid()
            plt.fill_between(x, y, color='red')
            mng = plt.get_current_fig_manager()
            mng.window.state('zoomed')
            # plt.savefig('./graficos/' + name + '.jpg')
            plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.1)
            plt.show()

        def reportGenerator(self):
            if self.n_run == 1:
                # Compute and write estimates of desired measures of performance
                print("Tiempo medio entre arribos en minutos: " + str(self.mean_interarrival))
                print("Tiempo medio de servicio en minutos: " + str(self.mean_service))
                print("La tasa de arribos es " + str(((1/self.mean_interarrival) / (1/self.mean_service)) * 100) + "% de la tasa de servicio")
                print("Numero de demoras requeridas: " + str(self.num_delays_required))
                print("Numero de demoras: " + str(self.num_custs_delayed))
                print("Demora promedio en el sistema en minutos: " + str(self.total_of_delays_in_system / self.num_custs_delayed))
                print("Demora promedio en cola en minutos: " + str(self.total_of_delays_in_q / self.num_custs_delayed))
                print("Numero promedio de clientes en el sistema: " + str(self.area_num_in_system / self.time))
                print("Numero promedio de clientes en cola: " + str(self.area_num_in_q / self.time))
                print("Utilizacion promedio del servicio: " + str(self.area_server_status / self.time))
                print("Probabilidad de n clientes en cola")
                i = 0
                while i <= self.q_limit:
                    print("Probabilidad de " + str(i) + " clientes en cola: " + str(self.time_n_custs_in_q[i] / self.time))
                    i += 1
                print("Probabilidad de denegación de servicio con una cola de tamaño " + str(self.q_limit) + ": " + str(self.probability_refusal_service))
                print("Tiempo de finalizacion de la simulacion: " + str(self.time))

                SingleServerQueueing.makeGraph(self.custs_in_system_graph_x, self.custs_in_system_graph_y,
                                               f'Clientes en el sistema con tiempo medio entre arribos: ' +
                                               str(mean_interarrival) + f'\n, tiempo medio de servicio: ' +
                                               str(mean_service) + f'\n y limite de cola: ' + str(q_limit) +
                                               f'\n - Numero promedio de clientes en el sistema: ' +
                                               str(self.area_num_in_system / self.time),
                                               'Clientes en el sistema', 'S(t) - ' + str(mean_interarrival)
                                               + ' - ' + str(mean_service) + ' - ' + str(q_limit))


                SingleServerQueueing.makeGraph(self.custs_in_q_graph_x, self.custs_in_q_graph_y,
                                               f'\n Clientes en cola con tiempo medio entre arribos: '
                                               + str(mean_interarrival) + f'\n, tiempo medio de servicio: '
                                               + str(mean_service) + f'\n y limite de cola: ' + str(q_limit)
                                               + f'\n - Numero promedio de clientes en cola: '
                                               + str(self.area_num_in_q / self.time),
                                               'Clientes en cola', 'Q(t) - ' + str(mean_interarrival) + ' - '
                                               + str(mean_service) + ' - ' + str(q_limit))


                SingleServerQueueing.makeGraph(self.server_utilization_graph_x,
                                               self.server_utilization_graph_y,
                                               f'\n Utilizacion del servicio con tiempo medio entre arribos: '
                                               + str(mean_interarrival) + f'\n, tiempo medio de servicio: '
                                               + str(mean_service) + f'\n y limite de cola: ' + str(q_limit)
                                               + f'\n - Utilizacion promedio del servicio: '
                                               + str(self.area_server_status / self.time),
                                               'Utilización del servidor', 'B(t) - ' + str(mean_interarrival) + ' - '
                                               + str(mean_service) + ' - ' + str(q_limit))



        # Main program
        def start(self):
            print("\n\nCorrida numero: " + str(self.n_run) + "\n")

            # Initialize the simulation
            self.initializationRoutine()

            # Run the simulation while more delays are still needed
            while self.num_custs_delayed < self.num_delays_required:
                # Determine the next event
                self.timingRoutine()
                if self.empty_event_list:
                    break

                # Update time-average statistical accumulators
                self.updateTimeAvgStats()

                # Update graphs before event
                self.updateGraphs()

                # Invoke the appropriate event function
                if self.next_event_type == 1:
                    self.depart()
                elif self.next_event_type == 2:
                    self.arrive()
                    if self.overflowing_queue:
                        break

                # Update graphs after event
                self.updateGraphs()

            # Add the time to the total time
            SingleServerQueueing.time += self.time

            # Invoke the report generator and end the simulation
            self.reportGenerator()


    mean_interarrival = readFloat("Ingrese el tiempo promedio entre arribos en minutos: ")
    mean_service = readFloat("Ingrese el tiempo promedio de servicio en minutos: ")
    num_delays_required = readInt("Ingrese el numero de demoras requeridas: ")
    q_limit = readInt("Ingrese el tamaño de la cola: ")
    n_runs = readInt("Ingrese el numero de corridas: ")

    for i in range(n_runs):
        i += 1
        singleServerQueueing = SingleServerQueueing(mean_interarrival, mean_service, num_delays_required, q_limit, i)
        singleServerQueueing.start()

    print("\n\nValores promedio en " + str(n_runs) + " corridas\n")
    print("Tiempo medio entre arribos en minutos: " + str(mean_interarrival))
    print("Tiempo medio de servicio en minutos: " + str(mean_service))
    print("La tasa de arribos es " + str(((1/mean_interarrival) / (1/mean_service)) * 100) + "% de la tasa de servicio")
    print("Numero de demoras requeridas: " + str(num_delays_required)) #1000
    print("Numero de demoras promedio en " + str(n_runs) + " corridas: " + str(SingleServerQueueing.num_custs_delayed / n_runs))
    print("Demora en el sistema promedio en " + str(n_runs) + " corridas en minutos: " + str(SingleServerQueueing.total_of_delays_in_system / SingleServerQueueing.num_custs_delayed))
    print("Demora en cola promedio en " + str(n_runs) + " corridas en minutos: " + str(SingleServerQueueing.total_of_delays_in_q / SingleServerQueueing.num_custs_delayed))
    print("Numero de clientes en el sistema promedio en " + str(n_runs) + " corridas: " + str(SingleServerQueueing.area_num_in_system / SingleServerQueueing.time))
    print("Numero de clientes en cola promedio en " + str(n_runs) + " corridas: " + str(SingleServerQueueing.area_num_in_q / SingleServerQueueing.time))
    print("Utilizacion del servicio promedio en " + str(n_runs) + " corridas: " + str(SingleServerQueueing.area_server_status / SingleServerQueueing.time))
    print("Probabilidad de n clientes en cola promedio en " + str(n_runs) + " corridas")
    i = 0
    while i <= q_limit:
        print("Probabilidad de " + str(i) + " clientes en cola promedio en " + str(n_runs) + " corridas: " + str(SingleServerQueueing.time_n_custs_in_q[i] / SingleServerQueueing.time))
        i += 1
    print("Tiempo de finalizacion de la simulacion promedio en " + str(n_runs) + " corridas: " + str(SingleServerQueueing.time / n_runs))
    print("Probabilidad de denegación de servicio con una cola de tamaño " + str(q_limit) + " y " + str(n_runs) + " corridas: " + str(SingleServerQueueing.sum_probability_refusal_service / n_runs))


# -------------------------------------- INVENTORY SYSTEM --------------------------------------

def ejecutar_inventario():
    class InventorySystem:
        total_ordering_cost = 0
        area_holding = 0
        area_shortage = 0

        def __init__(self, initial_inv_level, num_months, mean_interdemand, prob_distrib_demand, setup_cost, incremental_cost, holding_cost, shortage_cost, minlag, maxlag, smalls, bigs, n_run):
            # Specify parameters
            self.initial_inv_level = initial_inv_level
            self.num_months = num_months
            self.mean_interdemand = mean_interdemand
            self.prob_distrib_demand = prob_distrib_demand
            self.setup_cost = setup_cost
            self.incremental_cost = incremental_cost
            self.holding_cost = holding_cost
            self.shortage_cost = shortage_cost
            self.minlag = minlag
            self.maxlag = maxlag
            self.smalls = smalls
            self.bigs = bigs
            self.n_run = n_run

            # Specify the number of events for the timing function
            self.num_events = 4

        def initializationRoutine(self):
            # Initialize the simulation clock
            self.time = 0

            # Initialize the variables
            self.inv_level = self.initial_inv_level
            self.time_last_event = 0
            self.total_ordering_cost = 0
            self.area_holding = 0
            self.area_shortage = 0

            # Initialize lists
            self.time_next_event = [0] * (self.num_events + 1)

            # Initialize graph list
            self.inventory_graph_x = list()
            self.inventory_graph_y = list()
            self.ordering_cost_graph_x = list()
            self.ordering_cost_graph_y = list()
            self.holding_cost_graph_x = list()
            self.holding_cost_graph_y = list()
            self.shortage_cost_graph_x = list()
            self.shortage_cost_graph_y = list()
            self.s_graph_x = list()
            self.s_graph_y = list()
            self.S_graph_x = list()
            self.S_graph_y = list()

            self.inventory_graph_x.append(self.time)
            self.inventory_graph_y.append(self.initial_inv_level)
            self.ordering_cost_graph_x.append(self.time)
            self.ordering_cost_graph_y.append(0)
            self.holding_cost_graph_x.append(self.time)
            self.holding_cost_graph_y.append(0)
            self.shortage_cost_graph_x.append(self.time)
            self.shortage_cost_graph_y.append(0)
            self.s_graph_x.append(-0.1)
            self.s_graph_y.append(self.smalls)
            self.s_graph_x.append(0.1)
            self.s_graph_y.append(self.smalls)
            self.S_graph_x.append(-0.1)
            self.S_graph_y.append(self.bigs)
            self.S_graph_x.append(0.1)
            self.S_graph_y.append(self.bigs)

            # Initialize event list
            self.time_next_event[1] = math.inf
            self.time_next_event[2] = self.time + InventorySystem.expon(self.mean_interdemand)
            self.time_next_event[3] = self.num_months
            self.time_next_event[4] = 0
            self.empty_event_list = False

        def timingRoutine(self):
            min_time_next_event = math.inf
            self.next_event_type = 0

            # Determine the event type of the next event to occur
            for i in range(self.num_events):
                i += 1
                if self.time_next_event[i] < min_time_next_event:
                    min_time_next_event = self.time_next_event[i]
                    self.next_event_type = i

            # Check to see whether the event list is empty
            if self.next_event_type == 0:
                # The event list is empty, so stop the simulation
                print("Lista de eventos vacía en el tiempo: " + str(self.time))
                self.empty_event_list = True

            # The event list is not empty, so advance the simulation clock
            self.time = min_time_next_event

        def updateTimeAvgStats(self):
            # Compute time since last event, and update last-event-time marker
            time_since_last_event = self.time - self.time_last_event
            self.time_last_event = self.time

            # Determine the status of the inventory level during the previous interval
            if self.inv_level < 0:
                InventorySystem.area_shortage -= self.inv_level * time_since_last_event
                self.area_shortage -= self.inv_level * time_since_last_event
            elif self.inv_level > 0:
                InventorySystem.area_holding += self.inv_level * time_since_last_event
                self.area_holding += self.inv_level * time_since_last_event

        def updateGraphs(self):
            # Update inventory_graph
            self.inventory_graph_x.append(self.time)
            self.inventory_graph_y.append(self.inv_level)

            # Update ordering_cost_graph
            self.ordering_cost_graph_x.append(self.time)
            self.ordering_cost_graph_y.append(self.total_ordering_cost)

            # Update holding_cost_graph
            self.holding_cost_graph_x.append(self.time)
            self.holding_cost_graph_y.append(self.area_holding * self.holding_cost)

            # Update shortage_cost_graph
            self.shortage_cost_graph_x.append(self.time)
            self.shortage_cost_graph_y.append(self.area_shortage * self.shortage_cost)

        def orderArrival(self):
            # Increment the inventory level by the amount ordered
            self.inv_level += self.amount

            # Since no order is now outstanding, eliminate the order-arrival event from consideration
            self.time_next_event[1] = math.inf

        def demand(self):
            # Generate the demand size
            size_demand = InventorySystem.randomInteger(self.prob_distrib_demand)

            # Decrement the inventory level by the demand size
            self.inv_level -= size_demand

            # Schedule the time of the next demand
            self.time_next_event[2] = self.time + InventorySystem.expon(self.mean_interdemand)

        def evaluate(self):
            # Check whether the inventory level is less than smalls
            if self.inv_level < self.smalls:
                # The inventory level is less than smalls, so place an order for the appropriate amount
                self.amount = self.bigs - self.inv_level
                InventorySystem.total_ordering_cost += self.setup_cost + self.incremental_cost * self.amount
                self.total_ordering_cost += self.setup_cost + self.incremental_cost * self.amount

                # Schedule the arrival of the order
                self.time_next_event[1] = self.time + InventorySystem.uniform(self.minlag, self.maxlag)

            self.time_next_event[4] = self.time + 1

        @staticmethod
        def uniform(a, b):
            # Generate a U(0,1) random variate
            u = rdm.uniform(0, 1)

            # Return an uniform random variate
            return a + (b - a) * u

        @staticmethod
        def expon(mean):
            # Generate a U(0,1) random variate
            u = rdm.uniform(0, 1)

            # Return an exponential random variate with mean "mean"
            return -mean * math.log(u)

        @staticmethod
        def randomInteger(prob_distrib):
            # Generate a U(0,1) random variate
            u = rdm.uniform(0, 1)

            # Return a random integer in accordance with the (cumulative) distribution function prob_distrib
            i = 1
            while u >= prob_distrib[i]:
                i += 1
            return i

        @staticmethod
        def makeGraph(x, y, colour, label):
            plt.plot(x, y, colour, label=label)

        def showGraph(self):
            plt.title("Nivel de inventario y costos con s=" + str(self.smalls) + " y S=" + str(self.bigs))
            plt.xlabel("m (meses)")
            plt.ylabel("I (nivel de inventario)")
            plt.legend(loc=1)
            plt.grid()
            mng = plt.get_current_fig_manager()
            mng.window.state('zoomed')
            # plt.savefig('./images_m_m_1(' + str(self.smalls) + ", " + str(self.bigs) + ').jpg')
            plt.show()

        def reportGenerator(self):
            if self.n_run == 1:
                # Compute and write estimates of desired measures of performance
                avg_ordering_cost = self.total_ordering_cost / self.num_months
                avg_holding_cost = (self.holding_cost * self.area_holding) / self.num_months
                avg_shortage_cost = (self.shortage_cost * self.area_shortage) / self.num_months
                print("Inventory policy: (s = " + str(self.smalls) + ", S = " + str(self.bigs) + ")")
                print("Costo promedio de pedido por mes: " + str(avg_ordering_cost))
                print("Costo promedio de mantenimiento por mes: " + str(avg_holding_cost))
                print("Costo promedio de escasez por mes: " + str(avg_shortage_cost))
                print("Costo total promedio por mes: " + str(avg_ordering_cost + avg_holding_cost + avg_shortage_cost))

                InventorySystem.makeGraph(self.s_graph_x, self.s_graph_y, 'r-', 's')

                InventorySystem.makeGraph(self.S_graph_x, self.S_graph_y, 'r-', 'S')

                InventorySystem.makeGraph(self.inventory_graph_x, self.inventory_graph_y, 'r-',
                                          'Inventario')
                InventorySystem.makeGraph(self.ordering_cost_graph_x, self.ordering_cost_graph_y, 
                                          'y-', 'Costo de pedido')
                
                InventorySystem.makeGraph(self.holding_cost_graph_x, self.holding_cost_graph_y, 
                                          'g-', 'Costo de mantenimiento')
                InventorySystem.makeGraph(self.shortage_cost_graph_x, self.shortage_cost_graph_y, 
                                          'b-', 'Costo de escasez')
                self.showGraph()

        # Main program
        def start(self):
            print("\n\nCorrida numero: " + str(self.n_run) + "\n")

            # Initialize the simulation
            self.initializationRoutine()

            # Run the simulation while more delays are still needed
            while True:
                # Determine the next event
                self.timingRoutine()
                if self.empty_event_list:
                    break

                # Update time-average statistical accumulators
                self.updateTimeAvgStats()

                # Update graphs before event
                self.updateGraphs()

                # Invoke the appropriate event function
                if self.next_event_type == 1:
                    self.orderArrival()
                elif self.next_event_type == 2:
                    self.demand()
                elif self.next_event_type == 4:
                    self.evaluate()
                elif self.next_event_type == 3:
                    # Invoke the report generator and end the simulation
                    self.reportGenerator()
                    break

                # Update graphs after event
                self.updateGraphs()


    initial_inv_level = readInt("Ingrese el nivel de inventario inicial: ") #60
    num_months = readInt("Ingrese la cantidad de meses: ") #120
    mean_interdemand = readFloat("Ingrese el tiempo promedio entre demandas en meses: ") #0.1
    print("Ingrese la probabilidad acumulada de demanda de n items")
    prob_distrib_demand = list()  #1 2 3 4
    prob_distrib_demand.append(0)
    i = 1
    probability = 0
    while probability != 1:
        while True:
            probability = readFloat("Ingrese la probabilidad acumulada de solicitar " + str(i) + " items por demanda: ")  #0.16666 0.5 0.83333 1
            if probability > 1:
                print("La probabilidad acumulada no puede ser mayor que 1")
            elif probability < prob_distrib_demand[i - 1]:
                print("La probabilidad acumulada debe ser mayor o igual que " + str(prob_distrib_demand[i-1]))
            else:
                prob_distrib_demand.append(probability)
                i += 1
                break
    setup_cost = readFloat("Ingrese el costo fijo de pedido: ") #32
    incremental_cost = readFloat("Ingrese el costo por item pedido: ") #3
    holding_cost = readFloat("Ingrese el costo de mantenimiento por item por mes: ") #1
    shortage_cost = readFloat("Ingrese el costo de escasez por item por mes: ") #5
    minlag = readFloat("Ingrese la demora minima de arribo de un pedido en meses: ") #0.5
    maxlag = readFloat("Ingrese la demora maxima de arribo de un pedido en meses: ") #1
    n_runs = readInt("Ingrese el numero de corridas: ") #10
    num_policies = readInt("Ingrese el numero de politicas de inventario a analizar: ") #5(minimo)

    for i in range(num_policies):
        i += 1
        print("\n\nPolitica numero " + str(i) + "\n")
        smalls = readInt("Ingrese el punto de pedido: ")
        bigs = readInt("Ingrese la cantidad S de la politica de pedido: ")

        InventorySystem.total_ordering_cost = 0
        InventorySystem.area_holding = 0
        InventorySystem.area_shortage = 0

        for i in range(n_runs):
            i += 1
            inventorySystem = InventorySystem(initial_inv_level, num_months, mean_interdemand, prob_distrib_demand, setup_cost, incremental_cost, holding_cost, shortage_cost, minlag, maxlag, smalls, bigs, i)
            inventorySystem.start()

        print("\n\nValores promedio en " + str(n_runs) + " corridas\n")
        avg_ordering_cost = InventorySystem.total_ordering_cost / (num_months * n_runs)
        avg_holding_cost = (holding_cost * InventorySystem.area_holding) / (num_months * n_runs)
        avg_shortage_cost = (shortage_cost * InventorySystem.area_shortage) / (num_months * n_runs)
        print("Inventory policy: (s = " + str(smalls) + ", S = " + str(bigs) + ")")
        print("Costo promedio de pedido por mes en " + str(n_runs) + " corridas: " + str(avg_ordering_cost))
        print("Costo promedio de mantenimiento por mes en " + str(n_runs) + " corridas: " + str(avg_holding_cost))
        print("Costo promedio de escasez por mes en " + str(n_runs) + " corridas: " + str(avg_shortage_cost))
        print("Costo total promedio por mes en " + str(n_runs) + " corridas: " + str(avg_ordering_cost + avg_holding_cost + avg_shortage_cost))


if __name__ == "__main__":
    menu()
