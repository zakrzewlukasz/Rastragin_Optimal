from marshmallow import Schema, fields, post_load
from store import Store

class InnerSchema(Schema):
     foo = fields.Int()
     fo = fields.Int()

class StoreSchema(Schema):
<<<<<<< Updated upstream:schema.py
     _id = fields.Str()
     name = fields.Str()
     location = fields.Str()
=======
     _id = fields.Int()
     parameters = []
     standard_deviation = []
     fitness = fields.Float()
>>>>>>> Stashed changes:Population_db/schema.py

     @post_load
     def make_store(self, data, **kwargs):
        return Store(**data)