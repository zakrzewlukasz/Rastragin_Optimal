from database1 import Database
from schema import StoreSchema

store_schema = StoreSchema()

Database.initialize()
<<<<<<< HEAD
Database.save_to_db({"_id": 156, "parameters": [0,1], "stadnard_deviation": [33,66], "fitness": 22.77})
=======
#Database.save_to_db({"_id": "18", "name": "Walmart", "location": "Ve, CA"})
>>>>>>> parent of 65101da (Działa_zapis)

#loaded_objects = Database.load_from_db({"name": "Walmart"})

Database.update_to_db({"_id": "1"},{"$set" : { "name": "marchhin" , "location": "g"}})

for loaded_store in loaded_objects:
    store = store_schema.load(loaded_store)
    print(store.name)