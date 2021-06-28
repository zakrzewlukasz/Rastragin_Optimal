from Population import Invid
from Database import DB
import numpy as np
from numpy import asarray
from numpy import exp
from numpy import sqrt
from numpy import cos
from numpy import e
from numpy import pi
from numpy import argsort
import random
from numpy.random import randn
from numpy.random import rand
from numpy.random import seed
import time



class Genetic:
    """
    Główna klasa programu
    """
    def __init__(self):

        #self.load_data()
        #self.bounds = asarray([[-5.12, 5.12], [-8, -10]])
        self.best_results = []
        self.best_gen = None
        self.min = None
        self.lam = 100
        self.mu = 20
        self.populacja = []
        self.sub_population = []


        # check if a point is within the bounds of the search
    #def in_bounds(point, bounds):
	   # # enumerate all dimensions of the point
    #    for d in range(len(bounds)):
		  #  # check if out of bounds for this dimension
    #        if point[d] < bounds[d, 0] or point[d] > bounds[d, 1]:
    #            return False
    #        return True

    def initiate_population(self, liczba_osobnikow):

        # inicjacja populacji
        for i in range(liczba_osobnikow):
            self.populacja.append(Invid())
            self.populacja[i].generate(liczba_osobnikow, bounds)
            self.populacja[i].calculate_value(self.populacja[i].param_values)
            #populacja[i].calculate_value(self.dist_matrix, self.time_matrix, self.cost_matrix)

        self.min = self.populacja[0].value



    def start_algorithm(self, start_pop, no_of_gen):
        """
        Algotyrtm strategii ewolucyjnej (µ+λ).

        :param int start_pop: początkowa ilość osobników w każdym pokoleniu
        :param int no_of_gen: maksymalna ilość pokoleń w algorytmie
        """
        liczba_pokolen = no_of_gen
        liczba_osobnikow = start_pop
        populacja = []


        # inicjacja populacji
        for i in range(liczba_osobnikow):
            populacja.append(Invid())
            populacja[i].generate(liczba_osobnikow, bounds)
            populacja[i].calculate_value(populacja[i].param_values)
            #populacja[i].calculate_value(self.dist_matrix, self.time_matrix, self.cost_matrix)

        self.min = populacja[0].value

        #db = DB()
        #db.conncect(populacja, liczba_osobnikow)
        #db.mongodb_connect()


       # print(populacja[3].odchylenia)
        while liczba_pokolen > 0:

            ############################################
            #           KRZYŻOWANIE I MUTACJA

            childrens = self.crossover_arithmetic(populacja)
            for child in childrens:
                child.mutation()
                child.calculate_value(child.param_values)
                populacja.append(child)
            ############################################
            #           ZNAJDŹ LEPSZEGO OSOBNIKA
            for inv in populacja:
                if self.min > inv.value:
                    self.min = inv.value
                    self.best_gen = no_of_gen - liczba_pokolen
                    print(self.min)
                    print(inv.param_values)
                    #print(self.best_gen)
            ############################################
            #               SELEKCJA
            populacja.sort()
            populacja = populacja[:liczba_osobnikow]
            self.best_results.append(self.min)
            #print(self.best_results)
            liczba_pokolen -= 1
            print(liczba_pokolen)


    def crossover_arithmetic(self, populacja, multiply=10):
        """
        Operacja rekombinacji

        :param list populacja: obecna populacja w pokoleniu
        :param int multiply: wyznacznik ile razy więcej dzieci ma powstać w stosunku do liczby populacji
        :return: pula potomków
        :type return: list
        """
        childrens = []
        pop_lenght = len(populacja)
        random.shuffle(populacja)
        pop_nums = range(0, pop_lenght)
        for _ in range(pop_lenght * multiply):
            nums = random.sample(pop_nums, k=2)
            krzyzowanie = [populacja[nums[i]] for i in range(len(nums))]
            new_param = np.divide(np.add(krzyzowanie[0].param_values, krzyzowanie[1].param_values), 2)
            new_odch = np.divide(np.add(krzyzowanie[0].odchylenia, krzyzowanie[1].odchylenia), 2)
            childrens.append(Invid([list(new_param), list(new_odch)]))
        return childrens



if __name__ == "__main__":
    bounds = asarray([[-5.12, 5.12], [-5.12, 5.12]])
    gen = Genetic()
    #gen2.start_algorithm(100, 30)

    db = DB()
    db.mongodb_connect()
    if db.instance == 1:
        liczba_osobnikow = int(input('Wprowadź rozmair populacji początkowej µ: ' ))
        gen.initiate_population(liczba_osobnikow)
        gen.populacja.sort()
        db.store_population(gen.populacja, liczba_osobnikow)

        #SELEKCJA KONWEKCYJNA
        while db.instance -1 >= db.algo_end: #Wartość pominiejszona, bo w instnaces jest też master, który nie wykonuje obliczeń
            print(db.db_algorithm_status())
            print("Brak podłączonych komputerów lub proszę czekać na wykonanie obliczeń...")
            time.sleep(10)


    elif db.instance > 1:
        print("Czy poczekać na inne komputery? odp. TAK lub NIE \n")
        value = str(input())
        if value == 'TAK':
            print("xx")
        else:
            print(db.db_algorithm_status())
            db.get_population(gen.sub_population, 6, db.instance)
            print("tes")
            #value = print("Czy poczekać na inne komputery? odp. TAK lub NIE \n")



    db.mongodb_disconncect()