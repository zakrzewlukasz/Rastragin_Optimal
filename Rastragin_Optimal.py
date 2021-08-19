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
from bson.objectid import ObjectId

from Population import Population
from Database import Database
from Population_db.schema import StoreSchema
from Population_db.schema_info import StoreSchema_info



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
        self.info = []


        # check if a point is within the bounds of the search
    #def in_bounds(point, bounds):
	   # # enumerate all dimensions of the point
    #    for d in range(len(bounds)):
		  #  # check if out of bounds for this dimension
    #        if point[d] < bounds[d, 0] or point[d] > bounds[d, 1]:
    #            return False
    #        return True

    def initiate_population(self, liczba_osobnikow): #raczej w populacji kalsa

        # inicjacja populacji
        for i in range(liczba_osobnikow):
            self.populacja.append(Population())
            #self.populacja[i]._id = i 
            self.populacja[i].generate(liczba_osobnikow, bounds)
            self.populacja[i].calculate_value(self.populacja[i].parameters)
            #populacja[i].calculate_value(self.dist_matrix, self.time_matrix, self.cost_matrix)

        self.min = self.populacja[0].fitness

    def sort_population(self, liczba_osobnikow): # raczej w populacji kalsa
        self.populacja.sort(key=lambda x: x.fitness)

        for i in range(liczba_osobnikow):
            self.populacja[i]._id = i

    def start_algorithm(self, start_pop, no_of_gen):
        """
        Algotyrtm strategii ewolucyjnej (µ+λ).

        :param int start_pop: początkowa ilość osobników w każdym pokoleniu
        :param int no_of_gen: maksymalna ilość pokoleń w algorytmie 
        """
        liczba_pokolen = no_of_gen
        liczba_osobnikow = start_pop
        #populacja = []


        # inicjacja populacji
        #for i in range(liczba_osobnikow):
        #    populacja.append(Invid())
        #    populacja[i].generate(liczba_osobnikow, bounds)
        #    populacja[i].calculate_value(populacja[i].param_values)
        #    #populacja[i].calculate_value(self.dist_matrix, self.time_matrix, self.cost_matrix)

        self.min = self.populacja[0].fitness

        #db = DB()
        #db.conncect(populacja, liczba_osobnikow)
        #db.mongodb_connect()


       # print(populacja[3].odchylenia)
        while liczba_pokolen > 0:

            ############################################
            #           KRZYŻOWANIE I MUTACJA

            children = self.crossover_arithmetic() #children do poprawy nie ma childrens
            for child in children:
                child.mutation()
                child.calculate_value(child.parameters)
                self.populacja.append(child)
            ############################################
            #           ZNAJDŹ LEPSZEGO OSOBNIKA
            for inv in self.populacja:
                if self.min > inv.fitness:
                    self.min = inv.fitness
                    self.best_gen = no_of_gen - liczba_pokolen
                    
                    #print(self.min)
                    #print(inv.parameters)
                    #print(self.best_gen)
            ############################################
            #               SELEKCJA
            self.sort_population(liczba_osobnikow)
            self.populacja = self.populacja[:liczba_osobnikow]
            #self.best_results.append(self.min) #chyba równa się, bo robi tablice 
            self.best_results = self.min
            #print(self.best_results)
            liczba_pokolen -= 1
            #print(liczba_pokolen)
            


    def crossover_arithmetic(self, multiply=10):
        """
        Operacja rekombinacji

        :param list populacja: obecna populacja w pokoleniu
        :param int multiply: wyznacznik ile razy więcej dzieci ma powstać w stosunku do liczby populacji
        :return: pula potomków
        :type return: list
        """
        children = []
        pop_lenght = len(self.populacja)
        random.shuffle(self.populacja)
        pop_nums = range(0, pop_lenght)
        for _ in range(pop_lenght * multiply):
            nums = random.sample(pop_nums, k=2)
            krzyzowanie = [self.populacja[nums[i]] for i in range(len(nums))]
            new_param = np.divide(np.add(krzyzowanie[0].parameters, krzyzowanie[1].parameters), 2)
            new_odch = np.divide(np.add(krzyzowanie[0].standard_deviation, krzyzowanie[1].standard_deviation), 2)
            children.append(Population())
            children[_].parameters = list(new_param)
            children[_].standard_deviation = list(new_odch)
        return children



if __name__ == "__main__":
    bounds = asarray([[-5.12, 5.12], [-5.12, 5.12]])
    gen = Genetic()
    store_schema = StoreSchema()
    store_schema_info = StoreSchema_info()

    Database.initialize()
    #Database.save_to_db_info({"_id": 0, "instances": 0, "algo_start": 6, "algo_end": 0})





    #Pobierz informacje o ilości podłączonych komputerów 
    loaded_info = Database.load_from_db_info({"_id": {'$eq': 0}})
    for loaded_store in loaded_info:
        gen.info = store_schema_info.load(loaded_store)

    #Ta instacja zostaje rootem w algorytmie, czyli generuje populację oraz rozdziela obliczenia 
    if gen.info.instances == 0:
        Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"instances": 1}})
        Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"end": False}})
        Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"algo_start": 0}})
        Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"algo_end": 0}})
        
        #Usuń rekordy dotyczące populacji z bazy danych 
        Database.delete_db_collection_evo_records()

        #Wprowadź wilekość populacji 
        liczba_osobnikow = int(input('Wprowadź rozmair populacji początkowej µ: ' ))

        #Zapisz rozmiar populacji 
        Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"population_size": liczba_osobnikow}})

        #Wygeneruj populację 
        gen.initiate_population(liczba_osobnikow)
        gen.sort_population(liczba_osobnikow)

        #Zapisz populację do bazy danych 
        for i in range(len(gen.populacja)): 
            #https://careerkarma.com/blog/python-typeerror-list-indices-must-be-integers-or-slices-not-str/  opis range len 
            #print(gen.populacja[i]._id)
            Database.save_to_db({"_id":gen.populacja[i]._id, "parameters": gen.populacja[i].parameters.tolist(), "standard_deviation": gen.populacja[i].standard_deviation.tolist(), "fitness": gen.populacja[i].fitness})
     

        print("Czy rozpocząć obliczenia? \n tak - rozpocznij obliczenia \n nie - oczekuje na połączenie innych komputerów lub sprawdza stan algorytmu, \n end- kończy pracę \n")
        print("Obecnie podłączona liczba komputerów: " + str(gen.info.instances))
        value = str(input())

        while value != 'end':
            #Pobierz informacje o ilości podłączonych komputerów 
            loaded_info = Database.load_from_db_info({"_id": {'$eq': 0}})
            for loaded_store in loaded_info:
                gen.info = store_schema_info.load(loaded_store)
            #print("Obecnie podłaczono: " + str(gen.info.instances - 1))

            if value == 'tak':
                print("tak")
                Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"algo_start": 1}})
               
            elif value == 'nie':
                    print("Obecnie podłaczono: " + str(gen.info.instances -1))

            if gen.info.algo_end == gen.info.instances -1 and gen.info.algo_start == 1:
                #pobierz obiekty i sortuj 
                print("algo_edn=instances-1, sortuj")

                Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"algo_start": 0}})
                Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"algo_end": 0}})

                loaded_objects = Database.load_from_db({"_id": {'$gte' : 0 , '$lt' : gen.info.population_size }})
                for loaded_store in loaded_objects:
                    gen.populacja.append(store_schema.load(loaded_store))

                
                gen.sort_population(gen.info.population_size)
                 
                for i in range(gen.info.population_size): 
                    Database.update_to_db({"_id": {'$eq': i}}, {"_id": i , "parameters": gen.populacja[i].parameters, "standard_deviation": gen.populacja[i].standard_deviation, "fitness": gen.populacja[i].fitness})
            

            value = str(input())
        
        #Zamknij pozstałe nody
        if value == 'end':
            Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"end": True}})
            Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"instances": 0}})

    #Ta instancja zostaje nodem, wykonuje obliczenia 
    elif gen.info.instances > 0:
        instance_number = gen.info.instances
        Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"instances": gen.info.instances + 1}})
 
        while gen.info.end == False:
            #Pobierz informacje o ilości podłączonych komputerów 
            loaded_info = Database.load_from_db_info({"_id": {'$eq': 0}})
            for loaded_store in loaded_info:
                gen.info = store_schema_info.load(loaded_store)

            print(gen.info.end)

            if gen.info.algo_start == 0:
                status = False 
            while gen.info.algo_start != 1 and status == False and gen.info.instances > 0 :
                #Pobierz informacje o ilości podłączonych komputerów 
                loaded_info = Database.load_from_db_info({"_id": {'$eq': 0}})
                for loaded_store in loaded_info:
                    gen.info = store_schema_info.load(loaded_store)
                print("Obecnie podłaczono: " + str(gen.info.instances -1))

                if gen.info.algo_start == 1:
                    #Część całkwita dzielenia // ---> początek::((instance number-1)*poulation_size)//instances  koniec:(instance number*poulation_size)//instances (instances pomijeszamy, bo jest tam rootem)
                    loaded_objects = Database.load_from_db({"_id": {'$gte' : ((instance_number - 1)*gen.info.population_size)//(gen.info.instances - 1) , '$lt' : (instance_number*gen.info.population_size)//(gen.info.instances - 1) }})
                    for loaded_store in loaded_objects:
                        gen.populacja.append(store_schema.load(loaded_store))

                
                    gen.start_algorithm(len(gen.populacja), 1)
                
                    j = 0
                    for i in range(((instance_number - 1)*gen.info.population_size)//(gen.info.instances - 1) , (instance_number*gen.info.population_size)//(gen.info.instances - 1)): 
                        Database.update_to_db({"_id": {'$eq': i}}, {"_id": i , "parameters": gen.populacja[j].parameters, "standard_deviation": gen.populacja[j].standard_deviation, "fitness": gen.populacja[j].fitness})
                        j += 1
                    status = True

                    #Pobierz informacje o ilości podłączonych komputerów 
                    print("Zakończono obliczenia")
                    loaded_info = Database.load_from_db_info({"_id": {'$eq': 0}})
                    for loaded_store in loaded_info:
                        gen.info = store_schema_info.load(loaded_store)
                    algo_end = gen.info.algo_end
                    Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"algo_end": algo_end + 1}})

                time.sleep(10)

   



















#    gen.start_algorithm(len(gen.populacja), 30)


    

    #    #SELEKCJA KONWEKCYJNA
    #    while db.instance -1 >= db.algo_end: #Wartość pominiejszona, bo w instnaces jest też master, który nie wykonuje obliczeń
    #        print(db.db_algorithm_status())
    #        print("Brak podłączonych komputerów lub proszę czekać na wykonanie obliczeń...")
    #        time.sleep(10)


    #elif db.instance > 1:
    #    print("Czy poczekać na inne komputery? odp. TAK lub NIE \n")
    #    value = str(input())
    #    if value == 'TAK':
    #        print("xx")
    #    else:
    #        print(db.db_algorithm_status())
    #        db.get_population(gen.sub_population, 6, db.instance)
    #        print("tes")
    #        #value = print("Czy poczekać na inne komputery? odp. TAK lub NIE \n")



    #db.mongodb_disconncect()










    #    loaded_objects = Database.load_from_db({"_id": {'$gte' : 0, '$lt' : 60 }})
    #for loaded_store in loaded_objects:
    #    gen.populacja.append(store_schema.load(loaded_store))
    #    #print(store.parameters)
    #    #gen.populacja.append(Population(store.parameters, store.standard_deviation, store.fitness, store._id))

    ##for i in gen.populacja:
    ##    print(i.fitness)