import numpy as np
import math 
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
from datetime import datetime, timedelta
from bson.objectid import ObjectId

from Population import Population
from Database import Database
from Population_db.schema import StoreSchema
from Info_db.schema_info import StoreSchema_info
from Node_db.schema import StoreSchema_node



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
        self.node = []


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
    store_schema_node = StoreSchema_node()

    Database.initialize()
    #Database.save_to_db_info({"_id": 0, "instances": 0, "algo_start": 6, "algo_end": 0})





    #Pobierz informacje o ilości podłączonych komputerów 
    loaded_info = Database.load_from_db_info({"_id": {'$eq': 0}})
    for loaded_store in loaded_info:
        gen.info = store_schema_info.load(loaded_store)

    #Ta instacja zostaje rootem w algorytmie, czyli generuje populację oraz rozdziela obliczenia 
    if gen.info.root == 0: #warunek zabezpieczajcy awaryje zatrzymanie root, aby ustawic potem na 0
        
        #Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"instances": 0}})
        Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"end": False}})
        Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"algo_start": 0}})
        Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"algo_end": 0}})
        Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"root": 1}})
        
        #Usuń rekordy dotyczące populacji z bazy danych 
        Database.delete_db_collection_evo_records()

        #Usuń rekordy dotyczące podziału nodów
        Database.delete_db_collection_nodes()

        #Wprowadź wilekość populacji 
        liczba_osobnikow = int(input('Wprowadź rozmair populacji początkowej µ: ' ))

        #Wprowadź liczbę generacji algorytmu
        #liczba_generacji = int(input('Wprowadź liczbę generacji algorytmu: ' ))

        #Zapisz rozmiar populacji 
        Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"population_size": liczba_osobnikow}})

        #Zapisz liczbę generacji
        #Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"generation_number": liczba_generacji}})

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
                #Wprowadź liczbę generacji algorytmu
                liczba_generacji = int(input('Wprowadź liczbę generacji algorytmu: ' )) # zabezpiecznei na wprowadzenie liczby konieczne
                #Zapisz liczbę generacji
                Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"generation_number": liczba_generacji}})
                time.sleep(5)
                #Rozpaczęcie algorytmu oraz oznaczenie root node
                Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"algo_start": 1, "root": 1}})

                try:

                    #Oczekiwanie na dołaczenie minimum jednego noda
                    i = 0
                    while gen.info.instances == 0:
                        print("Oczekiwanie na dołączenie nodów")
                        time.sleep(10)
                        i+=1
                        pass
                        #Po 5 razach opuśc pętle 
                        if i == 5:
                            break

                    #Wykonaj, gdy dołaczy jakiś node
                    else:
                        #Pobierz informacje o ilości podłączonych komputerów 
                        loaded_info = Database.load_from_db_info({"_id": {'$eq': 0}})
                        for loaded_store in loaded_info:
                            gen.info = store_schema_info.load(loaded_store)

                        #Zadecyduj jakie ma być n - czy 2n czy n^2 (n- na ile części podzielić populację)
                        result = gen.info.population_size/gen.info.instances

                        #if result >= 10:
                        #    pop_divide = pow(gen.info.instances,2)

                        #else:

                        #    pop_divide = 2*gen.info.instances
                        pop_divide = 4*gen.info.instances

                        ##Sprawdź jaki zakres ma ostatni node 
                        #loaded_info = Database.load_from_db_nodes({})
                        #for loaded_store in loaded_info:
                        #    gen.node.append(store_schema_node.load(loaded_store))

                     
                        #Podziel populacje na nody
                        #- pamiętac aby dodać osobniki do ostatniego node, kótre zostały po podziale polulacji (reszta z dzielnia)
                        for i in range(gen.info.population_size // pop_divide):
                            if(i == ((gen.info.population_size // pop_divide)-1)):
                                 Database.save_to_db_nodes({"_id":i,
                                "population_range_in": i*pop_divide,
                                "population_range_out": gen.info.population_size,
                                "time": 0,
                                "calculated" : 0,
                                "in_progress": False,
                                #"start_time": time.strftime("%H:%M:%S", time.gmtime())})
                                "start_time": str(datetime.now())})
                            else:
                                Database.save_to_db_nodes({"_id":i,
                                "population_range_in": i*pop_divide,
                                "population_range_out": i*pop_divide + pop_divide -1,
                                "time": 0,
                                "calculated" : 0,
                                "in_progress": False,
                                "start_time": str(datetime.now())})


                        print("Rozpoczęto obliczenia!")

                        while liczba_generacji > 0:
                            #print("Oczekuje na zkończenie obliczeń")
                            time.sleep(10)

                            #import info o nodach 
                            gen.nodes = []
                            loaded_info = Database.load_from_db_nodes({})
                            for loaded_store in loaded_info:
                                gen.nodes.append(store_schema_node.load(loaded_store))
                            
                            #statusy nodów oraz aktualizacja czasu
                            for i in range(len(gen.nodes)):
                                if(gen.nodes[i].calculated == 0):
                                    Database.update_to_db_nodes({"_id": {'$eq': i}}, {'$set': {"time": ((datetime.now() - gen.nodes[i].start_time).total_seconds())}})
                                    

                            #- jesli koniec populacji sprawdź statusy nodów - zobacz czy kótryś nie przekroczył średniego czasu  

                            #zobacz czy nie został jako ostatni wtedy średnia oszukana, daj mu dodatkowe kilkanascie sec i usun

                            #- error in status weź jego populacje 


                            if gen.info.algo_end == gen.info.instances -1 and gen.info.algo_start == 1: #do modyfikcajci, progam ma zacząć sortowanie bazy danych po obliczeniu wszystkich osobników 
                                #pobierz obiekty i sortuj 
                                print("Sortuj, Selekcja konwekcyjna")
                                print("Generacja:" + str(liczba_generacji))
                                time.sleep(5)

                                #Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"algo_start": 0}})
                                Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"algo_end": 0}})
                                #Wyczyść tablicę 
                                gen.populacja = []
                                loaded_objects = Database.load_from_db({"_id": {'$gte' : 0 , '$lt' : gen.info.population_size }})
                                for loaded_store in loaded_objects:
                                    gen.populacja.append(store_schema.load(loaded_store))

                
                                gen.sort_population(gen.info.population_size)
                 
                                for i in range(gen.info.population_size): 
                                    Database.update_to_db({"_id": {'$eq': i}}, {"_id": i , "parameters": gen.populacja[i].parameters, "standard_deviation": gen.populacja[i].standard_deviation, "fitness": gen.populacja[i].fitness})
                                            
                                liczba_generacji -= 1
                                Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"generation_number": liczba_generacji}})

                    Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"algo_start": 0}})
                    print("Co dalej chcesz zrobić? \n tak - rozpocznij obliczenia \n nie - oczekuje na połączenie innych komputerów lub sprawdza stan algorytmu, \n end- kończy pracę \n")


                except KeyboardInterrupt: # !!!throw execption do poprawy!!
                    Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"root": 0}})
                    continue
                    
                

            elif value == 'nie':
                    print("Obecnie podłaczono: " + str(gen.info.instances))

          
            value = str(input())
        
        #Zamknij pozstałe nody
        if value == 'end':
            Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"end": True}})
            Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"instances": 0}})
            Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"root": 0}})
           


    #Ta instancja zostaje nodem, wykonuje obliczenia 
    elif gen.info.root == 1:
        Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"root": 0}})
        instance_number = gen.info.instances
        Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"instances": gen.info.instances + 1}}) #Czy to potrzebne

        #Zadecyduj jakie ma być n - czy 2n czy n^2 (n- na ile części podzielić populację)
        #result = gen.info.population_size/gen.info.instances

        #if result >= 10:
        #    pop_divide = pow(gen.info.instances,2)

        #else:
        #    pop_divide = 2*gen.info.instances

        #Sprawdź jaki zakres ma ostatni node 
        loaded_info = Database.load_from_db_nodes({})
        for loaded_store in loaded_info:
            gen.node.append(store_schema_node.load(loaded_store))

        #- ustal, od którego osobnika zacząć
        n_nodes = len(gen.node)


        #- jesli koniec populacji sprawdź statusy nodów - zobacz czy kótryś nie przekroczył średniego czasu 


        #- error in status weź jego populacje 


        #- utwórz node wstaw w niego star_time flaga in_progres, pop_in i pop_out 
        #Database.save_to_db_nodes({"_id":instance_number,
        #                          "population_range_in": 0,
        #                          "population_range_out": 10,
        #                          "time": 0,
        #                          "in_progress": False,
        #                          "start_time": time.strftime("%H:%M:%S", time.gmtime())})
     









        #####TO DZIAŁAŁO
 
        while gen.info.end == False:
            #Pobierz informacje o ilości podłączonych komputerów 
            loaded_info = Database.load_from_db_info({"_id": {'$eq': 0}})
            for loaded_store in loaded_info:
                gen.info = store_schema_info.load(loaded_store)

            liczba_generacji = gen.info.generation_number

            #print(gen.info.end)

            #if gen.info.algo_start == 0:
            #    status = False 
            while gen.info.algo_start == 1 and gen.info.generation_number > 0 :
                #Pobierz informacje o ilości podłączonych komputerów 
                loaded_info = Database.load_from_db_info({"_id": {'$eq': 0}})
                for loaded_store in loaded_info:
                    gen.info = store_schema_info.load(loaded_store)
                print("Obecnie podłaczono: " + str(gen.info.instances -1))

                if gen.info.algo_start == 1 and liczba_generacji == gen.info.generation_number:
                    #Część całkwita dzielenia // ---> początek::((instance number-1)*poulation_size)//instances  koniec:(instance number*poulation_size)//instances (instances pomijeszamy, bo jest tam rootem)
                    loaded_objects = Database.load_from_db({"_id": {'$gte' : ((instance_number )*gen.info.population_size)//(gen.info.instances) , '$lt' : (instance_number*gen.info.population_size)//(gen.info.instances ) }})
                    for loaded_store in loaded_objects:
                        gen.populacja.append(store_schema.load(loaded_store))

                
                    gen.start_algorithm(len(gen.populacja), 1)
                
                    j = 0
                    for i in range(((instance_number )*gen.info.population_size)//(gen.info.instances ) , (instance_number*gen.info.population_size)//(gen.info.instances )): 
                        Database.update_to_db({"_id": {'$eq': i}}, {"_id": i , "parameters": gen.populacja[j].parameters, "standard_deviation": gen.populacja[j].standard_deviation, "fitness": gen.populacja[j].fitness})
                        j += 1
                    #status = True

                    #Pobierz informacje o ilości podłączonych komputerów 
                    print("Zakończono obliczenia")
                    loaded_info = Database.load_from_db_info({"_id": {'$eq': 0}})
                    for loaded_store in loaded_info:
                        gen.info = store_schema_info.load(loaded_store)
                    algo_end = gen.info.algo_end
                    Database.update_to_db_info({"_id": {'$eq': 0}}, {'$set': {"algo_end": algo_end + 1}})
                    print("Generacja:" + str(liczba_generacji))
                    liczba_generacji -= 1

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




#   co jesli ktorys nei zwróci danych 
#czas ewaluacji funckji celu 
#ktorys moze byc z nich wolniejszy 
#4 rodzice mi lmabada potomków 
#n =100 osbników

#jesli czas obliczen jest za dlugi mozna dac innego 

#n 100
#5 osobniikow 8 potmkow zwracam 5 najlepszych 
#wrzucamy do workera mi 


#3 punkt przeglad stanu wiedzy - dzielimy 
#Strategie ewolucyje oepratory gentyczne 
#dwie startegi mi,lambda oraz mi plus lambda 
#strategie różnicowe może warto zazanczyć
#schematy selekcji 
#nie sukipać się na wszsytkoch tylku usystematyzować 

#przeglad standarów obliczeń chmurowych jak ona jest ulokowana w chmurach 

#4. wymagania jakie chcemy osiegnac 
#5 koncpecja rozwiązanaia - chmura tkaiego typu, workerzy, schemat blokowy 
#6. projekt wykonania i implenatacja 

#7 Badania i analiza wyników 

#porównać z szybkościa na jenym komputarze 
#wydajność wezłów ciezko zbadac na rastraginie 

#funkcja celu - Jiles-Atherton model
#rozwiazywanie równania różniczkowego zjada czas wersja isotrosipic
#artykuł z 2000 złe obliczenie równanai różniczkowego 

#modele selecji porównać czy nie ucieka do 
#czas konwergencji czas jaki osiągnie zbieżność jakie najlpszy osobnik w poszczegolnych iteracjach 
#algorytm stochastyczny - 





#SCHEMAT NODE:
#- utwórz node wstaw w niego star_time flaga in_progres, pop_in i pop_out 
#- oczekuj  na otrzymanie zakresu populacji 

#- zadecyduj jakie ma być n czy 2n czy n^2
#- zobacz jaki zakres ma ostatni dodany node 
#- jesli koniec populacji sprawdź statusy nodów - zobacz czy kótryś nie przekroczył średniego czasu, ustaw na nim flagę, że jeszcze do policzenia
#- error in status weź jego populacje 
#- utwórz node wstaw w niego star_time flaga in_progres, pop_in i pop_out 



##Zadanie dla root
#- zobacz czy któryś skończył 
#- oblicz średni czas powyżej 2 nodów - jeśli dłuższy niż jakiś czas usuń go ( czas wyliczony średnio z próbek)
#- zobacz czy kótryś noode nie przekroczył średniego czasu, ustaw na nim flagę, że jeszcze do policzenia
#- popraw try exeption z ctrc+c powduje zwracanie wyjątku 
#- pamiętac aby dodać osobniki do ostatniego node, kótre zostały po podziale polulacji (reszta z dzielnia) - zrobione











