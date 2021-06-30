<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
from database1 import Database
from schema import StoreSchema
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
from Database import Database
from Population_db.schema import StoreSchema
>>>>>>> Stashed changes

store_schema = StoreSchema()

Database.initialize()
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< HEAD
<<<<<<< HEAD
Database.save_to_db({"_id": 156, "parameters": [0,1], "stadnard_deviation": [33,66], "fitness": 22.77})
=======
#Database.save_to_db({"_id": "18", "name": "Walmart", "location": "Ve, CA"})
>>>>>>> parent of 65101da (Działa_zapis)
=======
#Database.save_to_db({"_id": "18", "name": "Walmart", "location": "Ve, CA"})
>>>>>>> parent of 65101da (Działa_zapis)

#loaded_objects = Database.load_from_db({"name": "Walmart"})
=======
#Database.save_to_db({"_id": 168, "parameters": [0.55,1.9], "standard_deviation": [3.3,6.6], "fitness": 22.77})

loaded_objects = Database.load_from_db({"_id": 168})
>>>>>>> Stashed changes
=======
#Database.save_to_db({"_id": 168, "parameters": [0.55,1.9], "standard_deviation": [3.3,6.6], "fitness": 22.77})

loaded_objects = Database.load_from_db({"_id": 168})
>>>>>>> Stashed changes
=======
#Database.save_to_db({"_id": 168, "parameters": [0.55,1.9], "standard_deviation": [3.3,6.6], "fitness": 22.77})

loaded_objects = Database.load_from_db({"_id": 168})
>>>>>>> Stashed changes

Database.update_to_db({"_id": "1"},{"$set" : { "name": "marchhin" , "location": "g"}})

for loaded_store in loaded_objects:
    store = store_schema.load(loaded_store)
    print(store.fitness)