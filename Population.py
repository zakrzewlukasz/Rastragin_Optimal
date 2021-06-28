import random
import math
from numpy import cos
from numpy import pi
from numpy.random import randn
from numpy.random import rand
from numpy.random import seed

class Invid:
    """
    Model osobnika
    """
    def __init__(self, init_state=None):
        """
        :param list init_state: dwuelementowa lista zawierająca początkowe wartości
        """
        if init_state is None:
            self.param_values = []
            self.odchylenia = []
        else:
            self.param_values, self.odchylenia = init_state
 
        self.value = 0


    def __lt__(self, other):
        return self.value < other.value

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

        :param int number: ilość liczb w wektorach do wygenerowania
        """
        #candidate = None
        #sigma = None
        #candidate = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
        #sigma = rand(len(bounds))
        #self.param_values.append(candidate)
        #self.odchylenia.append(sigma)
        self.param_values = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
        self.odchylenia = rand(len(bounds))


    def calculate_value(self, val):
        """
        Wyznacz przystosowanie osobnika na podstawie jego wektora parametrów.
        Składowe wektora są sortowane i ich kolejność wyznacza trase.


        """
        self.value = self.objective(val)
     

    def mutation(self):
        """
        Mutacja wektora parametrów oraz wektora odchyleń osobnika
        """
        n = len(self.param_values)
        rand1 = random.normalvariate(0, 1)
        tau = 1/((2*n**(1/2))**(1/2))
        fi = 1/((2 * n) ** (1 / 2))
        for i in range(n):
            rand2 = random.normalvariate(0, 1)
            self.odchylenia[i] *= math.exp(tau*rand2 + fi*rand1)
            if self.odchylenia[i] < 0.1:
                self.odchylenia[i] = 0.1
            rand3 = random.normalvariate(0, self.odchylenia[i])
            self.param_values[i] += rand3
   
  