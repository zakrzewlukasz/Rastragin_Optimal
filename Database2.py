#from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint
from Population import Invid
import numpy as np
#from pymongo.errors import ConnectionFailure
import pymongo


class DB:

	def __init__(self):
		self.connection_status = None #Connection_DB_status
		self.database = None #Database
		self.database_info = None #DB info
		self.pop_collection = None #Population_Table
		self.instance = 0 # Master or slave
		self.algo_end = 0 # Check if slave end evaluate pop
		#self.n_nodes =0 #Total number of nodes 

	def conncect(self, populacja, liczba_osobnikow):
		client = MongoClient("mongodb+srv://User:Z4zDyRRX5UaF2ep@cluster0.qmglk.mongodb.net/myFirstDatabase?retryWrites=true")
		db = client.get_database('evo_db')
		#records = db.evo_records
		#records.find_one({"name": "test"})
		#db = client.test_database
		
		population_records = client.evo_db.evo_records
		database_info = client.evo_db.info
		#print (db.serverStatus().connection)
		#print(collection)

		#for document in collection.find({}):
		#	pprint(document)

		mylist = []

		for x in range(liczba_osobnikow):
			#konwersja do listy naszej tablicy [ , ]
			record = {"_id" : x, "param": populacja[x].param_values.tolist(), "odchylenia": populacja[x].odchylenia.tolist(), "fitness": populacja[x].value}
			mylist.append(record)

		
		#population_records.insert_many(mylist)
		#object.param_values = np.fromiter( record['param'] )
		#np.asarray( object.param_values )
		#np.asarray( record['param'], dtype = None, order = None )
		#np.asarray( object.param_values )
		#np.asarray( object.odchylenia )

		
		for x in database_info.find({}, {"_id": 0, "instances": 1}):
			print(x)
			n_nodes = x.get('instances')
			print(n_nodes)


		n_nodes += 1
		myquery = { "_id": ObjectId("60abad83ca6b50b7c1a6f669") }
		newvalues = { "$set": { "instances": n_nodes } }
		
		database_info.update_one(myquery, newvalues)

		
		#myresults = database_info.find({}, {"_id": 0, "instances": 1})
		#print(myresults)	


	def mongodb_connect(self): # nie zwraca błedów dopiero jak zapuścisz query może być błąd

		client = pymongo.MongoClient("mongodb+srv://User:Z4zDyRRX5UaF2ep@cluster0.qmglk.mongodb.net/myFirstDatabase?retryWrites=true") 



		try:
			client.list_database_names()
			self.connection_status = True
			print("Pomyślnie połączono z bazą danych")
		except:
			self.connection_status = False
			print("Nie można połaczyć z bazą danych")

		try:
			self.database = client.evo_db
			self.database_info = client.evo_db.info
			self.pop_collection = client.evo_db.evo_records
			self.connection_status = True
		except:
			self.connection_status = False
			print("Wymagane tabele nie istnieją w bazie dancyh")

		if(self.connection_status == True):
			for x in self.database_info.find({}, {"_id": 0, "instances": 1}):
				self.instance = x.get('instances')

			self.instance += 1
			myquery = { "_id": ObjectId("60abad83ca6b50b7c1a6f669") }
			newvalues = { "$set": { "instances": self.instance } }
			self.database_info.update_one(myquery, newvalues)

	def mongodb_disconncect(self):
		self.instance -= 1
		myquery = { "_id": ObjectId("60abad83ca6b50b7c1a6f669") }
		newvalues = { "$set": { "instances": self.instance } }
		self.database_info.update_one(myquery, newvalues)

	def store_population(self, populacja, liczba_osobnikow ):
		self.pop_collection.drop()
		mylist = []
		#xx = 'ss'
		#mycollection = self.database[xx]

		for x in range(liczba_osobnikow):
			#konwersja do listy naszej tablicy [ , ]
			record = {"_id" : x, "param": populacja[x].param_values.tolist(), "odchylenia": populacja[x].odchylenia.tolist(), "fitness": populacja[x].value}
			mylist.append(record)
		
		self.pop_collection.insert_many(mylist)
		#mycollection.insert_many(mylist)

	#def db_number_nodes(self):
	#	for x in self.database_info.find({}, {"_id": 0, "instances": 1}):
	#		n_nodes = x.get('instances')
	#	return n_nodes

	def db_algorithm_status(self):
		for x in self.database_info.find({}, {"_id": 0, "algo_end": 1}):
			self.algo_end = x.get('algo_end')

	
	def db_algorithm_end(self):
		self.algo_end += 1
		myquery = { "_id": ObjectId("60abad83ca6b50b7c1a6f669") }
		newvalues = { "$set": { "algo_end": self.algo_end } }
		self.database_info.update_one(myquery, newvalues)

	def get_population(self, populacja, liczba_osobnikow, instance):
		for x in self.pop_collection.find({"_id": {'$gt' : 0, '$lt' : liczba_osobnikow/2 }}):
			populacja.append(Invid())
			populacja.param_values = x.get('param')
			populacja.odchylenia = x.get('odchylenia')
			populacja.value = x.get('fitness')
			

