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

# def definir_funcion(O):
#     x = O[0]
#     y = O[1]
#     nonlinear_constraint = (x - 1) ** 3 - y + 1
#     linear_constraint = x + y - 2
#     if nonlinear_constraint > 0:
#         penalty1 = 1
#     else:
#         penalty1 = 0
 
#     if linear_constraint > 0:
#         penalty2 = 1
#     else:
#         penalty2 = 0
 
#     z = (1 - x) ** 2 + 100 * (y - x ** 2) ** 2 + penalty1 + penalty2    
#     return z

# funcion_transferencia = definir_funcion
# numero_particulas = 12
# iteraciones = 100
# limites = [(-1, 1), (0, 1)] # [0, 0]
# parametros = [0.5, 1, 2] # w, c1, c2

# pso = PSO(funcion_transferencia, limites, numero_particulas, iteraciones, parametros).evaluar()

# # respuesta = pso.evaluar()

# print(pso[0])