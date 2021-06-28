import pymongo

class Database:
	@classmethod
	def initialize(cls):
		client = pymongo.MongoClient("mongodb+srv://User:Z4zDyRRX5UaF2ep@cluster0.qmglk.mongodb.net/myFirstDatabase?retryWrites=true")
		cls.database = client.get_default_database()

	@classmethod
	def save_to_db(cls, data):
		cls.database.stores.insert_one(data)

	@classmethod
	def load_from_db(cls, query):
		return cls.database.stores.find(query)

	@classmethod
	def update_to_db(cls, find , query):
		cls.database.stores.update_one(find, query)