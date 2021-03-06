import pymongo

class Database:
	@classmethod
	def initialize(cls):
		client = pymongo.MongoClient("mongodb+srv://User:Z4zDyRRX5UaF2ep@cluster0.qmglk.mongodb.net/myFirstDatabase?retryWrites=true")
		cls.database = client.get_database('evo_db')

	@classmethod
	def save_to_db(cls, data):
		cls.database.evo_records.insert_one(data)

	@classmethod
	def load_from_db(cls, query):
		return cls.database.evo_records.find(query)

	@classmethod
	def update_to_db(cls, find , query):
		cls.database.evo_records.update(find, query)

	@classmethod
	def delete_db_collection_evo_records(cls):
		cls.database.evo_records.drop()
##############   DB INFO   ##########################
	@classmethod
	def save_to_db_info(cls, data):
		cls.database.info.insert_one(data)

	@classmethod
	def update_to_db_info(cls, find , query):
		cls.database.info.update(find, query)

	@classmethod
	def load_from_db_info(cls, query):
		return cls.database.info.find(query)

	########## DB NODE ################################

	@classmethod
	def save_to_db_nodes(cls, data):
		cls.database.nodes.insert_one(data)

	@classmethod
	def load_from_db_nodes(cls, query):
		return cls.database.nodes.find(query)

	@classmethod
	def update_to_db_nodes(cls, find, query):
		return cls.database.nodes.update(find, query)

	@classmethod
	def delete_db_collection_nodes(cls):
		cls.database.nodes.drop()