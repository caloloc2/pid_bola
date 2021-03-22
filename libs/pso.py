import random
import time, math

class Particle:

    def __init__(self, limites, numero_variables, opcion, fitness_inicial):
        self.limites = limites
        self.opcion = opcion        
        self.posicion_particula = []  # particle position
        self.velocidad_particula = []  # particle velocity
        self.mejor_posicion_local_particula = []  # best position of the particle
        self.fitness_mejor_posicion_local_particula = fitness_inicial  # initial objective function value of the best particle position
        self.fitness_posicion_particula = fitness_inicial  # objective function value of the particle position
        self.numero_variables = numero_variables
 
        for i in range(self.numero_variables):
            self.posicion_particula.append(random.uniform(self.limites[i][0], self.limites[i][1]))  # generate random initial position
            self.velocidad_particula.append(random.uniform(-1, 1))  # generate random initial velocity
 
    def evaluar(self, funcion):
        self.fitness_posicion_particula = funcion(self.posicion_particula)
        if self.opcion == -1:
            if self.fitness_posicion_particula < self.fitness_mejor_posicion_local_particula:
                self.mejor_posicion_local_particula = self.posicion_particula  # update the local best
                self.fitness_mejor_posicion_local_particula = self.fitness_posicion_particula  # update the fitness of the local best
        if self.opcion == 1:
            if self.fitness_posicion_particula > self.fitness_mejor_posicion_local_particula:
                self.mejor_posicion_local_particula = self.posicion_particula  # update the local best
                self.fitness_mejor_posicion_local_particula = self.fitness_posicion_particula  # update the fitness of the local best
 
    def actualizar_velocidad(self, mejor_posicion_global, parametros):
        for i in range(self.numero_variables):
            r1 = random.random()
            r2 = random.random()

            w, c1, c2 = parametros
 
            velocidad_cognitiva = c1 * r1 * (self.mejor_posicion_local_particula[i] - self.posicion_particula[i])
            velocidad_social = c2 * r2 * (mejor_posicion_global[i] - self.posicion_particula[i])
            self.velocidad_particula[i] = w * self.velocidad_particula[i] + velocidad_cognitiva + velocidad_social
 
    def actualizar_posicion(self):
        for i in range(self.numero_variables):
            self.posicion_particula[i] = self.posicion_particula[i] + self.velocidad_particula[i]
 
            # check and repair to satisfy the upper self.limites
            if self.posicion_particula[i] > self.limites[i][1]:
                self.posicion_particula[i] = self.limites[i][1]
            # check and repair to satisfy the lower self.limites
            if self.posicion_particula[i] < self.limites[i][0]:
                self.posicion_particula[i] = self.limites[i][0]

class PSO:

    def __init__(self, funcion, limites, numero_particulas, iteraciones, parametros, opcion = -1, numero_variables = 2):
        self.funcion = funcion
        self.limites = limites
        self.numero_particulas = numero_particulas
        self.iteraciones = iteraciones
        self.numero_variables = numero_variables
        self.__opcion = opcion # -1 miniza funcion - 1 maximiza funcion
        self.__parametros = parametros

        self.fitness_inicial = None
        if (self.__opcion == -1):
            self.fitness_inicial = float("inf")
        if (self.__opcion == 1):
            self.fitness_inicial = -float("inf")
        
        self.__fitness_mejor_posicion_global_particula = self.fitness_inicial
        self.__mejor_posicion_global_particula = []
        

    def evaluar(self):
        enjambre_particulas = []
        for i in range(self.numero_particulas):
            enjambre_particulas.append(Particle(self.limites, self.numero_variables, self.__opcion, self.fitness_inicial))
        A = []

        for i in range(self.iteraciones):
            for j in range(self.numero_particulas):
                enjambre_particulas[j].evaluar(self.funcion)

                if self.__opcion == -1:
                    if enjambre_particulas[j].fitness_posicion_particula < self.__fitness_mejor_posicion_global_particula:
                        self.__mejor_posicion_global_particula = list(enjambre_particulas[j].posicion_particula)
                        self.__fitness_mejor_posicion_global_particula = float(enjambre_particulas[j].fitness_posicion_particula)
                if self.__opcion == 1:
                    if enjambre_particulas[j].fitness_posicion_particula > self.__fitness_mejor_posicion_global_particula:
                        self.__mejor_posicion_global_particula = list(enjambre_particulas[j].posicion_particula)
                        self.__fitness_mejor_posicion_global_particula = float(enjambre_particulas[j].fitness_posicion_particula)
            for j in range(self.numero_particulas):
                enjambre_particulas[j].actualizar_velocidad(self.__mejor_posicion_global_particula, self.__parametros)
                enjambre_particulas[j].actualizar_posicion()

            A.append(self.__fitness_mejor_posicion_global_particula)  # record the best fitness

        return self.__mejor_posicion_global_particula