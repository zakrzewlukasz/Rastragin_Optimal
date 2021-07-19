import random
import math
import uuid
from numpy import cos
from numpy import pi
from numpy.random import randn
from numpy.random import rand
from numpy.random import seed

class Population:
    """
    Model osobnika
    """
    def __init__(self, fitness:
                int = None, _id: int = None):
        """
        :param list init_state: dwuelementowa lista zawierająca początkowe wartości

        """
        self.parameters = []
        self.standard_deviation = []
        self.fitness = fitness
        self._id = _id or uuid.uuid4().hex




    #ta funckja chyba nie tu -> Rastargin
    def objective(self, v):	    
        x, y = v
	    #return -20.0 * exp(-0.2 * sqrt(0.5 * (x**2 + y**2))) - exp(0.5 * (cos(2 * pi * x) + cos(2 * pi * y))) + e + 20
        return 20.0 + x**2 + y**2 - 10*cos(2 * pi * x) - 10*cos(2 * pi * y)
        #return 3*x**8 + 3*y**8 + 8*(x**3)*(y**3)

    def generate(self, number, bounds):
        """
        Wygeneruj ciąg wartości parametrów, ktore są reprezentowane przez liczby rzeczywiste od <-10;10>
        o podanej długości oraz ciąg odchyleń standardowych o tej samej długości.

        """

        self.parameters = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
        self.standard_deviation = rand(len(bounds))


    def calculate_value(self, val):
        """
        Wyznacz przystosowanie osobnika na podstawie jego wektora parametrów.
        Składowe wektora są sortowane i ich kolejność wyznacza trase.

        """
        self.fitness = self.objective(val)    

    def mutation(self):
        """
        Mutacja wektora parametrów oraz wektora odchyleń osobnika
        """
        n = len(self.standard_deviation)
        rand1 = random.normalvariate(0, 1)
        tau = 1/((2*n**(1/2))**(1/2))
        fi = 1/((2 * n) ** (1 / 2))
        for i in range(n):
            rand2 = random.normalvariate(0, 1)
            self.standard_deviation[i] *= math.exp(tau*rand2 + fi*rand1)
            if self.standard_deviation[i] < 0.1:
                self.standard_deviation[i] = 0.1
            rand3 = random.normalvariate(0, self.standard_deviation[i])
            self.parameters[i] += rand3
   
  